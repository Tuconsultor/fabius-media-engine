# Instructions for human and AI contributors

AI-assisted code, documentation and tests ARE WELCOME in this repository.

1. Work in a branch with narrowly scoped commits and explain assumptions.
2. Do not change functionality without tests. Offline tests must not contact social networks.
3. Do not insert credentials, tokens, session cookies, tracked personal data or copyrighted media fixtures.
4. Respect upstream project licenses and contribution rules. Do not submit AI-generated changes to yt-dlp upstream.
5. Never add DRM circumvention, account bypass, private-content scraping or stealth evasion.
6. Treat input URLs as untrusted. This prototype MUST NOT be deployed publicly without egress filtering and abuse controls.
7. Record test commands and whether they passed; never claim downloads work without actual verified tests.
8. Keep `README.md`, `SECURITY.md` and `docs/ROADMAP.md` synchronized with features.

Suggested agent workflow: inspect code -> propose minimal patch -> write tests -> run checks -> make PR -> human review.
