# Índice de decisiones arquitectónicas (ADR)

| ADR | Título | Estado | Implementación | Origen | Fecha |
|---|---|---|---|---|---|
| ADR-001 | Gate local sin CI remoto | Aceptado | `scripts/hooks/pre-push` | Fundacional | 2026-08-12 |
| ADR-002 | Separación de docs por vida útil | Aceptado | Estructura de `docs/` | Fundacional | 2026-08-12 |
| ADR-003 | Directorios canónicos en inglés | Aceptado | Estructura de `docs/` | Instrucción directa | 2026-08-14 |
| ADR-004 | Graduar fail-closed por clase de operación | Aceptado | `f46dcca` | PROP-003 §3.1 | 2026-08-17 |
| ADR-005 | Resultado por línea de evidencia | Aceptado | `f46dcca` | PROP-003 §3.2 | 2026-08-17 |
| ADR-006 | Gate configurable por proyecto adoptante | Aceptado | `scripts/check_sizes.py` | PROP-002 §A-6 | 2026-08-15 |
| ADR-007 | Validar en la frontera implica fallar controlado | Aceptado | `estandar-diseno-software-github.md` §2.4 | `an-kla-memory` #84 | 2026-08-16 |
| ADR-008 | Disparadores objetivos de rigor | Aceptado | `AGENTS.md`, `04-ejecucion-y-verificacion.md` | PROP-002 §A-8 | 2026-08-15 |

**Reglas de este índice**

- Estado: solo `Aceptado` figura aquí; rechazados, diferidos o sustituidos se
  registran en el ADR que los reemplaza o en `docs/history/`.
- Implementación: commit, archivo o sección donde la decisión se materializó.
- Origen: si procede de una propuesta, se vincula; si es fundacional o externa,
  se declara como tal.
- Fecha: del commit o decisión que originó el ADR, no de la última edición.
