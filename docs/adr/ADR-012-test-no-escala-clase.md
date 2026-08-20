# ADR-012: Los archivos de test nuevos no escalan la clase de una tarea

Estado: aceptado; refina el disparador 1 de Bounded definido en
ADR-009. El resto de ADR-009 sigue vigente sin cambios.

Contexto: durante el primer piloto de ADR-009 sobre un repo existente
(`docs/history/piloto-orbitanova.md`), el disparador 1 de Bounded ("toca
sólo archivos existentes en disco") leído literal clasifica como
Architectural cualquier corrección de bug con test de regresión, porque todo
test nuevo es un archivo nuevo. Eso pelea contra el estándar §3.2, que
ordena corregir un bug con un test reproductor donde hay infraestructura de
tests: bajo la lectura literal, cumplir §3.2 siempre escala la clase — el
disparador contradice la norma que sirve (hallazgo PF-1).

Decisión: el disparador 1 de Bounded queda: "toca sólo archivos de
**producción** existentes en disco". Corte observable: **archivo de test es
el que sólo ejecutan los comandos de test declarados del proyecto**
(`package.json`, `AGENTS.md` o equivalente); todo lo demás es producción.
Los archivos de test nuevos —incluidos helpers y fixtures que viven bajo el
árbol de tests— no escalan la clase. Dos cercos: un "test" que añade una
dependencia escala por el disparador de dependencias nuevas; y la exención
cubre tests proporcionales al cambio que cubren, no desarrollo de
infraestructura de prueba bajo la etiqueta de test (eso es producción: lo
ejecuta o consume algo más que el comando de test).

Alternativas descartadas:

- **Lectura literal ("todo archivo nuevo escala")**: convierte cumplir §3.2
  en cambio arquitectural; el piloto lo registró como defecto.
- **Corte por directorio (`tests/` es test, lo demás producción)**: frágil —
  co-localización (`__tests__/`, `foo.test.js` junto al fuente) y monorepos
  lo rompen; el corte por "quién lo ejecuta" es el observable real.
- **No normar y confiar en "ante duda, clase superior"**: la duda se
  dispararía exactamente en cada fix con test — el caso más común.

Consecuencias: la fila Bounded de `01` §2 cita este ADR como procedencia.
ADR-009 queda anotado en su Estado. El agujero del "test" gigante queda
cercado por proporcionalidad y por el disparador de dependencias; su
aplicación es auditable con los comandos declarados del proyecto.

Verificación: `grep -n "producción" docs/ai-agent-guide/01-analisis-y-requerimientos.md`
→ la celda Bounded con el corte observable y la cita a este ADR;
`grep -n "ADR-012" docs/adr/00-INDICE.md` → fila registrada.

Procedencia: `docs/history/piloto-orbitanova.md` § PF-1 (2026-08-20);
estándar §3.2 ("Un bug se corrige con un test que lo reproduce primero");
ADR-009 como decisión refinada.
