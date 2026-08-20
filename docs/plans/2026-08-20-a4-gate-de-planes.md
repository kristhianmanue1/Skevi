# PLAN 2026-08-20 — Gate de planes (A-4): evaluación e implementación v1 mínima

> **Tipo:** plan de implementación multi-tarea (ADR-010; clase Architectural
> por ADR-013 — este plan es el disparador). **Autoriza:** decisión PROP-004
> §A-4 con condición cumplida (PLAN-0002 de orbitaNova, PR #11).
> **Estado:** en ejecución · **Fecha:** 2026-08-20 · **Base:** `main` @ `73f603d`

## F0 — Requisitos y no-objetivos

```text
REQ-1 [funcional] [fuente: PROP-004 decisión §2]
Enunciado: un verificador local comprueba estructura de planes — cada step
con criterio de verificación, cada tarea con Consumes/Produces/Steps, cada
ruta referenciada existente.
Criterio: scripts/check_plans.py sobre un plan válido → exit 0; sobre
planes rotos (fixture) → exit ≠ 0 enumerando cada fallo.
Prioridad: imprescindible

REQ-2 [restricción] [fuente: PROP-004 decisión §2 — "no listas léxicas"]
Enunciado: el chequeo es estructural; cero detección por vocabulario.
Criterio: un plan sin TBD/TODO pero sin Steps falla; uno con "pendiente de
definir" en prosa legítima no falla por eso.
Prioridad: imprescindible

REQ-3 [restricción] [fuente: ADR-006 — polaridad cerrada del gate]
Enunciado: sin configuración declarada, no se comprueba nada (fail-closed:
ausencia = inactivo, nunca error); skevi lo activa para docs/plans/.
Criterio: sin skevi-gate.json, check_plans → "OK — sin planes declarados";
con plans activo y plan roto → BLOQ.
Prioridad: imprescindible

REQ-4 [funcional] [fuente: piloto — evidencia doméstica]
Enunciado: el verificador corre sobre los dos planes reales existentes:
este mismo, y PLAN-0002 de orbitaNova (evidencia del piloto).
Criterio: ambos en exit 0; transcripción en el registro de la tarea.
Prioridad: imprescindible
```

**No-objetivos:** no se instalan hooks en orbitaNova (sólo se corre como
evidencia); no se valida semántica de steps (sólo estructura y resolución de
rutas); no hay CI nueva (ADR-001); no se comprueban planes de proyectos sin
configurar.

## Tareas

```text
TAREA a4-t1
  Consumes: REQ-1/2/3; skevi-gate.json (clave nueva `plans`, ADR-006)
  Produce: tests/test_check_plans.py — ancla de regresión (RED primero)
  Steps:
  - [x] Tests de estructura válida e inválida antes del script —
        verificación: `python3 -m unittest tests.test_check_plans` en rojo
        (ModuleNotFoundError: check_plans)
TAREA a4-t2
  Consumes: REQ-1/2/3; salida de t1 (tests en rojo)
  Produce: scripts/check_plans.py (Python estándar, copiable, config compartida
        con check_sizes vía skevi-gate.json clave `plans`)
  Steps:
  - [x] Implementar parser y cinco reglas — verificación: suite nueva en
        verde; suite existente (39) sin cambios
  - [x] skevi-gate.json de skevi con plans activo — verificación: correr
        ambos gates sobre el repo → OK
TAREA a4-t3
  Consumes: REQ-4; este plan (docs/plans/2026-08-20-a4-gate-de-planes.md)
  Produce: corrida de evidencia sobre los dos planes reales + ADR-014 +
        manifiesto/índice/README/AGENTS actualizados
  Steps:
  - [x] Correr el verificador sobre este plan y sobre PLAN-0002 de
        orbitaNova — verificación: transcripción de ambas salidas (abajo)
  - [ ] Ronda adversarial con contexto fresco — verificación: reporte con
        decisión proceed o hallazgos corregidos
```

## Evidencia de ejecución (transcripción)

```text
EV-t1  python3 -m unittest tests.test_check_plans (antes del script) →
      Ran 11 tests — FAILED (errors=11): ModuleNotFoundError: No module
      named 'check_plans' [pass: RED por la razón prescrita]
EV-t2  python3 -m unittest discover -s tests → Ran 51 tests — OK
      (12 nuevas + 39 existentes) [pass]
EV-t3  python3 scripts/check_sizes.py → OK — 59 archivos [pass]
EV-t4  python3 scripts/check_plans.py →
      "BLOQ — step sin criterio de verificación (E4)" ×2 — hallazgo real
      del gate sobre ESTE plan: steps multilínea con «verificación:» en
      línea de continuación; parser corregido para agrupar steps →
      "OK — 1 plan(es) verificados (estructura E1-E5)" [pass: dogfooding]
EV-t5  python3 scripts/check_plans.py /Users/krisnova/www/orbitaNova/
      docs/proposals/PLAN-0002-agentmd-comandos.md → sin fallos (exit 0
      junto a PLAN-0001 en la misma corrida) [pass]
EV-t6  ídem con PLAN-0001-modo-dino-fps.md → "BLOQ — sin bloques TAREA
      (regla E1)" — correcto y honesto: es un plan técnico de deliberación,
      otro género; el gate estructura planes ejecutables (ADR-010) [pass]
```

**DoD del plan:** suites en verde (nueva + 39 existentes); ambos gates OK;
evidencia REQ-4 transcrita; ADR-014 con procedencia; ronda adversarial.

## Diseño v1 — qué comprueba y qué no (honesto)

| Regla | Qué comprueba | Qué NO comprueba (declarado) |
|---|---|---|
| E1 | ≥1 bloque `TAREA <id>` | Que las tareas sean las correctas |
| E2 | cada TAREA con `Consumes:`, `Produce:`, `Steps:` | Que Consumes apunten al artefacto *adecuado* |
| E3 | cada TAREA ≥1 checkbox (`- [ ]`/`- [x]`) | Que los steps estén *hechos* de verdad |
| E4 | cada step con `— verificación:` | Que el criterio de verificación *sea* verificable |
| E5 | cada token con ruta y extensión en backticks, existente en el repo (salvo línea con "crea ") | Rutas sin backticks, extensiones desconocidas, semántica |

**Regla E5 acotada y declarada:** sólo tokens backtickados con `/` y
extensión conocida — "REQ-1/2/3" o "0002/0003/0006" no matchean (sin
extensión). Es un ancla, no un notario: el límite está declarado aquí para
que nadie confunda cobertura con cumplimiento.

## Procedencia

PROP-004 decisión §A-4 (condición cumplida 2026-08-20: PLAN-0002 ejecutado,
PR #11 de orbitaNova); rondas adversariales de PROP-004 (la primera midió el
gate vacuo y las listas léxicas eludibles); ADR-006 (config compartida);
ADR-010/013 (este plan y su clase).
