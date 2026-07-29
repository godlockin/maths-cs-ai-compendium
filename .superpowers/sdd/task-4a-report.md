# Task 4a report

- Implemented P1 unlabelled expansion and semantic candidate checks.
- Implemented P2 punctuation and CJK/Latin spacing checks with protected code, formula, URL, link, term, and abbreviation regions.
- Added JSON CLI report output, chapter mapping, strict and metrics-only modes.
- P0/P1 always block; P2 blocks only with `--strict`; CLI/mapping errors use exit 2.
- Token metrics intentionally not implemented.
