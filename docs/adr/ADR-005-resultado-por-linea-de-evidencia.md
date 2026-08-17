# ADR-005: cada línea de evidencia declara su resultado

Estado: aceptado; implementación no iniciada. Amplía el formato de reporte de
`docs/ai-agent-guide/00-INDICE.md` y de `04`, sin retirar los estados de fase.

Contexto: Skevi reporta el **estado del trabajo** con tres valores —`OK` gate
cumplido con evidencia, `PARCIAL` avance real al que falta un criterio, `BLOQ`
no se puede continuar sin decisión o permiso— y una lista de líneas
`comando → resultado observado`.

Lo que el formato no distingue es **una comprobación que falla** de **una
comprobación que no se pudo hacer**. Hoy las dos terminan en `PARCIAL` o en
`BLOQ` según el criterio de quien reporta.

Para un lector humano es un matiz. Para un agente decide la acción siguiente:
corregir el trabajo, o conseguir mejor evidencia. Sin la distinción, el ejecutor
"arregla" lo que no estaba roto.

La evidencia es del propio ecosistema y es de esta semana. El diagnóstico de
arranque de `an-kla-memory` necesitó `not_evaluated` distinto de `failed`, y su
primer diseño —un enum de cuatro estados compuestos— fue rechazado en ronda
adversarial precisamente por no representar esa diferencia: un store íntegro en
un árbol de sólo lectura no es un store roto, pero tampoco es un store
verificado.

`praxis/project-governance` ya exige distinguir `pass`, `fail` e
`inconclusive`. Su eje es el resultado de una comprobación, no el estado del
trabajo: los dos vocabularios no compiten.

Decisión: cada línea de evidencia declara su propio resultado.

```text
Evidencia:
- <comando o fuente> → <resultado observado> [pass | fail | inconclusive]
```

- `pass`: se comprobó y cumple.
- `fail`: se comprobó y no cumple.
- `inconclusive`: no se pudo comprobar. Lleva siempre su razón **y qué haría
  falta para que fuera concluyente**.

**Guardarraíl contra el abuso de `inconclusive`.** Marcar `inconclusive` es más
barato que marcar `fail`: no exige arreglar nada. Por eso la causa debe ser
**exógena a las acciones del propio ejecutor**. Si lo que impide medir lo
provocó él —borró el entorno, rompió la configuración, agotó su presupuesto—,
el resultado es `fail`, no `inconclusive`. Un `inconclusive` sin causa exógena
nombrada es un incumplimiento del formato, no una marca válida.

El estado de fase se **deriva** de las líneas y conserva sus tres valores
actuales. `inconclusive` **nunca cierra un gate**: no es un aprobado blando,
es trabajo pendiente de conseguir evidencia.

El cambio es aditivo. Los tres estados de fase sobreviven con su significado
exacto, y un reporte anterior sigue siendo legible: lo que gana es una columna
por línea, no una traducción.

**Transición para quien valide el formato.** Ningún gate de Skevi parsea
reportes hoy —`check_sizes.py` sólo comprueba estructura y tamaños—, así que el
cambio no rompe nada aquí. Pero la guía pide cumplir el formato *exactamente*
cuando el formato importa, y un adoptante puede haberse construido un validador
propio. Por eso la marca es **recomendada, no obligatoria, mientras dure la
transición**: un validador debe aceptar la línea con marca y sin ella. Pasa a
obligatoria cuando el proyecto adoptante declare que su validador la admite.

Alternativas descartadas:

- **adoptar `pass | fail | inconclusive` como estado de fase**, reemplazando los
  tres actuales: rompería a los adoptantes que ya reportan con ellos —`alubia` y
  `emd`— y confundiría dos ejes distintos, porque `BLOQ` significa "falta
  permiso o decisión", que no es el resultado de ninguna comprobación;
- **dejarlo como está y confiar en el criterio del que reporta**: es exactamente
  la clase de calificador subjetivo que este método ya midió que se resuelve a
  favor de quien reporta;
- **añadir sólo `inconclusive` al estado de fase**: mezclaría en el mismo campo
  el resultado de una comprobación con el estado del trabajo.

Consecuencias: los reportes se alargan una marca por línea. A cambio, un
tercero puede contar cuántas comprobaciones fueron concluyentes sin releer la
prosa, y un gate deja de poder cerrarse sobre evidencia que nadie pudo obtener.
Los adoptantes existentes no necesitan migrar nada; sus reportes siguen siendo
válidos y ganan precisión cuando adopten la marca.

Verificación: fixtures con las tres marcas; un caso en el que un gate intenta
cerrarse con una línea `inconclusive` y falla; y un reporte sin marcas que sigue
siendo legible.

Procedencia: PROP-003 §3.2 y su decisión del 2026-08-17. Evidencia del caso
real: `an-kla-memory`, ADR-0036 y su ronda adversarial; en Skevi,
`docs/history/drift-checkpoint-an-kla-2026-08-15.md`.
