# Validation — 10 October 2026

Acceptance suite: 16 meaningful core tests, module compilation, synthetic demo, wheel build and new-venv console commands outside source. Run `python verify.py`. No competitor benchmark was performed.

Remote CI is required before LIVE; receipts are recorded in the owner's chronological index. Supported matrix: Ubuntu/Python 3.10, 3.12, 3.14. Other OS/architectures are untested. Build tools must be available to run verification; the normal install path uses pip build isolation.

Offline snapshots only. Does not fetch segments, authenticate URLs, inspect codec/media bytes or measure playback. Master playlists, encryption, byte ranges, program-date-time, maps and other EXT tags are explicitly unsupported. Only the documented EXT tags are accepted. No full RFC certification. A no-overlap contiguous window is reported as overlap_count=0, not proof of segment integrity. URI hashes are identifiers, not anonymization of guessable URLs. UTF-8/BOM/CRLF, 2 MiB/playlist and 10,000 segments.

Local observed result: all acceptance checks passed on Linux/Python 3.12 with setuptools 84.0.0 and wheel 0.48.0. A new wheel environment, outside-source CLI success/failure checks and the synthetic demo passed. Remote matrix and normal build-isolated installation must still be verified at the public final commit.

Relative URI hashes compare URI text only: capture both playlists from the same base URL. This tool does not compare resolved resources or segment bytes.
