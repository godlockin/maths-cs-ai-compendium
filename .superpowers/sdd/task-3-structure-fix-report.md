# Task 3 Structure Fix

- Refactored line parsing in `scripts/verify_translation.py` so inline link/image assets are extracted independently from normalized prose across ordinary lines, lists, blockquotes/admonitions, and table rows.
- Added minimal regressions for URL-only list, blockquote/admonition, and table lines; each reports `P0-SOURCE-COVERAGE`.
- Preserved existing P0 behavior and interfaces; no P1/P2/metrics implementation.

## Verification

`python3 -m unittest tests/test_verify_translation.py -v`

- 9 tests run.
- 7 P0/legacy tests pass, including all three new regressions.
- Only expected P1 and P2 tests remain failing because those rules are intentionally not implemented.
