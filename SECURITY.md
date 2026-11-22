# Security status: local-only research prototype (v0.1.0)

**NOT APPROVED FOR PUBLIC INTERNET DEPLOYMENT.** Publishing source code on GitHub is not the same as securely hosting this service on a public server.

Reasons:
- yt-dlp and gallery-dl fetch remote URLs and may follow redirects, so an application-level platform domain allowlist is NOT sufficient to prevent SSRF.
- Expensive video jobs can exhaust CPU, disk, network and memory.
- Public sites need auth/rate limits, bandwidth quotas, time limits and abuse handling.
- There is no rigorous process-level sandbox in v0.1.0.
- Downloader-specific authentication is deliberately unsupported.

Before public hosting:
1. Run each job in a sandboxed container with read-only base filesystem, capped CPU/RAM/disk and outbound egress limited to safe public IP destinations using network policy/firewall.
2. Block all RFC1918, loopback, link-local, metadata-service and IPv6 private addresses, including redirects and DNS rebinding, at network level.
3. Add rate limiting, per-user quotas, abuse reporting and an acceptable use policy.
4. Add secure job queues, concurrency and storage limits, bounded output streaming, a janitor for stalled jobs, antivirus/file integrity checks, and log redaction.
5. Set explicit retention rules, legal notice and data handling practices.
6. Audit all third-party dependencies and pin exact known-good versions with hashes for release.
7. Perform pen test, dependency scan, and real downloader tests with authorized URLs.

Report suspected vulnerabilities privately to the repository maintainer through GitHub's private vulnerability reporting if enabled. Do not post exploit details in issues.
