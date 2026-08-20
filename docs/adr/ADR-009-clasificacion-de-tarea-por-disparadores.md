# ADR-009: Clasificación de tarea por disparadores observables, no calificativos

Estado: aceptado; implementa A-1 de PROP-004. Los disparadores de rigor de
Bounded **referencian** los de `04` §5.3 (ADR-008); no los reformulan.

Contexto: la guía F0→F3 asume proyecto nuevo — ítem `pospuesto` del manifiesto
("procedimiento de entrada para proyectos ya iniciados"). El trabajo real de
un agente sobre repos existentes es mayormente cambio acotado. Sin
clasificación, el ejecutor aplica el pipeline completo a un bug de una línea o
salta pasos en un cambio estructural. La v1 de PROP-004 definía Bounded como
"cambio acotado en flujo existente" — circular, y la misma forma de
calificativo subjetivo que el piloto Skopos aplicó mal 4/4 veces ("cotidiano
vs crítico", ADR-008) y que PROP-003 §2 rechazó en "trabajo ordinario".

Decisión: clasificación obligatoria al fijar cada TAREA, con clases definidas
por disparadores observables (tabla en `01` §2) y **orden de evaluación
Spike → Architectural → Bounded**. Spike es una declaración firmada en la
TAREA — pregunta escrita y criterio de respuesta — cuyas obligaciones (sin
SPEC, sin merge a `main`, salida con EV-*) hacen que declararla en falso no
eluda proceso. Bounded exige todos sus disparadores: sólo archivos
existentes, sin dependencias nuevas, sin interfaz pública ni contrato
nuevos, sin activar `04` §5.3. Architectural es el resto.
Ratchet ascendente: la clase sube al descubrir complejidad, nunca baja; ante
duda, clase superior. La spec de Bounded vive en la rama o el PR — nunca "en
chat", porque F3 y la ronda adversarial deben poder leerla con contexto
fresco. El código de Spike vive en rama no fusionada o fuera del repo.

Alternativas descartadas:

- **Calificativos ("chico/grande", "cotidiano/crítico")**: desterrados por
  ADR-008 y PROP-003 §2; el ejecutor resuelve la ambigüedad a su favor.
- **No clasificar**: obliga a elegir entre overkill y salto de pasos en cada
  tarea, sin criterio escrito que un tercero pueda auditar.
- **Spec de Bounded "en chat"** (v1): invisible para una sesión nueva; rompe
  la trazabilidad SPEC → test → evidencia y la ronda de contexto fresco.

Consecuencias: la guía gana puerta de entrada para repos existentes; la TAREA
gana el campo `Clase`. La regla ratchet exige re-fijar la TAREA al
reclasificar — coste declarado, preferido a la subestimación silenciosa.
Resuelve **parcialmente** el ítem `pospuesto` del manifiesto: define la
puerta; el procedimiento completo llega con el piloto.

Verificación: `grep -n 'disparador' docs/ai-agent-guide/01-analisis-y-requerimientos.md`
→ la fila Bounded referencia `04` §5.3;
`grep -n "Clase" docs/ai-agent-guide/04-ejecucion-y-verificacion.md`
→ campo en la TAREA.

Procedencia: PROP-004 §2 A-1 (v2), decidida en
`docs/history/PROP-004-decision-2026-08-20.md` tras la ronda
`docs/history/PROP-004-adversarial-2026-08-20.md` (hallazgo HIGH ×2 sobre la
v1). Evidencia de base: `docs/history/piloto-skopos.md` F3 (4/4 aplicaciones
incorrectas del criterio subjetivo).
