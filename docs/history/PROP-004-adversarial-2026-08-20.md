# Ronda adversarial — PROP-004

**Fecha:** 2026-08-20
**Artefacto:** PROP-004 — `docs/proposals/PROP-004-metodos-desarrollo-agentes.md`
en el commit `8a1f314` (tras la decisión del 2026-08-20 vive en este mismo
directorio: `PROP-004-metodos-desarrollo-agentes.md`)
**Revisor:** subagente de contexto fresco (sesión nueva, sin memoria de autoría)
**Modelo:** misma familia que el autor (GLM) — proveedor **no** distinto; se
declara porque una ronda sin contexto declarado no acredita independencia
**Ejecución:** sobre el árbol de Skevi en `8a1f314`, lectura completa del
corpus y verificación con comandos
**Decisión:** `fix-and-retry`

## Hallazgos aceptados

### [BLOCKER] A-3 es indecidible tal como está: propone dos hogares y uno viola su propio no-objetivo

**Problema:** A-3 dice "Añadir a `estandar-diseno-software-github.md` §3.2 o
a `04-ejecucion-y-verificacion.md`" (PROP-004:72-73), mientras el no-objetivo
§3 dice "No modificar el estándar atemporal §1–§8 por esta propuesta"
(PROP-004:113). §3.2 está dentro de §1–§8: una de las dos ramas de la propia
propuesta viola su propio no-objetivo. En paralelo, el manifiesto difiere
explícitamente la "capa de métodos de desarrollo adaptados a agentes,
separada del estándar atemporal" (`project-manifest.yaml:51`); TDD-como-regla
es exactamente esa capa.

**Impacto:** aceptar A-3 "por separado" sin resolver el hogar, o rompe el
no-objetivo, o revierte un ítem `pospuesto` sin tratarlo. El estándar §8
aplica literal: no se decide por omisión, y la propuesta omite decidir su
propia ubicación.

**Corrección:** eliminar la rama §3.2 y fijar A-3 en `04` (la guía, lado
consistente con "separada del estándar"), declarando que su aceptación
des-posponga una franja del ítem 51 del manifiesto.

**Estado:** abierto — exige v2 de la propuesta.

### [HIGH] A-1: "Bounded" reintroduce el calificador subjetivo que el corpus desterró dos veces

**Problema:** "Bounded = cambio acotado en flujo existente" es circular
(acotado = bounded) sin disparadores observables. La clase decide cuánto
pipeline aplica — la misma decisión que ADR-008 volvió objetiva con cuatro
disparadores — y el mismo patrón de "trabajo ordinario" que PROP-003 §2
rechazó por indefinido, "la misma forma que el cotidiano vs crítico que el
piloto Skopos demostró que un ejecutor resuelve a su favor" (Skopos: 4/4
aplicaciones incorrectas sobre el mismo tipo de componente).

**Impacto:** la mitigación "duda → clase superior" deriva del juicio del
ejecutor sobre "acotado", no de un observable. Un ejecutor que quiera evitar
proceso clasifica Bounded sin estar "en duda": es el vector de evasión que
la propia sección de riesgos de PROP-004 nombra y no cierra.

**Corrección:** definir cada clase con disparadores observables, no
calificadores. Bounded = toca flujos existentes en disco, sin dependencias
nuevas, sin interfaz pública nueva, sin contrato nuevo, y no activa ninguno
de los cuatro disparadores de `04` §5.3 — referenciados, no reformulados
(patrón ADR-008).

**Estado:** abierto — exige v2 de la propuesta.

### [HIGH] A-1: "spec en chat" rompe la trazabilidad y la propia ronda adversarial

**Problema:** la spec de una tarea Bounded viviría en el chat (PROP-004:34).
`04` §3 define la trazabilidad como "SPEC → test → evidencia" (04:46-47) y
§5.1 ordena al revisor de contexto fresco revisar "sólo el diff y las specs"
(04:78-80): una spec en chat es invisible para una sesión nueva o un
subagente — el mecanismo que ADR-008 vuelve obligatorio ante sus
disparadores. No contradice 01 §6 (que permite el documento de F0 en
conversación para proyectos chicos): el problema es específico de specs que
F3 y la ronda deben contrastar después.

**Impacto:** la clase de tarea más frecuente — Bounded, por el propio hallazgo
§1 de la propuesta — queda sin artefacto verificable: sin trazabilidad
comprobable, sin ronda adversarial posible con contexto fresco, fuera de todo
gate.

**Corrección:** la spec de Bounded vive en la rama de la tarea o en la
descripción del PR; el chat puede originarla, nunca almacenarla.

**Estado:** abierto — exige v2 de la propuesta.

### [HIGH] A-2: solapa con el contrato de tarea TAREA sin declarar la relación — dos fuentes de verdad

**Problema:** TAREA ya fija por tarea: objetivo, permitido/prohibido y "DoD:
checks ejecutables" (04:11-19). El plan añade "Global Constraints" y "steps
con comando o criterio de paso" (PROP-004:51-56): misma función autorizadora
+ criterio ejecutable en dos artefactos, sin decir si el plan reemplaza,
envuelve o coexiste con TAREA. El corpus ya pelea esta batalla en §3.5 del
estándar: "el contenido sustantivo vive en un solo lugar; las copias se
desincronizan". Tampoco propone trazabilidad plan↔SPEC, análoga al check
CONTRATO↔código que sí existe (04 §9:208-214).

**Impacto:** cada tarea tendría dos documentos con criterios de aceptación
que derivarán; un agente actualizará uno y no el otro.

**Corrección:** decidir la relación en la propuesta — una sola fuente: TAREA
referencia el plan y le cede sus campos de criterio, o el plan es una sección
de TAREA. Añadir el check espejo: cada Interfaces Consumes/Produces resuelve
a un CONTRATO/SPEC existente.

**Estado:** abierto — exige v2 de la propuesta.

### [HIGH] A-3: la exención vía `skevi-gate.json` no es expresable — el esquema del gate es cerrado

**Problema:** la mitigación para proyectos sin tests es "exención explícita
en `skevi-gate.json`" (PROP-004:87). `CONFIG_KEYS` es un conjunto cerrado de
seis claves (`check_sizes.py:115-118`) y una clave desconocida **falla**
(polaridad cerrada, 170-172). No existe clave para exenciones semánticas ni
campo "razón"; el gate comprueba forma y tamaño, no cumplimiento de reglas
(`project-manifest.yaml:26`). La §4-secuencia sólo prevé extensión del gate
para A-4, no para A-3.

**Impacto:** la única vía de escape de una regla incondicional ("**Todo**
cambio de comportamiento sigue RED-GREEN-REFACTOR") es inexistente. Para un
proyecto sin infraestructura de tests — caso que §3.2 del estándar ya trata
como condicional ("Si el proyecto tiene tests...") — A-3 es insatisfacible y
no eximible: BLOQ permanente o incumplimiento silencioso.

**Corrección:** heredar la condicionalidad de §3.2 (aplica si existe
infraestructura de test; crearla es decisión del contrato de tarea). Más
simple que extender el gate (criterio §8.1).

**Estado:** abierto — exige v2 de la propuesta.

### [HIGH] A-4: gate vacuo — el ámbito que declara escanear no existe en el repositorio

**Problema:** el ámbito es "artefactos de F1 en `docs/` o `plans/`"
(PROP-004:100-101). No existe `docs/specs/` ni `plans/` (verificado: `ls`).
En Skevi los artefactos de F1 son ADRs, que la propuesta excluye
explícitamente. Qué cuenta como "artefacto de F1" dentro de `docs/` queda
indefinido: hoy el gate comprobaría cero archivos.

**Impacto:** siempre verde — el anti-patrón que el propio corpus prohíbe:
"Un pipeline que siempre está en verde porque no comprueba nada es peor que
no tener pipeline" (03:66-68). Seguridad falsa de "verificación mecánica".

**Corrección:** anclar el gate a los planes que A-2 crea (dependencia
declarada), y fallar si el ámbito declarado existe pero está vacío.

**Estado:** abierto — exige v2 de la propuesta.

### [HIGH] Transversal: "pueden decidirse por separado" es falso — dependencias no declaradas

**Problema:** §4 dice que A-1 a A-4 "pueden decidirse por separado"
(PROP-004:120-121). Pero: (1) A-4 sin A-2 no tiene nada que escanear; (2) si
A-1 se acepta con "spec en chat", las tareas Bounded quedan fuera del ámbito
de A-4: aceptar ambas **aumenta** la fracción de trabajo invisible al gate;
(3) A-3 exige excepciones "con aprobación en contrato de tarea", pero TAREA
exige "Objetivo: cubre SPEC-\<n\> o REQ-\<n\>" (04:13) y el Spike de A-1 es
"sin spec" — el mecanismo de excepción es inalcanzable para la clase que más
lo necesita. El precedente inmediato declaraba dependencias en columna propia
("Depende de", PROP-002-decision:12).

**Impacto:** decisiones por separado producen combinaciones incoherentes.

**Corrección:** matriz de dependencias explícita estilo PROP-002; Spike deja
un artefacto mínimo (TAREA con REQ aunque sin SPEC); la excepción de A-3 no
depende de un campo que Spike no puede llenar.

**Estado:** abierto — exige v2 de la propuesta.

### [MED] A-1: el código throwaway del Spike no tiene hogar definido

**Problema:** "código `throwaway`, sin spec" (PROP-004:33) sin decir dónde
vive. §4.1 del estándar exige rama de trabajo siempre; §3.1 "cada cambio se
entrega completo o no se entrega".

**Impacto:** un Spike puede dejar código a medias en el árbol o fusionarse
"porque ya está"; sin regla, cada ejecutor inventa.

**Corrección:** el código de Spike vive en rama no fusionada o fuera del
repo; su salida es una respuesta con EV-*; nada del Spike llega a main sin
reclasificarse.

**Estado:** abierto — exige v2 de la propuesta.

### [MED] A-2: fase y hogar canónico del plan sin decidir; "límite" sin número

**Problema:** §4 paso 4 dice "Modificación de la guía F0/F1/F3" sin fijar en
qué fase vive el plan. El gate de F1 (02 §6) no incluye plan; F1 produce
decisiones, F3 ejecuta por TAREA. `plans/` no existe en ningún otro lugar del
corpus. "Si el plan excede el tamaño del proyecto" (PROP-004:56-57) no dice
qué límite.

**Corrección:** el plan es artefacto de entrada de F3 que TAREA referencia;
hogar `docs/plans/` (extendiendo la convención de 03:46) o dentro de la
tarea; límite explícito (300, como plantilla derivada).

**Estado:** abierto — exige v2 de la propuesta.

### [MED] A-4: detección por vocabulario, trivialmente eludible; el chequeo estructural ausente

**Problema:** la lista cerrada (`TBD`, `TODO`, `similar a`, `later`...) es
eludible cambiando palabras — el corpus es español y los marcadores en su
mayoría ingleses: "pendiente de definir", "parecido a", "más adelante"
pasan. Y ya hay superficie de falso positivo: 21 ocurrencias
case-insensitive de la propia lista **dentro de PROP-004** (discute los
marcadores) y más en prosa normativa legítima del estándar y la guía.

**Impacto:** verifica vocabulario, no completitud. A-2 ya exige "cada step
con comando o criterio de paso": el análogo real del check CONTRATO↔código
sería estructural, y no está propuesto.

**Corrección:** reemplazar o complementar el escaneo léxico por verificación
estructural: cada step referencia una ruta/comando/test que existe y resuelve
al momento del gate.

**Estado:** abierto — exige v2 de la propuesta.

### [MED] A-3: regla sin evidencia verificable; "Superpowers demuestra" eleva una Referencia a Evidencia

**Problema:** (1) "Si se escribió código antes del test, se borra"
(PROP-004:80-81) no es verificable con comando alguno; el manifiesto
descuenta exactamente esa verificación. El RED sí deja evidencia (salida del
test fallando); el borrado, no. (2) "Superpowers **demuestra** que el orden
es la regla" (PROP-004:69-70) trata un corpus de terceros como Evidencia que
define requisito; para 01 §2.1 una Referencia "informa decisiones, nunca
define requisitos", y ningún registro in-repo del análisis existe.

**Corrección:** (1) exigir en el reporte de tarea la evidencia del RED, no
la declaración del borrado; (2) reformular como "el análisis sugiere; la
regla se adopta por X" con X propio, o registrar la evidencia del análisis.

**Estado:** abierto — exige v2 de la propuesta.

### [MED] Transversal: sin mapeo iniciativas → ítems `pospuesto` del manifiesto

**Problema:** A-1 ataca casi con las mismas palabras el ítem 50 del
manifiesto ("procedimiento de entrada para proyectos ya iniciados"); A-2/A-3
son el ítem 51 ("capa de métodos..."). Ninguna sección declara qué ítem
resuelve cada iniciativa, y la checklist de cierre de ADR (02 §3.3:88-89) lo
exigirá después.

**Impacto:** aceptar A-1 sin tocar el manifiesto deja `pospuesto`
contradictorio: "hoy la guía asume proyecto nuevo" dejaría de ser cierto.

**Corrección:** tabla "ítem de `pospuesto` que resuelve / no resuelve" por
iniciativa.

**Estado:** abierto — exige v2 de la propuesta.

### [MED] Transversal: §4 pone la decisión antes de la ronda adversarial — regresión respecto de PROP-001/002

**Problema:** §4: "1. Decisión... 2. Ronda adversarial" (PROP-004:118-119).
En PROP-001 la ronda (08-14) precedió a la decisión (08-15); en PROP-002 fue
insumo de la decisión el mismo día. Esta ronda corrige el orden de facto —
existe antes de la decisión — pero el texto de la propuesta sigue
regresión del precedente.

**Corrección:** invertir los pasos 1 y 2 de §4 en la v2.

**Estado:** abierto — exige v2 de la propuesta.

## Lo que el revisor atacó sin éxito

- **El hallazgo §1 (la brecha).** La premisa de que la guía asume proyecto
  nuevo y el trabajo real es mayormente cambio acotado sobrevivió el ataque:
  el manifiesto `pospuesto` ítem 50 lo dice casi con las mismas palabras.
- **La prohibición de "similar a Task N" en A-2.** No es ornamento: es un
  modo de fallo real de ejecutores y ningún artefacto actual lo prohíbe.
- **El tamaño.** La plantilla de A-2 cabe en el límite de 300 de plantillas
  del gate; ninguna iniciativa exige tocar límites.

## Hallazgo fuera de alcance (registrado, no es de esta propuesta)

- **[HIGH] `02-specs-adr-contratos.md` carga un bloque duplicado.**
  "Reglas:" aparece dos veces consecutivas (líneas 65 y 67) y las viñetas de
  reglas de ADR aparecen dos veces (líneas 71 y 97), con §3.3 intercalado en
  el medio. Es deriva verificable en un archivo canónico de la guía, de la
  familia exacta que el estándar §3.4 describe ("duplicados, numeración rota
  y reglas que se contradicen"). Ningún gate actual la detecta — ni la
  detectaría A-4, que escanea vocabulario: evidencia adicional para el
  chequeo estructural. Corrección: tarea separada, antes de editar esa
  guía para cualquier iniciativa aceptada.

## Verificación independiente del autor

- `sed -n '70,75p;110,114p' docs/proposals/PROP-004-metodos-desarrollo-agentes.md`
  → rama "§3.2 o 04" y no-objetivo "§1–§8" literales, en el mismo archivo
  [pass: BLOCKER confirmado]
- `grep -n "Reglas:" docs/ai-agent-guide/02-specs-adr-contratos.md` → líneas
  35, 65, 67, 125 (doble en §3.2) [pass: duplicación confirmada]
- `grep -n "Una alternativa sin razón" docs/ai-agent-guide/02-specs-adr-contratos.md`
  → líneas 71 y 97 [pass: bloque duplicado confirmado]
- `ls docs/specs plans` → "No such file or directory" ×2 [pass: ámbito de
  A-4 hoy vacío]
- `sed -n '115,119p' scripts/check_sizes.py` → `CONFIG_KEYS` cerrado, sin
  clave de exención semántica [pass: mitigación de A-3 no expresable]
- `rg -in 'TBD|TODO|FIXME|XXX|placeholder|similar a|later|eventually' --count-matches docs/proposals/PROP-004-metodos-desarrollo-agentes.md`
  → 21 ocurrencias [pass: la propuesta haría zoom en su propio gate]
- `grep -n "Depende" docs/history/PROP-002-decision-2026-08-15.md` → línea
  12, columna "Depende de" [pass: precedente de matriz de dependencias]
- `grep -l "fix-and-retry" docs/history/*adversarial*.md` → 5 de 5 rondas
  previas [pass: sexta consecuta, patrón registrado en la nota de método]

## Nota de método

La propuesta nació de analizar un corpus externo (`obra/superpowers`) sin
inventariar las decisiones internas ya registradas: dos iniciativas chocan
con texto vigente (ítem `pospuesto` 51, ADR-008), la mitigación de una choca
con el esquema cerrado del propio gate, y la secuencia olvida el orden que
PROP-001/002 establecieron. Es el mismo patrón que la adenda de la ronda de
PROP-003 registró: proponer sin haber inventariado el ecosistema — esta vez
el interno. Y es la sexta ronda consecutiva que devuelve `fix-and-retry`;
  el ciclo de corrección previo a la decisión está funcionando, no fallando.

## Pendiente antes de re-decidir

1. v2 de la propuesta absorbiendo los hallazgos (estados pasan a `cerrado`).
2. `python3 scripts/check_sizes.py` y `python3 -m unittest discover -s tests`
   sobre el cambio.
3. Re-lectura de la v2 contra `project-manifest.yaml:49-53` (mapeo
   iniciativas → `pospuesto`).
4. Ronda fresca focalizada: ¿los disparadores de Bounded son observables
   (mismo criterio que ADR-008 exigió para "material")?
