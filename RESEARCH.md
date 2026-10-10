# Research and candidate brief — 10 October 2026

User: Video delivery engineers comparing two captured live HLS media-playlist windows.

Pain: An overlapping media sequence can silently change URI, duration or discontinuity number between reloads; a skipped retention window also leaves a gap that cannot be verified from one playlist.

Smallest useful capability: Parse bounded media playlists, compare overlapping sequence identities, trace discontinuity counters, identify gaps/regressions, and apply RFC-style rounded target-duration checks.

Demand is **inferred** from the workflow and established alternatives, not a verified request for this project. No invented users, adoption or growth promise.

Queries: `m3u8 sort:stars; hls playlist sort:stars`, GitHub repository search with stars qualifier, bounded first five results plus named relevant established comparables. Connector coverage and relevance selection are limited; this is not an exhaustive ranking. Highest-star relevant comparable **among those inspected**: [video-dev/hls.js](https://github.com/video-dev/hls.js) (16970 stars). Stars are research context, not technical performance.

| Exact comparable | Observed stars | Last push UTC | API license metadata |
| --- | ---: | --- | --- |
| [grafov/m3u8](https://github.com/grafov/m3u8) | 1292 | 2025-09-11T17:33:25Z | BSD-3-Clause |
| [globocom/m3u8](https://github.com/globocom/m3u8) | 2283 | 2025-01-31T21:13:34Z | NOASSERTION |
| [video-dev/hls.js](https://github.com/video-dev/hls.js) | 16970 | 2026-10-08T12:32:46Z | NOASSERTION |

Observed 10 October 2026 via GitHub repository metadata, current README and first five open issues. Missing README/license metadata is unavailable rather than evidence of absent support; NOASSERTION requires manual license review before any reuse. No reuse occurred. Archived status is preserved in raw research evidence; grafov/m3u8's README identifies its successor and suspended support.

Fair comparison: established alternatives have broader parsing, client, GUI, optimization, binding or management workflows and should be considered first. This tool offers the bounded offline workflow in the capability above, a Python source installation, synthetic example and exact failure exits. Its zero runtime dependencies do not establish better reliability or support. Installation and time-to-first-result were measured only for our examples; competitor installations and equivalent workloads were not benchmarked. We make no absence or superiority claim. Compare the stated scope/limitations with each alternative's current docs before selecting it.

Portfolio differentiation: medialoom catalogues media; this audits live playlist transitions. No existing owned repository handles HLS sequence/discontinuity reconciliation. The other four daily projects use different data, algorithms and users (video windows, mail graphs, SQL plans, PNG bytes, numeric ACLs); they are not subdivisions of one product.

Acceptance: the documented example produces its expected evidence; meaningful malformed inputs fail; original core behavior/regressions pass 16 tests; installed console command works outside source; remote CI runs Python 3.10, 3.12 and 3.14. Public existence without these checks is not a verified launch.

Discovery: HLS and m3u8 topics, a two-window CI fixture and searchable discontinuity examples.

Limits: Offline snapshots only. Does not fetch segments, authenticate URLs, inspect codec/media bytes or measure playback. Master playlists, encryption, byte ranges, program-date-time, maps and other EXT tags are explicitly unsupported. Only the documented EXT tags are accepted. No full RFC certification. A no-overlap contiguous window is reported as overlap_count=0, not proof of segment integrity. URI hashes are identifiers, not anonymization of guessable URLs. UTF-8/BOM/CRLF, 2 MiB/playlist and 10,000 segments.

## Workflow comparison

globocom/m3u8 offers pip-installable Python playlist parsing and loading; hls.js is a browser playback library with an npm/build workflow and extensive HLS support. grafov/m3u8 is a Go playlist package whose current README explicitly marks support suspended and points to a successor. These cover substantially broader media workflows. Our installation is a Python source CLI for two local snapshots and has no player, network loading or media validation. Existing upstream documentation/issues are support channels; ours offers Issues with no response-time commitment. No comparable was installed or timed today.

Evidence observed between 06:12 and 06:22 UTC, 10 October 2026. Repository metadata is a snapshot; push time is activity evidence, not a support guarantee.

Relative URI hashes compare URI text only: capture both playlists from the same base URL. This tool does not compare resolved resources or segment bytes.
