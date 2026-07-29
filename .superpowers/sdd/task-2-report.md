# Task 2 Report

## Scope

Created translation QA acceptance fixtures and tests only. Did not implement `scripts/verify_translation.py`.

## Changes

- Added canonical source fixture at `tests/fixtures/translation_qa/source/01.md`.
- Added valid labelled-enhancement target fixture.
- Added four one-mutation target fixtures covering formula change, missing paragraph, unlabelled expansion, and half-width punctuation.
- Added `tests/test_verify_translation.py` with the required five unittest cases and report-schema/rule assertions.
- Added empty `tests/__init__.py` so the specified unittest module path resolves to this repository rather than an unrelated installed `tests` package.

## Verification

Command:

```bash
python3 -m unittest tests/test_verify_translation.py -v
```

Expected red state confirmed. Test collection reaches the test module, then import fails because implementation is intentionally absent:

```text
ModuleNotFoundError: No module named 'scripts'
```

`git diff --cached --check` passed. Fixture mutation review confirmed only the requested mutation differs in each target fixture.

## Commit

`2d7e820 test: define translation QA acceptance fixtures`

## Concern

`tests/__init__.py` is an additional package marker not listed in the brief. It is needed in this environment because an installed `tests` package otherwise shadows the repository's namespace package, causing the specified command to fail before importing `scripts.verify_translation`.
