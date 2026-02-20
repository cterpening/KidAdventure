#!/usr/bin/env python3
"""Lightweight lint/smoke checks for the static KidAdventure project."""

from __future__ import annotations

from pathlib import Path
import re
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = REPO_ROOT / "index.html"
README_MD = REPO_ROOT / "README.md"
ASSETS_README_MD = REPO_ROOT / "assets" / "README.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_asset_paths(index_html: str) -> list[str]:
    return sorted(set(re.findall(r'"(assets/[^"]+)"', index_html)))


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    index_text = read_text(INDEX_HTML)
    readme_text = read_text(README_MD)
    assets_readme_text = read_text(ASSETS_README_MD)

    if re.search(r"^(<<<<<<<|=======|>>>>>>>)", index_text, re.MULTILINE):
        errors.append("index.html contains unresolved merge markers.")

    if index_text.count("<script>") != 1 or index_text.count("</script>") != 1:
        errors.append("index.html should contain exactly one inline <script> block.")

    if "const W = 960, H = 600;" not in index_text:
        warnings.append("Expected canvas dimensions constant was not found.")

    if "## How to Play" not in readme_text:
        warnings.append("README.md is missing the expected How to Play section.")

    if "Update `ASSET_CONFIG` in `index.html`" not in assets_readme_text:
        warnings.append("assets/README.md may be missing ASSET_CONFIG guidance.")

    asset_paths = extract_asset_paths(index_text)
    for rel_path in asset_paths:
        full_path = REPO_ROOT / rel_path
        if not full_path.exists():
            errors.append(f"Missing asset referenced in index.html: {rel_path}")

    if errors:
        print("FAIL: QA checks found issues:")
        for issue in errors:
            print(f"- {issue}")
        if warnings:
            print("\nWARNINGS:")
            for issue in warnings:
                print(f"- {issue}")
        return 1

    print("PASS: QA checks completed successfully.")
    if warnings:
        print("WARNINGS:")
        for issue in warnings:
            print(f"- {issue}")
    else:
        print("No warnings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
