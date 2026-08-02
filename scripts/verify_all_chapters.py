#!/usr/bin/env python3
"""Run verify_chapter on ALL 25 chapter pairs and produce a summary report."""
import argparse, json, os, sys
from pathlib import Path

# Ensure script directory is on path so we can import both modules
sys.path.insert(0, str(Path(__file__).resolve().parent))

from verify_translation import verify_chapter, _with_metadata, map_files
from verify_translation import Finding
from translation_rules import discover_chapter_pairs, CHAPTER_MAP


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run translation QA on all 25 chapters")
    parser.add_argument("--report-dir", type=Path, default=Path("/tmp/translation-qa"))
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)

    args.report_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(args.repo_root)

    pairs = discover_chapter_pairs(args.repo_root)

    all_findings = []
    chapter_reports = {}

    for en_path, zh_path in pairs:
        ch_name = zh_path.name
        try:
            report = verify_chapter(en_path, zh_path, strict=args.strict)
            chapter_reports[ch_name] = report
            all_findings.extend(report.get("findings", []))
        except Exception as exc:
            chapter_reports[ch_name] = {"status": "ERROR", "error": str(exc)}
            print(f"  {ch_name}: ERROR — {exc}", file=sys.stderr)

    # Summarize
    severity_counts = {"P0": 0, "P1": 0, "P2": 0}
    for f in all_findings:
        sev = f.get("severity", "P2")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    pass_count = sum(1 for r in chapter_reports.values() if r.get("status") == "PASS")
    fail_count = sum(1 for r in chapter_reports.values() if r.get("status") == "FAIL")
    err_count = sum(1 for r in chapter_reports.values() if r.get("status") == "ERROR")

    summary = {
        "chapters_total": len(pairs),
        "chapters_pass": pass_count,
        "chapters_fail": fail_count,
        "chapters_error": err_count,
        "total_findings": len(all_findings),
        "by_severity": severity_counts,
        "chapter_reports": {
            ch: {"status": r["status"],
                 "findings": len(r.get("findings", [])),
                 "metrics": r.get("metrics", {})}
            for ch, r in sorted(chapter_reports.items())
        },
    }

    # Write summary
    summary_path = args.report_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    # Write detailed findings per chapter (only if findings exist)
    for ch_name, report in chapter_reports.items():
        findings = report.get("findings", [])
        if not findings:
            continue
        ch_report = args.report_dir / f"{ch_name}.json"
        ch_report.write_text(json.dumps(
            _with_metadata(report, ch_name),
            ensure_ascii=False, indent=2
        ), encoding="utf-8")

    # Print summary
    print(f"\n{'='*55}")
    print(f"Translation QA — 25 Chapters Summary")
    print(f"{'='*55}")
    print(f"  Pass: {pass_count}  Fail: {fail_count}  Error: {err_count}")
    print(f"  Findings: P0={severity_counts.get('P0',0)}  "
          f"P1={severity_counts.get('P1',0)}  P2={severity_counts.get('P2',0)}")
    print(f"  Report: {args.report_dir}/summary.json")

    # Exit code: blocked by P0 or P1 findings
    blocked_by = severity_counts.get("P0", 0) + severity_counts.get("P1", 0)
    return 1 if blocked_by > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
