const input = document.getElementById('media-url');
const status = document.getElementById('status');
const result = document.getElementById('result');
const buttons = [...document.querySelectorAll('button')];
function state(message, error = false) {
  status.textContent = message;
  status.classList.toggle('error', error);
}
async function request(endpoint, body) {
  const response = await fetch(endpoint, {
    method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)
  });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(typeof data.detail === 'string' ? data.detail : `HTTP ${response.status}`);
  }
  return response;
}
async function act(mode) {
  if (!input.value.trim()) { state('Pega un enlace HTTPS primero.', true); input.focus(); return; }
  buttons.forEach(button => button.disabled = true);
  result.textContent = '';
  state('Procesando recurso...');
  try {
    if (mode === 'normalize' || mode === 'inspect') {
      const response = await request(`/api/${mode}`, {url: input.value.trim()});
      const data = await response.json();
      result.textContent = JSON.stringify(data, null, 2);
      state(mode === 'inspect' ? 'Metadatos obtenidos; la descarga aún no está verificada.' : 'URL normalizada.');
      return;
    }
    const response = await request('/api/download', {url: input.value.trim(), mode});
    const blob = await response.blob();
    const header = response.headers.get('Content-Disposition') || '';
    const match = header.match(/filename\*?=(?:UTF-8'')?"?([^";]+)/i);
    const safeName = match ? decodeURIComponent(match[1].replace(/"/g,'')) : `recurso-${mode}`;
    const objectUrl = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = objectUrl;
    anchor.download = safeName;
    document.body.appendChild(anchor);
    anchor.click(); anchor.remove();
    setTimeout(() => URL.revokeObjectURL(objectUrl), 30000);
    state(`Archivo recibido (${(blob.size / (1024 * 1024)).toFixed(1)} MiB).`);
  } catch (err) {
    state(`No se completó: ${err.message}`, true);
  } finally {
    buttons.forEach(button => button.disabled = false);
  }
}
const normalizeButton = document.getElementById('normalize');
normalizeButton.addEventListener('click', () => act('normalize'));
input.addEventListener('keydown', event => {
  if (event.key !== 'Enter' || event.isComposing) return;
  event.preventDefault();
  normalizeButton.click();
});
document.getElementById('inspect').addEventListener('click', () => act('inspect'));
document.getElementById('download-video').addEventListener('click', () => act('video'));
document.getElementById('download-audio').addEventListener('click', () => act('audio'));
document.getElementById('download-images').addEventListener('click', () => act('images'));
