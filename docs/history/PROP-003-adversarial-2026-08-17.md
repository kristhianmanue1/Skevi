# Ronda adversarial — PROP-003

**Fecha:** 2026-08-17
**Artefacto:** [`../history/PROP-003-frontera-con-praxis-dev.md`](../history/PROP-003-frontera-con-praxis-dev.md)
**Revisor:** `agy` con `gemini-3.1-pro-high`
**Contexto:** `fresco` — sesión y proveedor distintos del autor
**Modelo:** `gemini-3.1-pro-high`
**Ejecución:** sobre un clon desechable de Skevi, con acceso de lectura a
`praxis-dev` y `epistates` para poder comprobar las citas
**Decisión:** `fix-and-retry`

## Hallazgos aceptados

### [BLOCKER] La frontera dejaba los principios con dos hogares canónicos

**Problema:** §4 delegaba la autoridad en Praxis Dev y a la vez §6 congelaba la
capa de principios de Skevi conservando su texto. Los cinco principios
compartidos quedaban vivos en los dos sitios, con el mismo peso normativo.

**Impacto:** incumple el principio 3.3 del propio Praxis Dev —una afirmación
normativa tiene una sola fuente— que es el argumento central de la propuesta.

**Corrección:** nueva §4.1. La duplicación se declara **excepción temporal**,
con su razón —el hogar candidato es un borrador no promovido— y con condición de
caducidad: al promoverse una versión estable, los cinco principios pasan a ser
referencias. Decirlo es mejor que disimularlo. **Estado:** cerrado.

### [HIGH] El "conflicto" de las dos listas de operaciones no existía

**Problema:** §3 afirmaba que las listas de operaciones con autoridad de Skevi y
Praxis Dev derivarían. No colisionan: Skevi §4.3 gobierna operaciones de **Git**
—`push`, merge protegido, `reset --hard`, rebase, tags—; la matriz de Praxis Dev
gobierna operaciones de **gobernanza** —proponer, aceptar y reemplazar ADR,
excepciones, promoción del estándar—. Dominios disjuntos.

**Corrección:** se retira de la lista de conflictos, que baja de tres a dos, y se
reformula como lo que sí es: un riesgo de hueco, no de choque. **Estado:**
cerrado.

### [HIGH] La frontera abría un hueco en las operaciones de Git

**Problema:** corolario del anterior. Delegar "la matriz de operaciones
protegidas" sin matizar dejaba `push --force` y el rebase de historia compartida
sin hogar normativo, porque Praxis Dev no los cubre.

**Corrección:** la frontera declara explícitamente que Skevi **retiene** §4.3.
**Estado:** cerrado.

### [HIGH] Retirar iniciativas apoyándose en una dependencia inestable

**Problema:** §6 proponía retirar P0-01, A-1 y A-8 del backlog por estar
resueltas fuera, mientras §5 reconocía que Praxis Dev es un borrador no
promovido. La propuesta se contradecía a sí misma.

**Impacto:** si Praxis Dev cambia de posición, se estanca o no promueve nunca,
Skevi quedaría sin modelo de autoridad ni criterio de revisión independiente, y
sin iniciativa en el backlog para reconstruirlos.

**Corrección:** pasan a `deferred` bloqueadas, con condición nombrada —la
promoción estable— en vez de retiradas. **Estado:** cerrado.

### [MED] Praxis Dev especifica el CLI, no lo entrega

**Problema:** la propuesta trataba a Praxis Dev como si ya resolviera P0-00.

**Evidencia del revisor:** `praxis-dev/README.md:70` — *"Esta fase no implementa
todavía el CLI de producto `praxis`"*. Comprobado además: seis módulos Python y
seis archivos de test; `praxis_dev/cli.py` no registra subcomandos.

**Corrección:** §2.2 distingue ahora especificar de entregar. Que el contrato
exista basta para no reescribirlo en Skevi; no basta para dar por disponible una
herramienta. **Estado:** cerrado.

## Lo que el revisor atacó sin éxito

- **Citas torcidas:** comprobó una por una las de `estandar.md`,
  `fundamentos.md`, `modelo-autoridad.md`, `conformidad.md`, `contrato-cli.md` y
  `epistates/README.md`. Todas literales.
- **Solapamiento superficial:** revisó fila por fila la tabla §2.1 y concluyó
  que las equivalencias son semánticas, no léxicas.
- **El conflicto de fail-closed:** intentó descartarlo como artificial y
  concluyó que es real: la cláusula `development-unverified` permite avanzar
  donde Skevi manda detenerse.
- **Ausencia de referencia mutua:** `grep -rli skevi` sobre ambos repositorios,
  cero coincidencias, confirmado.

## Verificación independiente del autor

- `grep -n "no implementa todavía" praxis-dev/README.md` → línea 70, confirmado.
- `grep -n "add_parser\|def cmd_\|argparse" praxis_dev/cli.py` → sin salida.
- `ls tests/*.py | wc -l` → 6.

## Nota de método

Es la tercera ronda consecutiva con contexto fresco que devuelve
`fix-and-retry`, y la segunda con proveedor distinto. El BLOCKER de esta ronda
es del tipo más difícil de ver desde dentro: la propuesta usaba un principio
—hogar canónico único— como argumento contra otros, y lo incumplía en su propia
solución.

## Adenda — reducción posterior del artefacto (2026-08-17)

Después de cerrar esta ronda apareció `pinax`, el catálogo del ecosistema, con
un contrato versionado —`pinax/project-manifest/v1`— cuyos campos `ofrece`,
`no_ofrece`, `consume`, `fronteras_de_confianza` y `pospuesto` expresan de forma
validable la frontera que esta propuesta escribía en prosa.

PROP-003 se redujo entonces a lo que ningún manifiesto puede resolver: los dos
conflictos normativos. La frontera pasó a `project-manifest.yaml`.

Esto no invalida la ronda: sus cinco hallazgos siguen cerrados y el BLOCKER
—usar el principio de hogar canónico único como argumento y a la vez
incumplirlo— se resolvió por la vía más limpia posible, que es no tener dos
fuentes en absoluto.

Vale la pena registrar el patrón, porque es el tercero de la misma familia en
esta sesión: **el ecosistema ya tenía resuelto lo que Skevi estaba a punto de
escribir**. Primero `praxis-dev` con la autoridad y la revisión proporcional,
después `argos` con el plano de evidencia, ahora `pinax` con la declaración de
fronteras. En los tres casos la causa fue la misma: proponer sin haber
inventariado el ecosistema. Que es, literalmente, la razón por la que `pinax`
existe.
