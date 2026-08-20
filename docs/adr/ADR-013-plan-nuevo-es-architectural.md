# ADR-013: Crear un plan de implementación es disparador de Architectural

Estado: aceptado; cierra el hallazgo PF-2 del segundo piloto. Complementa a
ADR-010 (el plan como artefacto) y ADR-012 (los tests no escalan la clase).

Contexto: en el piloto de A-2 (`docs/history/piloto-orbitanova-2.md`), la
creación del plan disparó la duda PF-2: bajo el corte observable de ADR-012
(producción = todo lo que no ejecutan sólo los comandos de test), un plan
`.md` nuevo es producción, y por tanto **toda** tarea multi-tarea escala a
Architectural — la combinación "plan + Bounded" no existe. ¿Es un defecto del
corte o una consecuencia correcta?

Decisión: es correcta, y se vuelve explícita para dejar de depender de la
lectura: **crear o extender un plan de implementación es, por sí mismo, un
disparador de clase Architectural**. Vale a nivel del trabajo que crea o
extiende el plan; cada TAREA del plan hereda esa clase. La razón de fondo:
un plan existe cuando el trabajo ya no cabe en una tarea (ADR-010) — más
superficie coordinada exige el F0 completo de §7 (problema, resultado
observable, REQ-*, no objetivos, preguntas cerradas, EV-*). Ese F0 puede
vivir dentro del plan o junto a él — el piloto puso REQ y no-objetivos en el
plan y las preguntas cerradas y EV-* en el registro de evidencia; lo
obligatorio es que §7 esté completo, no su ubicación.

Alternativas descartadas:

- **Eximir los planes como los tests (extender ADR-012)**: abre la evasión de
  esconder producción bajo "gestión" — cualquier documento podría autodeclarar
  se plan para no escalar. El corte observable de "qué es gestión" es la misma
  trampa subjetiva que ADR-008 desterró.
- **Dejarlo implícito en el corte de ADR-012**: funciona pero invisible; cada
  ejecutor redescubre la duda y la resuelve a su favor (el patrón Skopos).
- **Permitir planes Bounded**: daría dos respuestas a la misma pregunta —
  Bounded por los archivos que toca cada tarea, Architectural por el alcance
  que hace necesario coordinarlas; y dejaría el F0 exigido a medio cubrir:
  coordinación multi-tarea sin §7 completo.

Consecuencias: la fila Architectural de `01` §2 lo explicita, y la fila
Spike lo cerca (un Spike no crea ni extiende planes: hacerlo escala). Un
efecto declarado: crear plan encarece la clase — es intencional; si el
trabajo cabe en una tarea, no hay plan y la clase la deciden los disparadores
de Bounded. Los planes previos a este ADR que no nacieron Architectural
(p. ej. PLAN-0001 de orbitaNova) no se reclasifican retroactivamente:
extenderlos sí dispara.

Verificación: `grep -n "ADR-013" docs/ai-agent-guide/01-analisis-y-requerimientos.md`
→ fila Architectural con el disparador;
`grep -n "ADR-013" docs/adr/00-INDICE.md` → fila registrada.

Procedencia: `docs/history/piloto-orbitanova-2.md` § PF-2 (2026-08-20);
ADR-010 (escala del plan); ADR-012 (corte producción/test que originó la duda).
