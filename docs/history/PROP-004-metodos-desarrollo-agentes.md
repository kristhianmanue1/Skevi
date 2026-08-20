# PROP-004 — Métodos de desarrollo adaptados a agentes: clasificación, planes contractuales y TDD

> **Estado:** borrador en revisión; propuesta no normativa.
> **Decisión requerida:** aceptar, rechazar o diferir cuatro iniciativas que
> complementan el pipeline F0→F3 sin modificar el estándar atemporal.
> **Efecto actual:** ninguno. No modifica norma vigente hasta decisión y ADR.
> **Origen:** análisis crítico de `obra/superpowers` (2026-08-19) y ronda
> adversarial sobre deriva documental (PR #18).

## 1. Hallazgo

Skevi tiene un pipeline F0→F3 completo para **proyectos nuevos**, pero la
mayoría del trabajo de un agente sobre repos existentes son **cambios acotados**.
Sin clasificación, el agente aplica todo el pipeline a un bug de una línea
(overkill) o salta pasos en un cambio estructural (riesgo).

Paralelamente, hay una brecha entre F1 (decisiones/ADRs) y F3
(implementación): falta un artefacto contractual que diga *cómo* se ejecuta
sin caer en prosa narrativa o placeholders.

## 2. Iniciativas

### A-1: Clasificación de tarea — Spike / Bounded / Architectural

**Qué resuelve.** Evita aplicar F0→F3 completo a tareas que no lo necesitan,
y evita saltarse pasos en tareas que sí.

**Propuesta.** Añadir a `01-analisis-y-requerimientos.md` una clasificación
obligatoria en F0:

| Clase | Definición | Pipeline Skevi |
|---|---|---|
| Spike | Pregunta de factibilidad; output es respuesta, no código persistente | F0 mínimo, código `throwaway`, sin spec |
| Bounded | Cambio acotado en flujo existente del repo | F0 reducido, spec en chat, ADR solo si aplica |
| Architectural | Nuevo proyecto, subsistema o interfaz pública | F0 completo → F1 → F2 → F3 |

**Regla de ratchet.** Complejidad descubierta en mitad de tarea sube la
clasificación; nunca baja.

**Riesgos.** Sujetividad en "bounded" (¿el flujo existe realmente en disco?);
falsificación de "spike" para evitar proceso. Mitigación: duda → clase
superior.

### A-2: Formato de plan como plantilla contractual

**Qué resuelve.** Brecha entre ADR (el porqué) y código (el cómo). Hoy no hay
artefacto intermedio que sea verificable sin caer en prosa.

**Propuesta.** Crear `templates/plan-de-implementacion.md` con:

- **Header:** Global Constraints (verbatim del ADR/contrato que lo autoriza);
- **Por tarea:** Interfaces Consumes/Produces (qué recibe, qué entrega, en
  qué formato);
- **Checkbox steps:** pasos verificables, no prosa; cada step con comando o
  criterio de paso explícito;
- **Límite:** si el plan excede el tamaño del proyecto, se parte en
  sub-planes vinculados.

**Reglas de contenido.** Prohibido: código de producción, placeholders
(`TBD`, `TODO`, `similar a Task N`), prosa sin criterio de verificación.

**Riesgos.** Falsificación del formato (Consumes/Produces vagos); overlap con
F3 si incluye código. Mitigación: cada campo debe ser referenciable (archivo,
SHA, test, contrato).

### A-3: TDD como regla, no recomendación

**Qué resuelve.** El estándar §3.2 exige tests con cambios, pero no el orden
RED-GREEN-REFACTOR. Superpowers demuestra que el orden **es** la regla: si no
viste fallar, no sabes si el test prueba lo correcto.

**Propuesta.** Añadir a `estandar-diseno-software-github.md` §3.2 o a
`04-ejecucion-y-verificacion.md`:

> Todo cambio de comportamiento sigue RED-GREEN-REFACTOR:
> 1. RED — Escribir test que falla; verificar que falla por la razón correcta.
> 2. GREEN — Escribir código mínimo que pasa.
> 3. REFACTOR — Limpiar con suite en verde.
>
> Si se escribió código de producción antes del test, se borra. No se adapta,
> no se conserva como referencia.
>
> Excepciones declaradas (requieren aprobación en contrato de tarea):
> throwaway prototypes, código generado, archivos de configuración.

**Riesgos.** Resistencia cultural; proyectos sin infraestructura de test.
Mitigación: exención explícita en `skevi-gate.json` con razón, no omisión
silenciosa.

### A-4: Gate "no placeholders en planes"

**Qué resuelve.** Verifica mecánicamente que los artefactos de F1 (plans,
specs) no contienen marcadores de incompletitud.

**Propuesta.** Extender `scripts/check_sizes.py` o crear
`scripts/check_plan.py` que falle si detecta en artefactos de F1:
`TBD`, `TODO`, `FIXME`, `XXX`, `placeholder`, `similar a`, `later`,
`eventually`.

**Ámbito cerrado.** Solo aplica a secciones de pasos/verificación de
artefactos en `docs/` o `plans/`; no a comentarios explicativos en ADRs ni a
TODOs legítimos en código de F3.

**Riesgos.** Falsos positivos (`TODO` en contexto legítimo: "TODO: evaluar
cuando el volumen supere 10k req/s" es información, no placeholder).
Mitigación: ámbito restringido + lista de marcadores cerrada + mensaje de
error con línea exacta.

## 3. No objetivos

- No convertir Skevi en un framework de skills tipo Superpowers.
- No acoplar el pipeline a ningún harness o agente específico.
- No modificar el estándar atemporal §1–§8 por esta propuesta.
- No crear runtime ni ejecutable propio.

## 4. Secuencia si se acepta

1. Decisión de esta propuesta.
2. Ronda adversarial con contexto fresco y proveedor distinto.
3. ADR por iniciativa aceptada (A-1, A-2, A-3, A-4 pueden decidirse por
   separado).
4. Modificación de la guía F0/F1/F3 y creación de plantilla.
5. Extensión de `check_sizes.py` o creación de `check_plan.py` para A-4.

## 5. Procedencia

- Análisis de `obra/superpowers` ( skills `brainstorming`,
  `test-driven-development`, `writing-plans`, `executing-plans` ) el
  2026-08-19.
- Ronda adversarial sobre deriva documental (S1–S6) corregida en PR #18.
- Hallazgo: Skevi asume proyecto nuevo; la realidad del agente es mayormente
  cambio acotado sobre repo existente.
