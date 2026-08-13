#!/usr/bin/env python3
"""Gate de estructura y tamaños de Skevi.

La polaridad es cerrada: todo archivo de texto queda sujeto a un límite salvo
una exención explícita. También falla si falta un archivo canónico o aparece
Markdown operativo suelto en la raíz.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ROOT_MARKDOWN = {"AGENTS.md", "CLAUDE.md", "README.md"}
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
    "plantillas/registro-contexto.md",
    "plantillas/skevi/usage-guide.md",
    "plantillas/skevi/architecture-overview.md",
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
TEMPLATE_PREFIX = "plantillas/"
TEMPLATE_LIMIT = 300


def limit_for(name: str) -> int:
    if name in LIMITS:
        return LIMITS[name]
    if name.startswith(TEMPLATE_PREFIX):
        return TEMPLATE_LIMIT
    return DEFAULT_LIMIT


REGISTRY_START_RE = re.compile(r"^<!--\s*skevi:registry:start\s*-->$", re.IGNORECASE)
REGISTRY_END_RE = re.compile(r"^<!--\s*skevi:registry:end\s*-->$", re.IGNORECASE)
REGISTRY_HOSTS = {"AGENTS.md", "CLAUDE.md"}


def _resolve_registry_path(value: str) -> Path | None:
    """Resuelve `value` contra ROOT; None si es absoluta o escapa de ROOT."""
    if value.startswith("/") or value.startswith("~"):
        return None
    candidate = (ROOT / value).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


def check_registry_block(relative: Path, text: str) -> list[str]:
    """Valida el bloque delimitado de §3.5 si el archivo lo trae."""
    if relative.name not in REGISTRY_HOSTS:
        return []

    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if REGISTRY_START_RE.match(line.strip())]
    ends = [i for i, line in enumerate(lines) if REGISTRY_END_RE.match(line.strip())]

    if not starts and not ends:
        return []
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        return [f"{relative}: bloque skevi:registry con delimitadores desbalanceados"]

    failures: list[str] = []
    raw_body = [line.strip() for line in lines[starts[0] + 1 : ends[0]] if line.strip()]
    body = [line for line in raw_body if not line.startswith((";", "#"))]

    if not body or body[0] != "[skevi]":
        failures.append(f"{relative}: bloque skevi:registry sin sección [skevi]")
        entries = body
    else:
        entries = body[1:]
        if any(line == "[skevi]" for line in entries):
            failures.append(f"{relative}: bloque skevi:registry con sección [skevi] duplicada")
            entries = [line for line in entries if line != "[skevi]"]

    if not entries:
        failures.append(f"{relative}: bloque skevi:registry sin entradas")

    for line in entries:
        if "=" not in line:
            failures.append(f"{relative}: línea de registro inválida: {line!r}")
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if not key or not value:
            failures.append(f"{relative}: línea de registro inválida: {line!r}")
            continue
        target = _resolve_registry_path(value)
        if target is None:
            failures.append(
                f"{relative}: skevi:registry.{key} usa ruta fuera de la raíz del "
                f"proyecto: {value}"
            )
        elif not target.is_file():
            failures.append(
                f"{relative}: skevi:registry.{key} apunta a ruta inexistente: {value}"
            )
    return failures


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
        limit = limit_for(name)
        rows.append((name, observed, limit))
        if observed > limit:
            failures.append(f"{name}: {observed} líneas > límite {limit}")
        if relative.name in REGISTRY_HOSTS:
            text = (ROOT / relative).read_text(encoding="utf-8")
            failures.extend(check_registry_block(relative, text))

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
