# hls-window-audit

Parse bounded media playlists, compare overlapping sequence identities, trace discontinuity counters, identify gaps/regressions, and apply RFC-style rounded target-duration checks.

## Who and why

Video delivery engineers comparing two captured live HLS media-playlist windows. An overlapping media sequence can silently change URI, duration or discontinuity number between reloads; a skipped retention window also leaves a gap that cannot be verified from one playlist.

## Quickstart

Python 3.10+ and pip. No service, credential or runtime dependency:

```sh
git clone https://github.com/nripankadas07/hls-window-audit.git
cd hls-window-audit
python -m venv .venv
# Unix: source .venv/bin/activate; Windows: .venv\Scripts\activate
python -m pip install .
hls-window-audit before.m3u8 after.m3u8
python demo.py
python -m pip install setuptools wheel
python verify.py
```

The fixtures are synthetic. CLI JSON is on stdout. Exit 0 means the operation succeeded; HLS/mbox return 1 for findings; all tools return 2 for malformed/unsupported input or IO errors. SQLite scan signals are evidence, not policy failures. PNG output must be a new file: repeating its command requires a new output filename.

Help: `hls-window-audit --help`. See [DEMO.md](DEMO.md), [VALIDATION.md](VALIDATION.md), [RESEARCH.md](RESEARCH.md) and [SUPPORT.md](SUPPORT.md).

## Scope and limitations

Offline snapshots only. Does not fetch segments, authenticate URLs, inspect codec/media bytes or measure playback. Master playlists, encryption, byte ranges, program-date-time, maps and other EXT tags are explicitly unsupported. Only the documented EXT tags are accepted. No full RFC certification. A no-overlap contiguous window is reported as overlap_count=0, not proof of segment integrity. URI hashes are identifiers, not anonymization of guessable URLs. UTF-8/BOM/CRLF, 2 MiB/playlist and 10,000 segments.

No performance-superiority or complete-security claim. Use the comparable research to choose a tool suitable for your workflow.

## License

MIT; original implementation. Build-time setuptools/wheel and Python retain their upstream licenses.

Relative URI hashes compare URI text only: capture both playlists from the same base URL. This tool does not compare resolved resources or segment bytes.
