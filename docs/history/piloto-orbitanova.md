# Piloto: clasificación de tarea (ADR-009) y TDD (ADR-011) sobre un repo existente

> Primer piloto de PROP-004 sobre un proyecto real en marcha:
> `orbitaNova` (github.com/kristhianmanue1/orbitaNova), sistema solar 3D en
> Three.js, adoptante del gate desde su ADR local 0006. Documento de
> evidencia, no norma: si algo aquí contradice el estándar o la guía
> vigentes, ganan ellos (`AGENTS.md` §Prioridad).
> Cubre A-1 (clasificación) y A-3 (TDD) sobre una tarea única Bounded.
> **A-2 (plan) no fue ejercitado**: la tarea era sola; el plan existe sólo a
> partir de trabajo multi-tarea (ADR-010).

## F0 — Clasificación

Tarea: resolver el issue #3 de orbitaNova — el README contradecía el conteo
de asteroides (línea 23: "800"; línea 134: "500").

REQ cubierto (preservado aquí porque la spec de Bounded vivía en el PR, ya
mergeado y su rama borrada):

```text
REQ-1 [funcional] [fuente: issue #3 de orbitaNova]
Enunciado: el README no se contradice sobre el conteo de asteroides y
refleja el count real del código.
Criterio de aceptación: tests/docs-consistency.test.js en verde (ancla
README ↔ Belts.js, cuerpo de createInstancedAsteroidBelt).
Prioridad: imprescindible
```

Contrato de tarea fijado antes de tocar nada, con la clase derivada de los
disparadores observables de `01` §2:

| Disparador Bounded | Verificado en disco |
|---|---|
| Toca sólo archivos existentes | ✗ bajo lectura literal de entonces (el test era archivo nuevo) → Bounded bajo la lectura PF-1, normada después como ADR-012 |
| Sin dependencias nuevas | package.json fuera de alcance ✓ |
| Sin interfaz pública ni contrato nuevos | sólo README + test ✓ |
| No activa `04` §5.3 | sin persistencia de terceros, sin LLM, sin concurrencia — 0/4 en la práctica; nota honesta: el README de un repo público es interfaz hacia lectores no controlados, y aun así se corrió la ronda de contexto fresco como compensación |

Clase: **Bounded**. El repo target ya habla el idioma del método (ADRs
propios, gate skevi-gate.json, Vitest): fricción mínima, foco en lo que se
estrena.

### PF-1 — Hallazgo de método (el resultado más valioso del piloto)

El disparador 1 de Bounded ("toca sólo **archivos** existentes en disco")
leído literal clasifica como Architectural **cualquier corrección de bug con
test de regresión**, porque todo test nuevo es un archivo nuevo. Eso
contradice el estándar §3.2, que exige test con cada cambio de comportamiento:
bajo la lectura literal, cumplir §3.2 siempre escala la clase — el disparador
pelea contra la norma que debería servir.

Lectura adoptada durante el piloto (registrada en la TAREA antes de editar):
"archivos de **producción** existentes; los archivos de **test** nuevos no
escalan la clase". Esta lectura se normó como ADR-012 y quedó en `01` §2 en
el mismo cambio que este registro.

## F3 — Ejecución (TDD)

1. **RED:** `tests/docs-consistency.test.js` escrito primero. Salida
   capturada antes del fix: `AssertionError: el README se contradice: 800 vs
   500: expected 2 to be 1` — falla por la razón correcta (la contradicción,
   no un error de montaje). El test ancla el README al cuerpo de
   `createInstancedAsteroidBelt` en `Belts.js`.
2. **GREEN:** fix de una línea — `README.md:134` "500 asteroides" → "800
   asteroides". El valor correcto es el del código: `Belts.js:15`
   `count: 800`.
3. **REFACTOR/REVISIÓN:** ronda adversarial con contexto fresco (subagente,
   sesión nueva) aunque §5.3 no la exigía — compensación declarada por la
   duda de clasificación PF-1.

### Ronda adversarial

Decisión: `proceed`. Hallazgos: 1 MED + 5 LOW.

- **[MED] El ancla tomaba el primer `count:` del archivo** — podía desviarse
  al cinturón de Kuiper, a un comentario o a un string si Belts.js se
  reordenaba. Corregido: el test recorta el cuerpo de la función antes de
  extraer el literal.
- **[LOW ×4]** separadores de miles ("1.800" matcheaba "800"); umbral de
  menciones congelaba la maquetación del README; fallo ilegible si el ancla
  dejaba de resolver; DoD del issue pedía citar la fuente en el PR. Los
  cuatro corregidos o cubiertos en el PR.
- **[LOW] Fuera de alcance anotado:** el cinturón de Kuiper (otros 800
  asteroides) no está documentado en el README — backlog de orbitaNova.

## Evidencia

```text
EV-1  npx vitest run tests/docs-consistency.test.js (antes del fix) →
      1 failed: "el README se contradice: 800 vs 500" [pass: RED por la razón correcta]
EV-2  npx vitest run tests/docs-consistency.test.js (después del fix) → 1 passed [pass]
EV-3  npm test → 41/41 (6 archivos; antes del cambio: 40/5) [pass]
EV-4  npm run lint → limpio [pass]
EV-5  python3 scripts/check_sizes.py (orbitaNova) → OK, 95 archivos [pass]
EV-6  gh pr merge 10 --squash → MERGED 5287053; issue #3 → CLOSED [pass]
EV-7  git pull --ff-only; npm test post-merge → 41/41; check_sizes OK [pass]
```

### Excepción documentada: CI sin correr

El workflow de orbitaNova nunca inició sus jobs (4s, run 32396303373):
"The job was not started because recent account payments have failed". Merge
autorizado por el maintainer con evidencia local equivalente corrida dos
veces (commits 476fe9c y a55d215) y la excepción registrada como comentario
en el PR #10. Mismo patrón que motivó ADR-001 en Skevi: la limitante es de
la cuenta, no del cambio.

## Qué validó este piloto y qué no

| Validó | No validó |
|---|---|
| ADR-009 aplicado a un repo existente real, no al laboratorio | A-2 / ADR-010: tarea única, sin plan |
| La clasificación obligó a verificar disparadores **antes** de tocar nada — la verdad del conteo se buscó en `Belts.js:15`, no en el issue | Clases Spike y Architectural: no se ejercitaron |
| ADR-011 con RED capturado por la razón correcta y ancla de regresión permanente | Ratchet: no hubo reclasificación a mitad de tarea |
| Ronda adversarial como compensación honesta ante duda de clasificación | El piloto F0→F3 completo sobre proyecto nuevo que exige el README para salir de Alpha |
| PF-1: un defecto real del método, encontrado en cancha y normado | Generalización: N=1, proyecto del propio maintainer — evidencia de un caso, no promesa |

## Consecuencias para Skevi

- `01` §2 refina el disparador 1 con la lectura de PF-1 (este cambio).
- `project-manifest.yaml` `pospuesto` actualizado: la clasificación corrió
  sobre un proyecto real; A-4 sigue diferida hasta un piloto con planes
  reales (multi-tarea).
- Siguiente piloto sugerido: tarea **multi-tarea** en orbitaNova (candidatos:
  issue #4 — AGENTS.md sin comandos — o documentar el cinturón de Kuiper)
  para estrenar A-2 y habilitar la evaluación de A-4.

## Procedencia

- PROP-004 (v2), decisión 2026-08-20; ADR-009/010/011.
- Evidencia completa: PR #10 de orbitaNova (commits 476fe9c, a55d215;
  squash 5287053), issue #3, run de CI 32396303373.
- Memoria an-kla de skevi: checkpoint + fact `f-piloto-orbitanova-2026-08-20`.
