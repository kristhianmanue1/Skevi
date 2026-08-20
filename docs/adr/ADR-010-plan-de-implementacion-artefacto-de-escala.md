# ADR-010: El plan de implementación es un artefacto de escala, subordinado a la TAREA

Estado: aceptado; desde ADR-013, crear o extender un plan es disparador de
clase Architectural. No reemplaza ni duplica el contrato de tarea de `04`
§1.

Contexto: la TAREA individual sostiene una tarea, pero cuando el trabajo cruza
múltiples tareas, sesiones o agentes, nada conserva coherencia entre ellas. La
v1 de PROP-004 proponía el plan como artefacto general, sin declarar su
relación con la TAREA — dos documentos con criterios de aceptación paralelos,
el modo de fallo que el estándar §3.5 documenta ("las copias se
desincronizan"), y sin trazabilidad plan↔SPEC análoga al check
CONTRATO↔código de `04` §9 (hallazgos HIGH de la ronda 2026-08-20).

Decisión: `templates/plan-de-implementacion.md` es obligatorio **sólo** a
partir de esa escala; una tarea sola no lleva plan. Cuando existe, la TAREA
lo referencia y el plan es dueño de los criterios (DoD, steps): una sola
fuente. Cada Consumes/Produce resuelve a un CONTRATO/SPEC real o declara
cuál creará; cada step referencia archivo/comando/test real con criterio de
paso — verificación estructural, no de vocabulario. Hogar `docs/plans/`
(03 §2); límite 300 como plantilla derivada (estándar §3.4); al exceder, se
parte en sub-planes vinculados.

Alternativas descartadas:

- **Plan obligatorio para toda tarea**: duplica la TAREA; dos fuentes de
  verdad por tarea.
- **Plan sin verificación estructural** (lista de marcadores prohibidos, v1):
  eludible cambiando palabras en un corpus en español; la ronda midió 21
  ocurrencias de la propia lista dentro de la v1.
- **`plans/` en raíz**: rompe la convención `docs/` por vida útil (ADR-002,
  03 §2).

Consecuencias: la coherencia multi-tarea tiene artefacto y plantilla
canónica; el gate protege la plantilla como archivo requerido. La
generalización (y cualquier gate de planes, A-4) queda condicionada al
piloto — hoy no hay planes reales que verificar, y un gate siempre verde es
el anti-patrón que 03 §3 prohíbe.

Verificación: `python3 scripts/check_sizes.py` → la plantilla cuenta como
requerida y dentro del límite de plantillas.

Procedencia: PROP-004 §2 A-2 (v2), decidida en
`docs/history/PROP-004-decision-2026-08-20.md`; dependencia de A-1 declarada
allí (la clase define cuándo hay plan).
