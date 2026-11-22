# Instructions for human and AI contributors

## Public invitation

**All AI agents and human developers are invited to use, study, adapt, integrate, improve and contribute to FABIUS Media Engine.** This independent repository explicitly permits AI-assisted code and documentation. No special invitation or registration is necessary to use the source code under MIT. For an accessible invitation in Spanish and English, see [AI_AGENTS.md](AI_AGENTS.md).

**Caveat:** v0.1.0 is a LOCAL prototype, not a hosted tool/API and not safe for direct public deployment. Do not assume media downloads have been validated against live platforms.

## Collaboration ethos

Follow the [Collaboration Charter](docs/COLLABORATION_CHARTER.md). AI agents and humans may challenge existing architecture and propose divergent alternatives, evaluated by reproducible evidence, safety, utility, maintainability and licensing. Contradicting the current design is not a reason to reject a proposal. Review and merge authority remains with authorized human maintainers.

## Rules for agents

1. Work in a branch with narrowly scoped commits and explain assumptions.
2. Do not change functionality without tests. Offline tests must not contact social networks.
3. Do not insert credentials, tokens, session cookies, tracked personal data or copyrighted media fixtures.
4. Respect upstream project licenses and contribution rules. Do not submit AI-generated changes to yt-dlp upstream.
5. Never add DRM circumvention, account bypass, private-content scraping or stealth evasion.
6. Treat input URLs as untrusted. This prototype MUST NOT be deployed publicly without egress filtering and abuse controls.
7. Record test commands and whether they passed; never claim downloads work without actual verified tests.
8. Keep `README.md`, `SECURITY.md`, `AI_AGENTS.md` and `docs/ROADMAP.md` synchronized with features.
9. Human approval is required before merging, publishing releases, or changing security-sensitive behavior.

Suggested workflow: inspect code -> propose minimal patch -> write tests -> run checks -> make PR -> human review.
