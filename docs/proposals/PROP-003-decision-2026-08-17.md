# PROP-003 — Decisión sobre los dos conflictos

> **Fecha:** 2026-08-17
> **Artefacto decidido:** [`PROP-003-frontera-con-praxis-dev.md`](PROP-003-frontera-con-praxis-dev.md)
> **Resultado:** ambos conflictos se resuelven convergiendo hacia Praxis Dev.
> **Responsable de la decisión:** maintainer de Skevi.
> **Efecto:** ninguno todavía. Cada decisión produce un ADR, y el ADR precede a
> la modificación del estándar y la guía.

## 1. Decisiones

| Conflicto | Decisión | Artefacto |
|---|---|---|
| Fail-closed absoluto frente a gradación por clase de operación | **graduar**, sin excepción posible en las clases protegidas | ADR-004 |
| Estado del trabajo frente a resultado de comprobación | **añadir el resultado por línea de evidencia**, conservando los tres estados de fase | ADR-005 |

Ninguna de las dos declara conformidad con `praxis/project-governance`, que
sigue en borrador no promovido. Skevi converge en la sustancia porque la
sustancia es mejor, no porque adopte el estándar ajeno.

## 2. Fail-closed: por qué graduar

El absoluto de Skevi §1.5 es más simple y más fácil de aplicar, y ésa es su
virtud. Su coste apareció durante esta misma sesión: **cuando parar sale
demasiado caro, el operador humano autoriza en bloque**. El clasificador de
permisos bloqueó tres veces una operación acotada, y la salida no fue una
excepción estrecha sino `--dangerously-skip-permissions`, que concede todo.

Una regla que en la práctica produce una autorización más amplia que la que
evitaba es una regla que empeora lo que protege.

La gradación de Praxis Dev cuelga el bloqueo de la **clase de operación**, no de
la fase del proyecto — que es el eje correcto, porque un agente siempre
encontrará que "está en desarrollo" y casi nunca que "está tocando seguridad"
sin darse cuenta.

Skevi adopta la sustancia con dos exigencias propias:

1. **Las clases protegidas no admiten excepción**: seguridad, publicación,
   políticas, decisiones aceptadas, datos de terceros y todo lo irreversible.
2. **Toda excepción se emite como degradación declarada con su razón**, nunca
   como silencio ni como éxito. Es la única forma en que un tercero puede
   contarlas después.

No se adopta el término `trabajo ordinario` de Praxis Dev: aparece cinco veces
en su corpus sin definirse, y es la misma forma que el `cotidiano vs crítico`
que el piloto Skopos demostró que un ejecutor resuelve a su favor. Está
reportado en `praxis-dev#16`, y su resolución pertenece a ese proyecto.

## 3. Vocabularios: por qué añadir en vez de reemplazar

La lectura completa deshizo el conflicto aparente. Skevi reporta **estado del
trabajo** —`OK` gate cumplido con evidencia, `PARCIAL` avance real al que falta
un criterio, `BLOQ` no se puede continuar sin decisión o permiso—; Praxis Dev
reporta **resultado de una comprobación**. Son ejes distintos y no compiten.

Lo que falta en Skevi no es el vocabulario: es la distinción entre **no cumple**
y **no se pudo medir**. Hoy las dos caen en `PARCIAL` o `BLOQ` según el criterio
del que reporta.

Para un agente esa distinción decide la acción siguiente: corregir el trabajo, o
conseguir mejor evidencia. Sin ella, "arregla" lo que no estaba roto.

La evidencia es de esta semana y es del propio ecosistema: el diagnóstico de
arranque de `an-kla-memory` **necesitó** `not_evaluated` distinto de `failed`, y
su primer diseño —un enum de cuatro estados— murió en la ronda adversarial
precisamente por no tener esa distinción. Un store íntegro en un árbol de sólo
lectura no es un store roto.

Por eso la decisión es **aditiva**: cada línea de evidencia declara su resultado,
`inconclusive` entra en el vocabulario, y el estado de fase se deriva de las
líneas. Los tres estados actuales sobreviven y los adoptantes que ya los usan
—`alubia` y `emd`— no se rompen.

Con la regla que la hace útil: **`inconclusive` nunca cierra un gate**. No es un
aprobado blando; es trabajo pendiente de conseguir evidencia.

## 4. Secuencia

1. ADR-004 y ADR-005 con esta decisión. *(este cambio)*
2. Ronda adversarial con contexto fresco y proveedor distinto sobre ambos.
3. Modificación del estándar §1.5 y de la guía `00-INDICE.md` y `04`.
4. Revisión de `alubia` y `emd` como adoptantes que ya usan el vocabulario
   anterior; el cambio es aditivo, pero conviene comprobarlo y no suponerlo.

## 5. Lo que esta decisión no concede

- No declara conformidad con `praxis/project-governance`.
- No modifica todavía el estándar ni la guía: eso ocurre en el paso 3.
- No adopta el vocabulario de Praxis Dev en el eje de estado del trabajo.
- No resuelve `trabajo ordinario`, que es de otro proyecto.
