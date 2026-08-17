# ADR-008: "material" para rigor de revisión son los disparadores de F3, no una sensación

Estado: aceptado; resuelve A-8 (PROP-002, `P1-03` de PROP-001), diferido su
número de ADR original por colisión de numeración — ver "Procedencia".

Contexto: `docs/ai-agent-guide/04-ejecucion-y-verificacion.md` §5.3 ya define
cuatro disparadores observables que sustituyeron, tras el piloto Skopos, al
criterio subjetivo "cotidiano vs crítico": persistencia de datos de terceros,
salida de LLM que actúa sin revisión humana, concurrencia, y consumidor
externo no controlado por el mismo autor. Esa corrección funcionó — el defecto
que motivó (aplicar la barra baja 4 de 4 veces sobre un componente con
inyección de prompt explotable) no volvió a aparecer.

El problema es que la palabra **"material"** se sigue usando, sin definición,
en al menos cuatro sitios que deciden **rigor de revisión** — si repetir la
ronda tras un fix (`04:108`), si la ronda adversarial es obligatoria antes de
cerrar un cambio (`AGENTS.md:55`) — sin apuntar a los cuatro disparadores que
ya existen. Un lector nuevo del corpus no tiene forma de saber que "material"
en esos sitios **significa exactamente** esos cuatro puntos.

Decisión: los cuatro disparadores de `04 §5.3` son el hogar canónico de
"material" para toda decisión de **rigor de revisión** — ronda adversarial
obligatoria, contexto fresco obligatorio, repetición de la ronda tras un fix.
Todo uso de "material" con ese sentido en el corpus referencia esos
disparadores en vez de reformularlos o dejarlos implícitos, siguiendo el mismo
patrón que unificó las cinco formulaciones de fail-closed (ADR-004).

**Alcance deliberadamente estrecho.** "Material" aparece también en otros dos
sentidos que este ADR **no** toca, porque ya tienen criterio propio o son
demasiado contextuales para forzar una definición común:

- si un **supuesto** es material y por tanto exige preguntar en vez de asumir
  (`00-INDICE.md` regla 2, `AGENTS.md` §"Prioridad ante conflicto");
- si un **pendiente** es material y por tanto bloquea cerrar una fase en `OK`
  (`00-INDICE.md` §"Formato de reporte de fase").

Un tercer uso —si una dependencia nueva es material y por tanto exige ADR
(`04` §"Escritura")— sí tenía criterio objetivo ya escrito, sólo sin
referenciar: `02-specs-adr-contratos.md` §3.1 ("alternativas reales con costes
distintos, cara o imposible de revertir, dependencia o frontera nueva"). Se
corrige con el mismo cruce, sin crear vocabulario nuevo.

Forzar una única definición universal de "material" en los tres sentidos
restantes sería peor que el problema que resuelve: un supuesto puede ser
material sin que el componente toque ninguno de los cuatro disparadores de
riesgo —por ejemplo, si el proyecto debe soportar Windows es un supuesto
material para F0 y no tiene nada que ver con concurrencia o datos de
terceros. Generalizar de más aquí violaría la regla 3 del propio índice: cada
artefacto responde a una incertidumbre real, no a una plantilla.

Alternativas descartadas:

- **Redefinir "material" de forma universal para los tres usos**: descartado
  arriba; el supuesto y el pendiente son preguntas distintas de "qué rigor de
  revisión exige este cambio", y una definición que las cubriera a todas
  quedaría o demasiado amplia para ser útil, o demasiado estrecha para ser
  correcta en los otros dos sentidos.
- **No tocar nada y confiar en que el lector infiera la conexión**: es el
  estado anterior a este ADR, y es exactamente la ambigüedad que costó cuatro
  fallos seguidos en el piloto Skopos antes de que `04 §5.3` existiera.

Consecuencias: ningún comportamiento nuevo — los disparadores ya regían de
facto para el contexto fresco desde el piloto Skopos. Lo que cambia es que
`AGENTS.md` y el resto de `04` dejan de usar la palabra suelta y apuntan al
mismo lugar, cerrando la ambigüedad para un lector que no conozca la historia
del piloto.

Verificación: `grep -rn "\bmaterial\b"` sobre el corpus normativo — cada
resultado debe ser identificable como uno de cuatro sentidos (rigor de
revisión → referencia a `04 §5.3`; dependencia nueva → referencia a `02 §3.1`;
supuesto o pendiente → contextual, sin referencia forzada).

Procedencia: PROP-002 §A-8 (equivalente a P1-03 de PROP-001), aceptada en
`docs/proposals/PROP-002-decision-2026-08-15.md`. Esa decisión reservó
`ADR-005` para A-8, pero ese número lo ocupó después la decisión de los
conflictos de PROP-003 (`docs/proposals/PROP-003-decision-2026-08-17.md`), sin
que nadie corrigiera la tabla original. A-1, A-7 y A-9 tienen la misma
colisión y siguen sin ADR propio; quedan fuera de este cambio.
`docs/history/piloto-skopos.md` F3 es la evidencia original de los cuatro
disparadores.
