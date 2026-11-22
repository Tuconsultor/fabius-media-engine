# Architecture decision 001: independent orchestration layer

**Decision:** MIT-licensed code wraps yt-dlp/gallery-dl without copying source into this repository.
FFmpeg is an optional system binary for transcoding. Each dependency retains its own license.

`Browser -> FastAPI -> URL validator -> yt-dlp/gallery-dl -> temp directory -> FileResponse`

`/api/normalize` operates offline. `/api/inspect` makes network requests for metadata.
`/api/download` fetches media to temporary disk and returns the result via HTTP. Completed
responses clean up their job folders. Exceptions also clean up files.

This v0.1 is deliberately local-only: synchronous jobs inside request handlers are
unsuitable for an untrusted public workload. Version 0.2 must isolate media jobs in
network-restricted workers and move long jobs into a queue.
