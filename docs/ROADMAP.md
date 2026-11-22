# Roadmap / Estado de desarrollo

## Implemented in source code (not verified against live platforms)
- [x] HTTPS URL normalization for TikTok, Douyin, Bilibili, LinkedIn and X
- [x] X post URL canonicalizer from a direct status URL
- [x] Python FastAPI endpoints for metadata inspection and media download
- [x] yt-dlp adapter for video and MP3 extraction
- [x] gallery-dl adapter for images ZIP
- [x] Static responsive interface and self-hosted local launcher
- [x] Offline unit/API tests and CI workflow definition
- [x] AI-contribution policy

## NOT yet verified / Not implemented
- [ ] Live authorized-download success rate per platform
- [ ] Real Android/iPhone browser downloads
- [ ] Public production security hardening
- [ ] Network sandbox preventing SSRF after redirects
- [ ] Proper job queue, progress reporting, resumable jobs, quotas
- [ ] Public deployment and domain
- [ ] Rights-holder reporting and acceptable-use legal review
- [ ] X thread link extraction using permitted official interfaces
- [ ] Gallery support audit for each platform
- [ ] Per-platform compatibility report and regression fixtures

## Milestone 0.2
1. Secure worker sandbox and upload/download quotas
2. Job API with polling and progress
3. Report success rates from 10-20 consented media links per platform
4. Dependabot and dependency vulnerability checks
5. Deployment documentation only after security review
