#!/usr/bin/env python3
"""Gate de estructura y tamaños de Skevi.

La polaridad es cerrada: todo archivo de texto queda sujeto a un límite salvo
una exención explícita. También falla si falta un archivo canónico o aparece
Markdown operativo suelto en la raíz.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ROOT_MARKDOWN = {"AGENTS.md", "README.md"}
REQUIRED = {
    "AGENTS.md",
    "README.md",
    "docs/estandar-diseno-software-github.md",
    "docs/guia-agentes-ia/00-INDICE.md",
    "docs/guia-agentes-ia/01-analisis-y-requerimientos.md",
    "docs/guia-agentes-ia/02-specs-adr-contratos.md",
    "docs/guia-agentes-ia/03-cascaron-proyecto.md",
    "docs/guia-agentes-ia/04-ejecucion-y-verificacion.md",
    "scripts/check_sizes.py",
}
SKIP_DIRS = {
    ".an-kla",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "data",
    "datos",
    "dist",
    "generated",
    "node_modules",
    "vendor",
}
EXEMPT_SUFFIXES = {
    ".gif",
    ".gz",
    ".ico",
    ".jpeg",
    ".jpg",
    ".lock",
    ".pdf",
    ".png",
    ".pyc",
    ".svg",
    ".tar",
    ".woff",
    ".woff2",
    ".zip",
}
EXEMPT_PATHS: set[str] = set()
LIMITS = {
    "AGENTS.md": 200,
    "README.md": 300,
}
DEFAULT_LIMIT = 800


def discover() -> list[Path]:
    paths: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in relative.parts[:-1]):
            continue
        paths.append(relative)
    return sorted(paths)


def count_text_lines(relative: Path) -> int | None:
    if relative.as_posix() in EXEMPT_PATHS:
        return None
    if relative.suffix.lower() in EXEMPT_SUFFIXES:
        return None
    try:
        text = (ROOT / relative).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    return len(text.splitlines())


def main() -> int:
    failures: list[str] = []

    for relative in sorted(REQUIRED):
        if not (ROOT / relative).is_file():
            failures.append(f"falta archivo requerido: {relative}")

    unexpected_markdown = sorted(
        path.name
        for path in ROOT.glob("*.md")
        if path.name not in ROOT_MARKDOWN
    )
    if unexpected_markdown:
        failures.append(
            "Markdown operativo suelto en raíz: " + ", ".join(unexpected_markdown)
        )

    rows: list[tuple[str, int, int]] = []
    for relative in discover():
        observed = count_text_lines(relative)
        if observed is None:
            continue
        name = relative.as_posix()
        limit = LIMITS.get(name, DEFAULT_LIMIT)
        rows.append((name, observed, limit))
        if observed > limit:
            failures.append(f"{name}: {observed} líneas > límite {limit}")

    if failures:
        print("BLOQ — check_sizes encontró incumplimientos")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "OK — "
        f"{len(rows)} archivos de texto dentro de límites; "
        "estructura y hogares canónicos verificados"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
