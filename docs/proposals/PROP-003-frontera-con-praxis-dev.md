# PROP-003 — Dos conflictos normativos con Praxis Dev

> **Estado:** borrador en revisión; propuesta no normativa.
> **Decisión requerida:** resolver dos incompatibilidades entre el estándar de
> Skevi y `praxis/project-governance`. Ninguna es una errata: son posiciones
> distintas y sólo el humano puede elegir.
> **Efecto actual:** ninguno. No declara conformidad ni modifica el estándar.
> **Alcance reducido:** una versión anterior proponía además una frontera
> completa entre ambos proyectos. Esa parte se retiró; ver §4.

## 1. El hallazgo

En el mismo ecosistema existen **dos capas normativas que no se referencian
entre sí**: el estándar de Skevi (`docs/estandar-diseno-software-github.md`) y
el de Praxis Dev (`docs/estandar.md` más `fundamentos.md`, `modelo-autoridad.md`
y `conformidad.md`).

Praxis Dev se define como *"un estándar ejecutable de gobernanza para proyectos
de software asistidos por agentes de IA"*. Su tabla de límites enumera AN-KLA,
Kratos, Ágora, CAGF y Git. **Skevi no aparece.** Un `grep -rli skevi` sobre
`praxis-dev` y sobre `epistates` no devuelve nada, y Skevi tampoco los mencionaba
hasta esta propuesta.

Es el problema que P0-01 describe —un agente ante dos fuentes de autoridad
incompatibles resuelve arbitrariamente y sin avisar— a escala de ecosistema.

## 2. Solapamiento medido

Cinco de los siete principios de Skevi §1 tienen equivalente directo en
`fundamentos.md` §3 de Praxis Dev: evidencia sobre afirmaciones, autoridad
explícita, fail-closed, datos no confiables y simplicidad. La equivalencia es
semántica, no léxica; se verificó fila por fila.

Y **tres iniciativas del backlog de Skevi ya están escritas allí**:

| Iniciativa de Skevi | Dónde vive ya |
|---|---|
| P0-01 matriz de autoridad | `estandar.md` §1 y `modelo-autoridad.md` §4 |
| A-1 atestación de independencia | `conformidad.md` §7 |
| A-8 disparadores objetivos de rigor | `conformidad.md` §7 |

`conformidad.md` §7 incluso contiene la polaridad que esta sesión creyó
descubrir tras una ronda adversarial: *"La independencia se basa en procedencia
verificable, no sólo en nombres de modelos. Dos ejecuciones del mismo runtime
pueden aportar diversidad de lectura, pero no deben presentarse como
independencia fuerte."*

Y `modelo-autoridad.md` §4 nombra el mecanismo del problema con precisión:
*"el candidato y la supuesta prueba pueden ser creados por el mismo actor"*.

## 3. Los dos conflictos

Ninguno se resuelve declarando fronteras: los dos son posiciones normativas
distintas sobre la misma pregunta.

### 3.1 Fail-closed con excepción

**Skevi §1.5** no admite excepciones: *"ante la incertidumbre, el sistema se
detiene en estado seguro; nunca asume permiso ni éxito por defecto"*.

**Praxis Dev 3.6** admite una: durante el ciclo `development`, la autenticación
advisory puede degradarse a `development-unverified` **sin bloquear trabajo
ordinario**, declarando que esa excepción de ergonomía no satisface una
transición protegida ni habilita promoción estable.

**Precisión tras leer el texto completo.** El primer párrafo de esa misma
cláusula ya cuelga el bloqueo de la **clase de operación**, no de la fase:
*"para seguridad, publicación, políticas y decisiones aceptadas, `unknown`
bloquea"*. La excepción es por tanto estrecha y está acotada. El eje de Praxis
Dev es correcto, y más fino que el de Skevi, que sólo tiene un principio
absoluto sin gradación.

**Qué queda entonces del conflicto:** la excepción se apoya en el término
`trabajo ordinario`, que aparece cinco veces en el corpus de Praxis Dev y no se
define en ninguna. Es la misma forma que el `cotidiano vs crítico` de Skevi que
el piloto Skopos demostró que un ejecutor resuelve a su favor — 4 de 4 veces.
Reportado en `praxis-dev#16`; su resolución es de ese proyecto.

**Lo que decide Skevi**, con independencia de eso: si mantiene el fail-closed
como absoluto —regla simple, coste alto: cuando parar sale demasiado caro, el
operador humano acaba autorizando en bloque, que es menos seguro que una
excepción acotada— o si adopta una gradación equivalente por clase de
operación, sin excepción posible para seguridad, publicación, datos de terceros
e irreversibles, y siempre emitida como degradación declarada con su razón.

### 3.2 Dos vocabularios de resultado

**Skevi** cierra con `OK | PARCIAL | BLOQ`. **Praxis Dev** exige distinguir
`pass`, `fail` e `inconclusive`.

No son traducibles uno a uno: `inconclusive` significa "no se pudo medir", que
en Skevi cae ambiguamente entre `PARCIAL` y `BLOQ`. La distinción de Praxis es
mejor —separa no cumplir de no poder comprobar— y coincide con lo que el
diagnóstico de arranque de AN-KLA acabó necesitando: `not_evaluated` distinto de
`failed`.

**Precisión tras leer las definiciones.** No son dos vocabularios para lo mismo.
Skevi reporta **estado del trabajo** —`OK` gate cumplido con evidencia,
`PARCIAL` avance real al que falta un criterio, `BLOQ` no se puede continuar sin
decisión o permiso—. Praxis reporta **resultado de una comprobación**. Son ejes
distintos, y por eso no hay que elegir entre ellos.

**Lo que decide Skevi:** si cada línea de evidencia declara su propio resultado
con `inconclusive` incluido, y el estado de fase se deriva de esas líneas. Es
aditivo: los tres estados actuales sobreviven, `alubia` y `emd` no se rompen, y
entra la única distinción que hoy falta — "no cumple" frente a "no se pudo
medir"—, con la regla que la hace útil: **`inconclusive` nunca cierra un gate**.

### 3.3 Lo que resultó no ser un conflicto

Se afirmó que las dos listas de operaciones con autoridad derivarían. No
colisionan: Skevi §4.3 gobierna operaciones de **Git** —`push`, merge protegido,
`reset --hard`, rebase de historia compartida, tags—; la matriz de Praxis Dev
(`modelo-autoridad.md` §7) gobierna operaciones de **gobernanza** —proponer,
aceptar y reemplazar ADR, excepciones, promoción del estándar—. Dominios
disjuntos.

El riesgo real era el inverso: delegar "la matriz de operaciones protegidas" sin
matizar habría dejado las operaciones de Git sin hogar normativo. El manifiesto
de Skevi lo evita al declarar qué conserva.

## 4. Por qué esta propuesta se redujo

Su primera versión proponía además una frontera completa entre ambos proyectos,
escrita en prosa: qué conserva Skevi, qué delega, qué degrada si falta una
dependencia, qué iniciativas quedan bloqueadas.

Ese contenido tiene desde el 2026-08-17 un hogar mejor: `project-manifest.yaml`,
conforme a `pinax/project-manifest/v1`. Los campos `ofrece`, `no_ofrece`,
`consume` con `requerido: false`, `fronteras_de_confianza` y `pospuesto` dicen
lo mismo de forma validable, y el mapa del ecosistema los compila.

Mantener las dos versiones habría creado exactamente lo que este documento
denuncia: dos fuentes para una misma afirmación normativa. La frontera vive en
el manifiesto; aquí quedan sólo las incompatibilidades que ningún manifiesto
puede resolver.

## 5. Estado de la dependencia

Praxis Dev está en `0.1.0-draft.1`, *"borrador no promovido"*, y su §2 establece
que un proyecto conforme debe declarar una **versión estable**, y que un `draft`
puede usarse para pilotos pero no presentarse como conformidad estable.

Skevi **no puede declarar conformidad todavía**, y hacerlo incumpliría la regla
del estándar al que quiere adherirse. Por eso P0-01, A-1 y A-8 quedan
`deferred` bloqueadas por esa promoción, y no retiradas: si Praxis Dev cambia de
posición, se estanca o no promueve nunca, Skevi necesita conservar la iniciativa
para reconstruir su propio modelo de autoridad y de revisión.

Además `docs/contrato-cli.md` especifica un CLI que todavía no existe: el
`README.md` de Praxis Dev dice en su línea 70 *"esta fase no implementa todavía
el CLI de producto `praxis`"*. Especificar no es entregar.

## 6. No objetivos

- No fusionar los dos proyectos: Praxis Dev 3.2 dice "componer antes que
  fusionar", y esa frontera es sana.
- No declarar conformidad con un borrador.
- No suponer que Praxis Dev acierta por existir antes: los dos conflictos de §3
  pueden resolverse en cualquiera de las dos direcciones.
- No modificar el estándar por esta propuesta: primero la decisión.

## 7. Procedencia

Lectura directa de `praxis-dev` (`estandar.md`, `fundamentos.md`,
`modelo-autoridad.md`, `conformidad.md`, `contrato-cli.md`, `README.md`) y de
`epistates` el 2026-08-17. Ronda adversarial con contexto fresco y proveedor
distinto en
[`../history/PROP-003-adversarial-2026-08-17.md`](../history/PROP-003-adversarial-2026-08-17.md),
que devolvió `fix-and-retry` con 1 BLOCKER, 3 HIGH y 1 MED.
