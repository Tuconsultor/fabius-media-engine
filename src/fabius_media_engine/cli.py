"""Command line launcher. Binds to loopback only by default."""

import argparse


def main():
    parser = argparse.ArgumentParser(description="Launch FABIUS Media Engine locally")
    parser.add_argument("--host", default="127.0.0.1", help="Local address; not production hardened")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    if args.host not in {"127.0.0.1", "localhost", "::1"}:
        parser.error("Only loopback is supported in v0.1.0. See SECURITY.md.")
    import uvicorn
    uvicorn.run("fabius_media_engine.app:app", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
