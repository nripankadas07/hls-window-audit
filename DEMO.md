# Synthetic demo

Run `python demo.py` to exercise the checked-in synthetic fixture, expected success/evidence and malformed input using `smoke.json`.

Installed command: `hls-window-audit before.m3u8 after.m3u8`. Each smoke case records its exact expected exit and any essential output fields. Policies/input schemas follow the fixture files and module docstring; no private input is included.

Offline snapshots only. Does not fetch segments, authenticate URLs, inspect codec/media bytes or measure playback. Master playlists, encryption, byte ranges, program-date-time, maps and other EXT tags are explicitly unsupported. Only the documented EXT tags are accepted. No full RFC certification. A no-overlap contiguous window is reported as overlap_count=0, not proof of segment integrity. URI hashes are identifiers, not anonymization of guessable URLs. UTF-8/BOM/CRLF, 2 MiB/playlist and 10,000 segments.

Relative URI hashes compare URI text only: capture both playlists from the same base URL. This tool does not compare resolved resources or segment bytes.
