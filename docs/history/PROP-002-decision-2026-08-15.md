# PROP-002 — Decisión por iniciativa

> **Fecha:** 2026-08-15
> **Artefacto decidido:** [`PROP-002-correcciones-desde-adoptantes.md`](PROP-002-correcciones-desde-adoptantes.md)
> **Resultado global:** parcialmente aceptada — 7 aceptadas, 2 diferidas.
> **Responsable de la decisión:** maintainer de Skevi.
> **Efecto:** ninguna iniciativa se convierte en norma por este documento. Cada
> aceptada produce ADR antes de modificar el estándar o la guía.

## 1. Decisiones

| ID | Decisión | Depende de | Evidencia exigida | Siguiente artefacto |
|----|----------|-----------|-------------------|---------------------|
| A-1 atestación de independencia | `accepted` | — | fixture: ronda con `contexto: fresco` sin rastro verificable → falla el gate | ADR-004 |
| A-8 disparadores objetivos | `accepted` | — | ningún calificador subjetivo queda como única condición de rigor | ADR-005 |
| A-7 declaración de adopción | `accepted` | — | dado un repo adoptante, un agente responde qué versión sigue y qué dejó, leyendo un archivo | ADR-006 |
| A-9 ancla verificable | `accepted` | — | barrido: ninguna regla de revalidación del corpus sin ancla nombrada | ADR-007 |
| A-5 contrato por campos | `accepted` | A-8 | instrucción breve con los 8 campos pasa; tarjeta extensa sin SHA base, no | ADR-008 |
| A-3 hard/soft gates | `accepted` **condicionada** | A-8 | lista de soft **enumerada y finita**; todo lo no enumerado es hard | ADR-009 |
| A-2 baseline por derivación | `accepted` | A-8, A-3 | fixture de origen mixto llega a baseline sin mutarlo ni declarar `F0: OK` retroactivo | ADR-010 |
| A-4 clasificación de sensibilidad | `deferred` | A-8 | un segundo proyecto, no clínico, que reporte necesitarla | — |
| A-6 gate extensible | `deferred` | — | un adoptante que reporte fricción al extender el gate | — |

Se ratifican los diez retiros de §4 de PROP-002, incluido el de P0-00.

## 2. Por qué A-1 va primero

Es la única iniciativa con evidencia de campo obtenida **midiendo**, no
argumentando. El 2026-08-15, sobre el ADR-0036 de `an-kla-memory`:

- la revisión del propio autor cerró en `proceed`;
- una ronda con contexto fresco sobre el mismo artefacto devolvió
  `fix-and-retry` con **2 BLOCKER y 3 HIGH**;
- uno de los BLOCKER era que el ADR contradecía literalmente a un ADR aceptado
  del mismo repositorio, que ya había descartado esa decisión por escrito;
- otro era que el ADR no cerraba el issue que lo motivaba.

Ninguno era sutil, y ninguno se detectó releyendo: los dos salieron de ejecutar
comandos. La diferencia entre `contexto: mismo` y `contexto: fresco` dejó de ser
una recomendación razonable y pasó a tener un caso medido.

A eso se suma la convergencia: `emd` institucionalizó `INDEPENDENT-AUDIT` como
artefacto recurrente y `ektel` inventó "revisión externa". Dos adoptantes
construyeron por su cuenta la pieza que el método no les daba.

## 3. Por qué A-3 queda condicionada

La distinción hard/soft es correcta y viene de un adoptante que la usa en
producción. Pero introduce una categoría no bloqueante en el punto exacto donde
el método ya falló: en el piloto Skopos, ante dos niveles de rigor, el ejecutor
eligió el bajo 4 de 4 veces sobre un componente con inyección de prompt
explotable.

Por eso se acepta **sólo** con la polaridad invertida respecto del modelo de
`emd`: la lista enumerada y finita es la de soft gates, y todo lo no enumerado es
hard por defecto. `emd` puede sostener el modelo abierto porque tiene controlador
humano y auditor independiente; un adoptante en solitario, no. Sin ese cierre, la
iniciativa se rechaza.

## 4. Por qué se difieren A-4 y A-6

**A-4 — clasificación de sensibilidad.** La evidencia es un solo adoptante, y es
un proyecto clínico con datos de pacientes: el caso donde la necesidad es
máxima y menos generalizable. Obligar a todo adoptante a declarar una
clasificación —incluido un script de 50 líneas— contradice la regla 3 del índice.
La cláusula anti-exceso de `emd` ("el tema médico no convierte automáticamente un
archivo en PHI") es valiosa y se recupera si la iniciativa se acepta más
adelante. Se reevalúa cuando un segundo proyecto, no clínico, reporte
necesitarla.

**A-6 — gate extensible.** `alubia` extendió el gate con una comprobación
anti-credenciales sin pedir permiso ni reportar fricción: el corpus nunca lo
prohibió. Normar que algo permitido está permitido no cambia ninguna conducta.
Se reevalúa si alguien reporta haber dudado.

## 5. Lo que esta decisión no concede

- No autoriza modificar el estándar ni la guía: cada aceptada necesita su ADR.
- No importa el dominio de `emd` —clínico, PHI, Moodle— al corpus de Skevi.
- No convierte la convergencia entre adoptantes en prueba de necesidad
  universal; la muestra son cuatro proyectos de un mismo autor humano.
- No autoriza instalar AN-KLA, Argos ni Escrubery.

## 6. Verificación

- `python3 scripts/check_sizes.py` → `OK`.
- `python3 -m unittest discover -s tests` → 16 tests, `OK`.
- Cobertura: las 9 iniciativas de PROP-002 tienen decisión; los 10 retiros de su
  §4 quedan ratificados.
