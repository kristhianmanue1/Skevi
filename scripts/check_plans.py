#!/usr/bin/env python3
"""Gate estructural de planes de implementación (A-4 de PROP-004, ADR-014).

Comprueba estructura, no vocabulario: cada tarea con Consumes/Produce/Steps,
cada step con su criterio de verificación, cada ruta backtickada existente.
Las reglas E1-E5 y sus límites declarados viven en
docs/plans/2026-08-20-a4-gate-de-planes.md.

Fail-closed (ADR-006): sin clave `plans` en skevi-gate.json no comprueba
nada — inactivo, nunca error. Copiable sin edición: comparte la
configuración con check_sizes.py mediante la misma clave cerrada.

Uso:
  python3 scripts/check_plans.py            # planes declarados en config
  python3 scripts/check_plans.py FILE...    # archivos explícitos (evidencia)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_NAME = "skevi-gate.json"
EXTENSIONES_CONOCIDAS = {
    ".css", ".glb", ".html", ".js", ".json", ".md", ".py", ".toml",
    ".ts", ".txt", ".yaml", ".yml",
}
TAREA_RE = re.compile(r"^\s*TAREA\s+\S+", re.MULTILINE)
CHECKBOX_RE = re.compile(r"^\s*- \[[ xX]\]")
CAMPO_RE = {
    "Consumes:": re.compile(r"^\s*Consumes:", re.MULTILINE),
    "Produce:": re.compile(r"^\s*Produce:", re.MULTILINE),
    "Steps:": re.compile(r"^\s*Steps:", re.MULTILINE),
}
TOKEN_RE = re.compile(r"`([^`]+)`")


def cargar_config(root: Path) -> dict:
    ruta = root / CONFIG_NAME
    if not ruta.is_file():
        return {}
    data = json.loads(ruta.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{CONFIG_NAME}: la raíz debe ser un objeto")
    desconocidas = sorted(set(data) - _claves_validas())
    if desconocidas:
        raise ValueError(
            f"{CONFIG_NAME}: claves desconocidas: {', '.join(desconocidas)}"
        )
    return data


def _claves_validas() -> set[str]:
    """Las mismas de check_sizes.py más nada: una sola fuente de config."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from check_sizes import CONFIG_KEYS

        return set(CONFIG_KEYS) | {"plans"}
    except ImportError:
        return {"plans"}


def _bloques_tarea(texto: str) -> list[list[str]]:
    lineas = texto.splitlines()
    indices = [i for i, ln in enumerate(lineas) if TAREA_RE.match(ln)]
    bloques = []
    for n, inicio in enumerate(indices):
        fin = indices[n + 1] if n + 1 < len(indices) else len(lineas)
        bloques.append(lineas[inicio:fin])
    return bloques


def _rutas_rotas(linea: str, root: Path) -> list[str]:
    if "crea " in linea:  # creación declarada: no tiene que existir aún
        return []
    rotas = []
    for token in TOKEN_RE.findall(linea):
        if "/" not in token:
            continue
        ruta = Path(token)
        if ruta.suffix.lower() in EXTENSIONES_CONOCIDAS and not (root / ruta).exists():
            rotas.append(token)
    return rotas


def _agrupar_steps(bloque: list[str]) -> list[str]:
    """Cada step = línea checkbox + sus líneas de continuación (más
    indentadas que el guion del checkbox, sin cruzar otro elemento)."""
    steps: list[str] = []
    actual: list[str] = []
    for ln in bloque[1:]:
        if CHECKBOX_RE.match(ln):
            if actual:
                steps.append("\n".join(actual))
            actual = [ln]
        elif actual:
            if TAREA_RE.match(ln):
                break
            indentacion = len(ln) - len(ln.lstrip())
            marcador = len(actual[0]) - len(actual[0].lstrip()) + 2
            if ln.strip() and indentacion >= marcador:
                actual.append(ln)
            else:
                steps.append("\n".join(actual))
                actual = []
        # líneas antes del primer checkbox: no son steps
    if actual:
        steps.append("\n".join(actual))
    return steps


def comprobar_plan(relativo: str, texto: str, root: Path) -> list[str]:
    fallos: list[str] = []
    bloques = _bloques_tarea(texto)
    if not bloques:
        return [f"{relativo}: sin bloques TAREA (regla E1)"]

    for bloque in bloques:
        id_tarea = bloque[0].strip()
        cuerpo = "\n".join(bloque)
        for campo, patron in CAMPO_RE.items():
            if not patron.search(cuerpo):
                fallos.append(f"{relativo}: {id_tarea} sin '{campo}' (regla E2)")
        steps = _agrupar_steps(bloque)
        if not steps:
            fallos.append(
                f"{relativo}: {id_tarea} sin steps con checkbox (regla E3)"
            )
        for step in steps:
            if "verificación" not in step.lower():
                fallos.append(
                    f"{relativo}: {id_tarea}: step sin criterio de "
                    "verificación (regla E4)"
                )
        for ln in bloque:
            if ln.strip().startswith(("Consumes:", "Produce:")):
                for rota in _rutas_rotas(ln, root):
                    fallos.append(
                        f"{relativo}: {id_tarea}: ruta referenciada "
                        f"inexistente: {rota} (regla E5)"
                    )
    return fallos


def planes_declarados(root: Path) -> list[Path] | None:
    """Archivos de planes que el gate debe comprobar, según config.

    None = fail-closed: sin clave `plans` no se comprueba nada.
    Levanta ValueError si la config es inválida (clave desconocida).
    """
    config = cargar_config(root)
    plans_dir = config.get("plans")
    if not isinstance(plans_dir, str) or not plans_dir:
        return None
    directorio = root / plans_dir
    if not directorio.is_dir():
        raise ValueError(f"{CONFIG_NAME}: plans declarado pero el directorio no existe: {plans_dir}")
    archivos = sorted(directorio.glob("*.md"))
    if not archivos:
        raise ValueError(f"{CONFIG_NAME}: plans declarado pero sin planes en {plans_dir}")
    return archivos


def main_para_tests(root: Path, archivos: list[str]) -> list[str]:
    """Núcleo puro para los tests; devuelve la lista de fallos."""
    fallos: list[str] = []
    for archivo in archivos:
        texto = (root / archivo).read_text(encoding="utf-8")
        fallos.extend(comprobar_plan(archivo, texto, root))
    return fallos


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv

    if argv:  # archivos explícitos: evidencia sobre planes de cualquier repo
        root = Path.cwd()
        fallos: list[str] = []
        for arg in argv:
            ruta = Path(arg)
            if not ruta.is_file():
                print(f"BLOQ — no existe: {arg}")
                return 1
            fallos.extend(comprobar_plan(arg, ruta.read_text(encoding="utf-8"), root))
        if fallos:
            print("BLOQ — check_plans encontró incumplimientos")
            for fallo in fallos:
                print(f"- {fallo}")
            return 1
        print(f"OK — {len(argv)} plan(es) verificados (estructura E1-E5)")
        return 0

    try:
        archivos = planes_declarados(ROOT)
    except (ValueError, OSError) as exc:
        print("BLOQ — check_plans no pudo leer la configuración del proyecto")
        print(f"- {exc}")
        return 1

    if archivos is None:
        print("OK — sin planes declarados (fail-closed: clave 'plans' ausente)")
        return 0

    fallos = []
    for ruta in archivos:
        fallos.extend(
            comprobar_plan(
                ruta.relative_to(ROOT).as_posix(),
                ruta.read_text(encoding="utf-8"),
                ROOT,
            )
        )
    if fallos:
        print("BLOQ — check_plans encontró incumplimientos")
        for fallo in fallos:
            print(f"- {fallo}")
        return 1

    print(f"OK — {len(archivos)} plan(es) verificados (estructura E1-E5)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
