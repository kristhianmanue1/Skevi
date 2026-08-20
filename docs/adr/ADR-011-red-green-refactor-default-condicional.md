# ADR-011: RED-GREEN-REFACTOR como default condicional de F3

Estado: aceptado; implementa A-3 de PROP-004. Vive en la guía (`04` §3), no
en el estándar §3.2 — la ronda 2026-08-20 bloqueó la rama del estándar por
contradecir el no-objetivo de la propia propuesta y el ítem `pospuesto`
"capa de métodos... separada del estándar atemporal".

Contexto: el estándar §3.2 exige tests con cambios pero no el orden. Si el
ejecutor no vio fallar el test, no sabe si prueba lo correcto. La v1 proponía
la regla como incondicional con exención por `skevi-gate.json` — imposible:
el esquema de configuración es cerrado y el gate comprueba forma y tamaño,
no método (hallazgo HIGH de la ronda). Además exigía como evidencia "se borró
el código prematuro", que ningún comando verifica.

Decisión: en `04` §3, si el proyecto tiene infraestructura de tests, todo
cambio de comportamiento sigue RED-GREEN-REFACTOR: RED (test que falla, por
la razón correcta) → GREEN (código mínimo) → REFACTOR (suite en verde). La
evidencia exigida en el reporte de tarea es la **salida del RED** — que sí
deja registro —, no la declaración de haber borrado código. La regla hereda
la condicionalidad del estándar §3.2 ("Si el proyecto tiene tests...");
crear infraestructura para un cambio acotado es decisión del contrato de
tarea. Excepciones declaradas en la TAREA: throwaway (Spike), código
generado, configuración.

Alternativas descartadas:

- **Regla incondicional (v1)**: insatisfacible en proyectos sin
  infraestructura de tests; BLOQ permanente o incumplimiento silencioso.
- **Exención vía `skevi-gate.json`**: no expresable; `CONFIG_KEYS` es
  cerrado y una clave desconocida falla (ADR-006).
- **Hogar en el estándar §3.2 (v1)**: contradice el no-objetivo de PROP-004
  y el `pospuesto` del manifiesto — el BLOCKER de la ronda.
- **No normar el orden**: el estándar exige el test pero tolera escribirlo
  después, cuando ya no puede fallar por la razón correcta.

Consecuencias: F3 gana un default de método verificable por su evidencia (la
salida del RED). `obra/superpowers` queda clasificado como Referencia que
informa la regla, no evidencia que la demuestra; la justificación doméstica
es que Skevi opera test-first (su gate lleva suite propia desde ADR-006) y
que el piloto Skopos registró el coste de la verificación tardía.

Verificación: `grep -n "RED-GREEN-REFACTOR" docs/ai-agent-guide/04-ejecucion-y-verificacion.md`
→ §3, con la condicionalidad y la evidencia del RED.

Procedencia: PROP-004 §2 A-3 (v2), decidida en
`docs/history/PROP-004-decision-2026-08-20.md`; hallazgos BLOCKER + HIGH ×2
de `docs/history/PROP-004-adversarial-2026-08-20.md` sobre la v1.
