from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def test_required_portfolio_files_exist():
    required = [
        "index.html", "README.md", "LICENSE", "CITATION.cff", "references.bib",
        "assets/styles.css", "assets/app.js", "assets/logo.svg", "assets/architecture.svg",
        "data/baseline.json", "data/sites.json", "data/sources.json",
        "docs/METHODOLOGY.md", "docs/ORIGIN.md", "docs/SCIENTIFIC_AUDIT.md",
        "docs/DATA_SOURCES.md", "docs/VALIDATION.md", "docs/INTERVIEW_CHEATSHEET.md",
        ".github/workflows/ci.yml",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_sources_have_traceability_fields():
    sources = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))
    assert len(sources) >= 9
    for source in sources:
        for key in ["id", "title", "organization", "year", "url", "use", "use_es", "quality", "variables", "used_in", "confidence", "accessed", "date_basis"]:
            assert source.get(key), (source.get("id"), key)


def test_no_raw_markdown_links_are_used_as_primary_navigation():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'href="docs/METHODOLOGY.md"' not in html
    assert 'href="docs/ORIGIN.md"' not in html
    assert 'href="#methodology"' in html
    assert 'href="#origin"' in html


def test_app_has_no_external_runtime_dependency():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "cdn.jsdelivr" not in html
    assert "unpkg.com" not in html
    assert "cdnjs.cloudflare" not in html
