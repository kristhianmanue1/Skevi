# PROP-004 — Métodos de desarrollo adaptados a agentes: clasificación, planes contractuales y TDD

> **Estado:** decidida 2026-08-20 — ver
> [`PROP-004-decision-2026-08-20.md`](PROP-004-decision-2026-08-20.md).
> Esta v2 absorbe la ronda adversarial del 2026-08-20
> ([`PROP-004-adversarial-2026-08-20.md`](PROP-004-adversarial-2026-08-20.md);
> la v1 queda en el commit `8a1f314`, ancla declarada de esa ronda).
> **Decisión requerida:** aceptar, rechazar o diferir A-1, A-2 y A-3 por
> separado; A-4 se propone **diferida con condición nombrada**.
> **Efecto actual:** ninguno. No modifica norma vigente hasta decisión y ADR.
> **Hogar declarado:** la guía (`docs/ai-agent-guide/`) y sus plantillas.
> Ninguna iniciativa toca el estándar §1–§8: la ronda bloqueó la rama que lo
> hacía (A-3 en §3.2), consistente con el no-objetivo y con el ítem
> `pospuesto` "capa de métodos... separada del estándar atemporal".
> **Origen:** análisis de `obra/superpowers` (2026-08-19, **Referencia**:
> informa, no define), ronda sobre deriva documental (PR #18), ronda
> adversarial propia (2026-08-20, `fix-and-retry`).

## 1. Hallazgo

Skevi tiene un pipeline F0→F3 completo para **proyectos nuevos**, pero la
mayoría del trabajo de un agente sobre repos existentes son **cambios
acotados** — es el ítem `pospuesto` "procedimiento de entrada para proyectos
ya iniciados" (`project-manifest.yaml`), casi con estas palabras. Sin
clasificación, el agente aplica todo el pipeline a un bug de una línea
(overkill) o salta pasos en un cambio estructural (riesgo).

Paralelamente, hay una brecha entre F1 (decisiones) y F3 (ejecución por
TAREA): cuando el trabajo cruza varias tareas, sesiones o agentes, la TAREA
individual no alcanza para sostener coherencia.

## 2. Iniciativas

### A-1: Clasificación de tarea con disparadores observables

**Qué resuelve.** Evita aplicar F0→F3 completo a tareas que no lo necesitan,
y saltarse pasos en tareas que sí — sin reintroducir el calificador subjetivo
que ADR-008 desterró tras el piloto Skopos (4/4 aplicaciones incorrectas de
"cotidiano vs crítico").

**Propuesta.** Clasificación obligatoria al fijar cada TAREA (04 §1), con
clases definidas por **disparadores observables en disco**, no calificativos:

| Clase | Disparadores observables | Pipeline Skevi |
|---|---|---|
| Spike | La pregunta es de factibilidad; la salida es una respuesta, no código persistente | F0 mínimo; salida = respuesta con EV-* |
| Bounded | Toca sólo código/flujos **existentes en disco**, sin dependencias nuevas, sin interfaz pública ni contrato nuevos, y no activa ninguno de los cuatro disparadores de 04 §5.3 — **referenciados, no reformulados** | F0 reducido; spec en la rama; ADR sólo si aplica |
| Architectural | Cualquier condición de Bounded no cumplida | F0 completo → F1 → F2 → F3 |

Reglas:

- **Ratchet:** complejidad descubierta a mitad de tarea sube la clase; nunca
  baja. Ante duda sobre si un disparador aplica, la clase superior — la misma
  forma de "ante duda sobre la clase, es protegida" de ADR-004, pero anclada
  a observables, no al juicio de "acotado".
- **Hogar del código de Spike:** rama no fusionada o fuera del repo. Nada del
  Spike llega a `main` sin reclasificarse como Bounded/Architectural.
- **Hogar de la spec de Bounded:** la rama de la tarea o la descripción del
  PR — nunca "en chat": una spec que F3 y la ronda adversarial deben
  contrastar tiene que ser visible para una sesión nueva (04 §3 y §5.1). El
  chat puede originarla; no almacenarla.
- La clase se registra en la TAREA, que para Spike/Bounded admite cubrir un
  REQ sin SPEC.

### A-2: Plan de implementación como artefacto de escala

**Qué resuelve.** La brecha de coherencia cuando el trabajo cruza múltiples
tareas, sesiones o agentes. **No** reemplaza ni duplica la TAREA: una tarea
sola se ejecuta sólo con su TAREA (04 §1), como hoy.

**Propuesta.** `templates/plan-de-implementacion.md`, obligatorio sólo a
partir de esa escala:

- **Fuente única:** cuando hay plan, la TAREA lo referencia y el plan es dueño
  de los criterios (DoD, steps); nunca dos documentos con criterios de
  aceptación paralelos — el modo de fallo que el estándar §3.5 documenta.
- **Header:** restricciones globales verbatim del ADR/contrato que autoriza.
- **Por tarea:** Interfaces Consumes/Produces que **resuelven** a un
  CONTRATO/SPEC existente o declaran cuál crearán.
- **Steps con checkbox:** cada step referencia un archivo, comando o test
  real del repo y su criterio de paso explícito.
- **Hogar y límite:** `docs/plans/` (o el equivalente declarado por el
  proyecto adoptante); límite 300 como plantilla derivada (§3.4 del
  estándar); si excede, se parte en sub-planes vinculados.
- **Prohibido:** código de producción, placeholders (`TBD`, `TODO`),
  "similar a Task N", prosa sin criterio de verificación.

### A-3: RED-GREEN-REFACTOR como default de F3

**Qué resuelve.** El estándar §3.2 exige tests con cambios, pero no el orden.
Si no viste fallar el test, no sabés si prueba lo correcto.

**Propuesta.** En `04-ejecucion-y-verificacion.md` §3 — **no** en el estándar
(resuelto el bloqueo de la v1):

> Si el proyecto tiene infraestructura de tests, todo cambio de comportamiento
> sigue RED-GREEN-REFACTOR: (1) RED — test que falla, verificando que falla
> por la razón correcta; (2) GREEN — código mínimo que pasa; (3) REFACTOR —
> limpieza con suite en verde.

Reglas:

- **Hereda la condicionalidad de §3.2:** aplica si hay infraestructura de
  tests; crearla para un cambio acotado es decisión del contrato de tarea, no
  obligación silenciosa. La exención por proyecto no viaja por
  `skevi-gate.json` (su esquema es cerrado y comprueba forma, no método).
- **Evidencia:** el reporte de tarea incluye la **salida del RED** (test
  fallando). "Se borró el código prematuro" no es evidencia verificable y no
  se exige como tal — se exige el RED, que sí deja registro.
- **Excepciones** declaradas en el contrato de tarea: throwaway (Spike),
  código generado, configuración. Para Spike, que no tiene SPEC, la TAREA
  cubre con REQ o declara throwaway.
- **Procedencia honesta:**   `obra/superpowers` es una Referencia que informa
  esta regla, no la demuestra. Se adopta porque Skevi mismo opera test-first
  (su único ejecutable lleva suite propia desde ADR-006: 39 tests hoy) y
  porque el piloto Skopos registró el coste de verificación tardía.

### A-4: Gate de planes — diferida con condición

**Por qué se difiere.** Su ámbito no existe hasta que A-2 produzca planes
reales: un gate siempre verde es el anti-patrón que 03 §3 prohíbe
expresamente. Y la detección por vocabulario es trivialmente eludible en un
corpus en español, con falsos positivos ya medidos (la propia v1 contenía 21
ocurrencias de su lista — ronda 2026-08-20).

**Condición de reactivación:** planes de A-2 en uso real en al menos un
piloto con evidencia. Entonces se evalúa el **chequeo estructural** — cada
step referencia un archivo/comando/test que existe y resuelve al momento del
gate, análogo al check CONTRATO↔código de 04 §9 —, no listas de vocabulario.

## 3. No objetivos

- No convertir Skevi en un framework de skills tipo Superpowers.
- No acoplar el pipeline a ningún harness o agente específico.
- No modificar el estándar atemporal §1–§8 por esta propuesta — ahora en
  ninguna iniciativa, incluida A-3.
- No crear runtime ni ejecutable propio.

## 4. Dependencias y mapeo al manifiesto

| ID | Recomendación de esta v2 | Depende de | Ítem `pospuesto` que resuelve |
|---|---|---|---|
| A-1 | aceptar | — | "procedimiento de entrada para proyectos ya iniciados" (parcial: define la puerta; el procedimiento completo llega con el piloto) |
| A-2 | aceptar como artefacto de escala | A-1 (la clase define cuándo hay plan) | "capa de métodos de desarrollo adaptados a agentes" (parcial) |
| A-3 | aceptar como default condicional | — | ídem A-2 (parcial) |
| A-4 | diferir con condición nombrada | A-2 desplegada y pilotada | ninguno |

Aceptada una iniciativa, el cierre de su ADR actualiza `project-manifest.yaml`
(checklist de 02 §3.3) para des-posponer exactamente lo que la tabla declara.

## 5. Secuencia

1. ~~Ronda adversarial~~ — hecha (2026-08-20, `fix-and-retry`); esta v2
   absorbe sus hallazgos.
2. Decisión del maintainer por iniciativa (la ronda precede a la decisión,
   como en PROP-001/002).
3. ADR por iniciativa aceptada + `project-manifest.yaml`.
4. Ediciones de guía (01 para A-1; 03/04 para A-2 y A-3) y plantilla
   `templates/plan-de-implementacion.md`.
5. **Piloto real** de A-1/A-2 sobre un cambio acotado en un repo del
   ecosistema. Ninguna fase F0→F3 corrió aún completa sobre un proyecto real
   (README, Estado); esta propuesta no agrava esa deuda sin evidencia
   doméstica: A-4 y la generalización de A-2 quedan condicionadas al piloto.

## 6. Procedencia

- Análisis de `obra/superpowers` (skills `brainstorming`,
  `test-driven-development`, `writing-plans`, `executing-plans`),
  2026-08-19 — clasificado **Referencia** por la tabla de fuentes de `01`
  («Fuentes y su clasificación»).
- Ronda adversarial sobre deriva documental (S1–S6), corregida en PR #18.
- Ronda adversarial de esta propuesta, 2026-08-20 — 1 BLOCKER, 6 HIGH,
  6 MED, todos absorbidos aquí; hallazgo HIGH fuera de alcance (duplicación
  en `02`) corregido aparte.
- `project-manifest.yaml` `pospuesto` ítems 1 y 2.
