# Piloto: plan de implementación (ADR-010) y clase Architectural sobre trabajo multi-tarea

> Segundo piloto de PROP-004 sobre `orbitaNova`: estrena A-2 (plan de
> implementación) con la tarea del issue #4 → PR #11 (squash `0427cda`),
> ejecutada como PLAN-0002 en el propio repo adoptante. Documento de
> evidencia, no norma: si algo aquí contradice el estándar o la guía
> vigentes, ganan ellos (`AGENTS.md` §Prioridad).

## F0 — Clasificación

Tarea: resolver el issue #4 — `AGENTS.md` sólo contenía el bloque gestionado
de AN-KLA; sin comandos, convenciones ni prohibiciones para agentes.

Trabajo multi-tarea (test ancla + contenido documental) → plan de
implementación (ADR-010) en el hogar declarado por el adoptante:
`docs/proposals/` (precedente PLAN-0001), equivalente local de `docs/plans/`.

**Clase: Architectural.** Duda declarada en la TAREA antes de empezar (PF-2):
bajo el corte observable de ADR-012, un plan `.md` nuevo es "producción" →
ante duda, clase superior. Primera vez que esta clase se ejercita.

### PF-2 — Hallazgo de método

Si los archivos de plan cuentan como producción (ADR-012), **toda** tarea
multi-tarea escala a Architectural — la combinación "plan + Bounded" no
existe. ¿Es un defecto o es correcto?

La evidencia de este piloto dice que es correcta y coherente, con una
precisión: un plan multi-tarea exige F0 completo de §7, pero no lo agota —
REQ-* y no-objetivos vivieron cómodamente dentro del plan; las preguntas
cerradas y los EV-* vivieron fuera (en el registro). Lo obligatorio es §7
completo, no su ubicación dentro del plan. La resolución no es eximir los
planes como los tests (abriría la evasión de esconder producción bajo
"gestión"), sino **hacer explícito el disparador**: crear **o extender** un
plan de implementación es trabajo Architectural (ADR-013).

## F3 — Ejecución

- **TAREA t1 (RED):** `tests/agents-md.test.js` antes del contenido. Tres
  fallos por la razón correcta: «AGENTS.md no declara la sección de comandos
  de verificación», «la sección no documenta comandos npm: 0 ≥ 4», «falta la
  sección Convenciones». El cuarto test pasaba de base: el bloque gestionado
  ya existía — REQ-3 se cumple por preservación, no por creación.
- **TAREA t2 (GREEN):** AGENTS.md documentado (comandos anclados a
  `package.json`, convenciones con ADRs locales citados, prohibiciones);
  bloque gestionado **byte-idéntico** a `main` (diff vacío; mismo sha256 que
  el `content_sha256` del marcador).
- **Ancla de REQ-3:** golden fixture del bloque gestionado — el test compara
  contenido exacto, no sólo marcadores. Si AN-KLA regenera el bloque de
  forma legítima, el fixture se actualiza de forma consciente, nunca en
  silencio.

### Ronda adversarial

Contexto fresco obligatorio (disparador 4: AGENTS.md es interfaz consumida
por agentes no controlados). Decisión: `fix-and-retry` → 1 HIGH + 2 MED +
5 LOW, los ocho corregidos en la misma rama. Los más relevantes para el
método: el ancla de REQ-3 contaba marcadores sin proteger contenido (HIGH →
golden fixture); el DoD del plan citaba una cifra de tests no verificada
(MED → evidencia real pegada); el RED no estaba transcrito en ningún
artefacto inspeccionable (MED → transcripción en el plan). Lección: un DoD
con cifras se escribe **después** de correr, y el RED se pega donde el plan
viva, no sólo en la conversación.

## Evidencia

```text
EV-1  npx vitest run tests/agents-md.test.js (antes del contenido) →
      3 failed / 1 passed, mensajes citados arriba [pass: RED por la razón correcta]
EV-2  npm test → 45/45 (7 archivos; base del repo: 41/5) [pass]
EV-3  npm run lint → exit 0; npm run check:sizes → OK 98 archivos [pass]
EV-4  diff del bloque gestionado vs main @ 5287053 → vacío [pass: REQ-3]
EV-5  gh pr merge 11 --squash → MERGED 0427cda; issue #4 → CLOSED [pass]
EV-6  post-merge: npm test 45/45; check:sizes OK; árboles idénticos eebbb9b [pass]
```

CI de orbitaNova: sin iniciar por facturación de la cuenta (mismo patrón que
el piloto 1); excepción documentada como comentario en el PR #11 antes del
merge, con evidencia local equivalente.

## Qué validó este piloto y qué no

| Validó | No validó |
|---|---|
| A-2/ADR-010: plan con F0, tareas con Consumes/Produces reales, DoD con evidencia, hogar declarado por el adoptante | §7 completo dentro del plan: REQ y no-objetivos sí; preguntas cerradas y EV-* vivieron fuera — válidos, pero el plan solo no agota §7 |
| Clase Architectural por primera vez — F0 de §7 exigido y cubierto entre plan y registro | La partición de planes que excedan el límite (el plan tuvo 2 tareas) |
| La TAREA referenció el plan y el plan fue dueño de los criterios (una sola fuente) | Contratos completos de t1/t2 (Clase/Base/Permitido/Prohibido/Parada) transcritos en el registro: abajo — vivieron en la conversación, no en el plan; los planes futuros deberían llevarlos |
| El hogar del plan es configurable por el adoptante (`docs/proposals/` ≠ `docs/plans/`) | Spike y ratchet: siguen sin ejercitarse |
| PF-2, resuelto como ADR-013 (crear **o extender** un plan escala; los planes previos no se reclasifican) | A-4 en ejecución: existe un plan real con evidencia (PLAN-0002) — **la condición de reactivación quedó cumplida**; evaluarla es trabajo aparte |

### Contratos de las tareas (transcritos; vivieron en la conversación)

```text
TAREA on4-agentmd-t1 + on4-agentmd-t2 (multi-tarea → PLAN-0002)
Objetivo: resolver issue #4 — AGENTS.md sin comandos ni convenciones — estrenando A-2/ADR-010
Clase: Architectural (duda PF-2 declarada → clase superior)
Base: main @ 5287053, árbol limpio
Permitido: AGENTS.md, tests/, docs/proposals/PLAN-0002, rama local
Prohibido: AN-KLA.md, bloque an-kla:managed, src/, deps, CI, push/merge
DoD: RED capturado antes del contenido; suite+lint+gate OK; bloque managed byte-intacto; ronda adversarial
Parada: issue #4 con sus 4 checkboxes cubiertos
```

### Erratas del artefacto piloto

PLAN-0002 (mergeado en orbitaNova) cita "check:sizes → OK **97** archivos"
en su DoD — cifra del estado previo al golden fixture; el estado final es
**98**. Y la base del repo era 41 tests en **6** archivos (este registro
citó 5 en su primera redacción). Ambas corregidas aquí; PLAN-0002 queda como
está (errata menor, ya fusionada).

## Consecuencias para Skevi

- ADR-013: crear un plan de implementación es disparador de Architectural
  (este cambio). `01` §2 fila Architectural actualizada.
- `project-manifest.yaml`: el piloto multi-tarea corrió; la evaluación de A-4
  queda habilitada y pendiente de ejecutar.
- Siguiente sesión sugerida: evaluar A-4 (chequeo estructural de planes sobre
  PLAN-0001/PLAN-0002 reales), o el piloto F0→F3 sobre proyecto nuevo
  (requisito Alpha→estable).

## Procedencia

- PROP-004 (v2); ADR-009/010/011/012. Registro del piloto 1:
  `piloto-orbitanova.md`.
- Evidencia completa: orbitaNova PR #11 (commits 7182ecc, 8b093f6; squash
  0427cda), issue #4, PLAN-0002 en el repo adoptante.
- Memoria an-kla de skevi y orbitaNova: checkpoint y facts de ambos pilotos.
