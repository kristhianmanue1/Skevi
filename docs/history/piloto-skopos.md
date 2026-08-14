# Retrospectiva — piloto F0→F3 sobre Skopos

**Fecha:** 2026-08-13
**Alcance:** segundo piloto real del método (el primero fue Skevi sobre sí
mismo, ver `piloto-autoaplicacion-skevi.md`). Este es el primero sobre un
proyecto externo, de código real, con dependencias reales (MongoDB,
Ollama) y datos reales de usuario.
**Proyecto piloteado:** `/Users/krisnova/www/aria/Skopos`
**Revisor del propio pipeline construido:** contexto fresco, subagente
separado, ronda adversarial 2026-08-13 (ver commit `ab9f51b` en Skopos)
**Decisión:** `fix-and-retry` sobre el método — el arranque (F0/F1) fue
sólido; la ejecución (F3) acumuló fallos reales que una ronda adversarial
tardía tuvo que corregir de golpe. El método necesita ajustes, no un
rediseño.

## Resultado ejecutivo

F0 y F1 funcionaron bien: problema bien acotado, preguntas abiertas
manejadas correctamente (se detuvo y preguntó en los puntos que cambiaban
diseño: mecanismo de captura, modelo de IA, interfaz de recuperación,
formato de config), specs y contratos testables. F2 fue disciplinado
(cero placeholders, cero dependencias sin confirmar).

F3 es donde se acumularon los problemas. Cuatro tareas de implementación
se cerraron cada una con un `TAREA ... : OK` y una ronda adversarial
"propia" (mía, sin contexto fresco) — hasta que el humano pidió
explícitamente una ronda con contexto fresco real. Esa ronda encontró 3
BLOCKER y 4 HIGH que habían estado "cerrados" en el historial durante
varios commits: una vulnerabilidad de inyección de prompt explotable (se
reprodujo contra el modelo real y filtró un secreto falso a la base de
datos), una condición de carrera real, y un contrato que prometía una
interfaz nunca construida.

La causa raíz no es que la guía no tenga las reglas — las tiene. Es que
son lo bastante subjetivas (o inexistentes en un punto) como para que el
propio ejecutor se las aplicara mal a sí mismo, repetidamente, sin
notarlo. Ver hallazgos.

## Hallazgos sobre el método (no sobre el código de Skopos — ese ya se
corrigió allá)

### F1 — HIGH — la evidencia de F0 no exigió profundidad suficiente antes de que F1 comprometiera diseño

**Problema:** F0 registró (EV-3) los *tipos* de evento presentes en un
rollout real de Codex, pero nunca inspeccionó la forma exacta de un
payload antes de que F1 (`SPEC-001`) fijara el comportamiento de
extracción. F1 asumió un esquema (`payload.type` en
`{message, agent_message, user_message}`) que no existía: el esquema
real usa un único `type: "message"` con un campo `role`.

**Impacto:** la primera implementación de captura extrajo texto vacío en
5 de 5 turnos reales; sólo se detectó al validar contra datos reales
durante F2, no durante F0 o F1 — es decir, dos fases después de donde
debió atraparse.

**Regla de guía implicada:** `01-analisis-y-requerimientos.md` §2.2
pregunta 5 pide "¿qué formatos?" pero el Definition of Ready (§3.2) no
distingue entre "vi que existe" y "vi la forma exacta".

**Propuesta:** agregar al DoD de F0 (§3.2): *"si un REQ depende de un
formato de datos externo citado como evidencia, esa evidencia debe
incluir al menos un ejemplo real completo del formato — no sólo
metadatos o categorías observadas — o queda registrado como PREGUNTA-*
explícita a confirmar antes de que F1 lo use para diseñar."*

### F2 — BLOCKER — la disciplina de ramas no se sostiene sin un remoto que la fuerce

**Problema:** el estándar (§4.1) dice "nunca trabajar directo sobre la
rama principal protegida". Para Skopos, un repo `git init` local sin
remoto todavía, no hay ninguna protección real — y de hecho el ejecutor
(este agente) violó la regla en el 100% de los commits de Skopos (13
commits directos a `main`), pese a haber corregido exactamente este
mismo patrón para Skevi mismo unas horas antes, en la misma sesión.

**Impacto:** sin historial de branch+PR, no quedó ningún checkpoint de
revisión incremental por tarea — toda la corrección llegó de una sola
ronda adversarial tardía, no de revisiones progresivas más baratas de
corregir.

**Propuesta:** el estándar debería ser explícito en que "rama de
trabajo" aplica desde el primer commit, exista o no remoto todavía —
"nunca directo a main" no es una regla condicionada a que exista GitHub.
Agregar al reporte de fase de F3 (00-INDICE.md) un campo: *"rama de este
cierre: <nombre> | main (si main, justifícalo)"* para que sea una
decisión explícita, nunca un olvido silencioso.

### F3 — BLOCKER — el criterio "cotidiano vs crítico" de la ronda adversarial es demasiado subjetivo

**Problema:** `04-ejecucion-y-verificacion.md` §5.3 dice: *"cotidiano,
una ronda propia honesta basta; cambio crítico o release, contexto
fresco real."* Skopos: persiste conversaciones reales de usuario
indefinidamente, alimenta texto no confiable a un LLM cuya salida se
persiste sin validar, y corre con concurrencia potencial (el vigilante).
Ninguno de esos tres hechos es "cotidiano" bajo ninguna lectura razonable
de seguridad — pero cada tarea individual (análisis, almacenamiento,
orquestador+CLI, vigilante) se sentía incremental, y el ejecutor aplicó
la barra baja las cuatro veces.

**Impacto:** código con una inyección de prompt explotable y una
condición de carrera real quedó reportado como `OK` en el historial
durante varios commits, hasta que el humano pidió explícitamente
contexto fresco.

**Propuesta:** sustituir el criterio subjetivo por condiciones
objetivas — si el componente cumple *cualquiera* de estas, la ronda con
contexto fresco (subagente u otro modelo) es obligatoria, no opcional
según "sensación":
1. persiste datos de un usuario real o de terceros;
2. consume salida de un LLM y actúa sobre ella sin revisión humana antes
   de persistirla o ejecutarla;
3. puede ejecutarse con concurrencia (dos instancias, dos procesos);
4. expone una interfaz a un consumidor no controlado por el mismo autor.

### F4 — HIGH — "mínimo necesario" se aplicó también a propiedades de corrección, no sólo a alcance

**Problema:** `00-INDICE.md` reglas 3-4 ("mínimo necesario",
"sin generalidad especulativa") se usaron para justificar no pensar en
condiciones de carrera, no delimitar el prompt contra inyección, y no
validar en el borde de persistencia. Ninguna de esas es "generalidad
especulativa" (una feature que nadie pidió) — son propiedades básicas de
corrección de un requisito que ya estaba aprobado (REQ-3: persistir sin
duplicar; REQ-2: analizar texto no confiable).

**Impacto:** la misma raíz que F3 — bugs de corrección/seguridad
disfrazados de "no lo pidieron, no lo hago".

**Propuesta:** aclarar en `00-INDICE.md` regla 3-4 que "mínimo
necesario" limita **alcance** (features, configurabilidad,
generalización) y nunca **corrección o seguridad de lo que ya está en
alcance**. Agregar la frase: *"mínimo necesario nunca significa omitir
manejo de errores esperables, condiciones de carrera evidentes para el
diseño elegido, o validación de datos no confiables de un requisito ya
aceptado — eso no es 'de más', es la implementación completa de lo
prometido."*

### F5 — MED — el drift entre CONTRATO y código no tiene checkpoint dedicado

**Problema:** el CONTRATO de Skopos prometía un parámetro `offset`/modo
"baseline" que nunca se implementó; la SPEC decía "leído
incrementalmente" cuando no lo era. `04-ejecucion-y-verificacion.md` §9
(gate de F3) sólo tiene "docs y comentarios coherentes con el código",
una casilla genérica que no obliga a comparar campo por campo.

**Propuesta:** agregar al gate de F3, cuando la tarea toca un componente
con CONTRATO: *"cada campo de entrada/salida del CONTRATO existe
literalmente en la firma o esquema real del código — verificado
leyendo/grepeando el código ahora, no de memoria de cuando se escribió
el contrato."*

### F6 — positivo, mantener igual — el mecanismo de preguntas abiertas de F0

Cuando el análisis llegó a decisiones que cambiaban diseño (mecanismo de
captura del CLI, elección de modelo de IA, interfaz de recuperación,
formato de configuración), el proceso se detuvo y preguntó con opciones
y recomendación, en vez de asumir. Evitó varias decisiones equivocadas
silenciosas. No tocar esta parte de la guía.

### F7 — positivo, formalizar — el patrón para requisitos nuevos post-cierre de F0

A mitad del piloto surgió una herramienta no contemplada en el F0
original (escrubery). El patrón que se siguió — parar, investigar contra
el repo real, registrar un REQ nuevo con fuente y un ADR explicando por
qué es opcional/no bloqueante — funcionó limpio y no exigió reabrir todo
el análisis. Hoy este patrón no está descrito en la guía, sólo se
infirió. Vale la pena nombrarlo explícitamente como el procedimiento
correcto para "requisito nuevo después del cierre de F0".

## Verificaciones

- Historial de commits de Skopos (`git log --oneline`) → 13 commits
  locales antes del primer push, todos directos a `main`, cero ramas de
  trabajo, confirmando F2.
- Ronda adversarial de Skopos (subagente, contexto fresco, 2026-08-13) →
  3 BLOCKER, 4 HIGH, reproducidos contra Ollama/MongoDB reales,
  confirmando F3.
- `docs/contratos/f1-contratos.md` de Skopos (versión pre-corrección) vs
  `src/skopos/captura.py` (`extraer_turnos(path)`, sin parámetro
  `offset`) → confirma F5.

## Decisión

`fix-and-retry` — sobre el método, no sobre Skopos (que ya se corrigió).
Las propuestas de F1-F5 quedan para que el humano decida cuáles
incorporar a `docs/guia-agentes-ia/` y `docs/estandar-diseno-software-github.md`;
este documento es evidencia de procedencia, no las aplica por sí mismo.
