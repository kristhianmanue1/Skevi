# PROP-002 — Correcciones al método desde la evidencia de los adoptantes

> **Estado:** borrador en revisión; propuesta no normativa.
> **Audiencia:** agentes de IA que crean o mantienen software con Skevi.
> **Decisión requerida:** aceptar, rechazar o dividir las iniciativas A-1…A-9, y
> ratificar el retiro de nueve iniciativas de PROP-001.
> **Efecto actual:** ninguno; las reglas aplicables siguen viviendo en el
> estándar y la guía.
> **Relación con PROP-001:** no la reemplaza. Corrige su decisión del
> [2026-08-15](PROP-001-decision-2026-08-15.md) con evidencia que esa decisión
> no tuvo a la vista.

## 1. Propósito

PROP-001 razonó sobre qué mejorar en Skevi desde el propio corpus. Esta
propuesta razona desde algo distinto: **qué construyeron por su cuenta los
proyectos que adoptaron Skevi de verdad**, y qué dice eso sobre lo que al método
le falta.

La tesis es sencilla. Cuando un adoptante inventa una pieza que Skevi no le dio,
esa pieza es un hueco del método, no una preferencia del adoptante. Cuando dos
adoptantes independientes inventan la misma pieza, el hueco está confirmado.

## 2. Base empírica

### 2.1 Quiénes son adoptantes

Skevi existe desde el 2026-08-12. Sólo cuatro repositorios son posteriores y lo
usan: `Skopos` (piloto guiado), `ektel`, `alubia` y `emd`. Los repositorios
`argos`, `escrubery`, `agora`, `epistates` y `praxis-dev` son **anteriores**:
comparten prácticas con Skevi porque el método las codificó de ese ecosistema,
no porque las hayan adoptado de él.

Esta distinción se estableció por fecha de primer commit y corrige dos
inferencias previas erróneas registradas en §6.

### 2.2 Qué adoptaron

Las cifras siguientes cuentan **archivos `.md` que contienen cada término con
límites de palabra** (`grep -rlE "\b…\b"`). El método importa: una primera
medición sin límites infló tres de estas cifras entre 18× y 65×, porque `BLOQ`
coincide con "bloqueado" y `F0` con dígitos de un hash. Las cifras infladas
sostuvieron una versión anterior de esta propuesta y la ronda adversarial las
tumbó.

| Práctica | `alubia` | `emd` |
|---|---:|---:|
| fases `F0`–`F3` | **18** | 3 |
| ronda adversarial (frase exacta) | 1 | **41** |
| `fail-closed` | — | **61** |
| contexto fresco | 2 | 6 |
| vocabulario `PARCIAL`/`BLOQ` | 3 | 2 |

`alubia` tomó la maquinaria de fases: 17 ADR, 5 SPEC, F0/F1 cerrados citando a
Skevi, cascarón F2, gate de tamaños, `.skevi/` instalado y un bloque
`skevi:registry` en su `AGENTS.md`. Además **extendió** el gate con una
comprobación propia de credenciales (su ADR-017). Lo que casi no tomó es la
ronda adversarial.

`emd` tomó lo contrario, y es el adoptante más informativo porque aplica el
método a un sistema legado real en producción: ronda adversarial y rigor
fail-closed de forma intensiva, `docs/evidence/` como directorio de primer
nivel, auditorías que reproducen 31,159 rutas con hashes byte a byte — y casi
nada de las fases.

`ektel` tomó sólo la ronda adversarial, y la ejecutó cuatro veces, tres de ellas
declaradas externas.

**El dato central es la disyunción.** Dos adoptantes serios del mismo corpus
eligieron subconjuntos que casi no se solapan, y ninguno de los dos tomó el
vocabulario de estados. No hay un núcleo que todos adopten; hay un corpus del
que cada quien extrae lo que su problema exige.

### 2.3 Qué tuvieron que inventar

| Pieza inventada | Quién | Qué falta en Skevi |
|---|---|---|
| `INDEPENDENT-AUDIT` como artefacto repetido | emd | atestación de independencia |
| "revisión externa" como ronda aparte | ektel | ídem |
| default deny + cuarentena + promoción | emd | procedimiento de baseline |
| hard gates vs soft gates | emd | clases de hallazgo no bloqueante |
| clases D0–D4 de sensibilidad | emd | clasificación de datos |
| gate anti-credenciales | alubia | extensibilidad del gate |
| procedencia fijada a commit `944e72e` | emd | declaración de adopción |

Siete piezas, cuatro adoptantes, dos de ellas inventadas dos veces por separado.

Una octava candidata quedó descartada al verificarla: la exención de gate para
contenido congelado **no** la inventó emd, ya estaba normada en el estándar §3.4
("un documento histórico congelado se exenta"). Se retira de la lista de huecos.

### 2.4 Límites de esta evidencia

Cuatro adoptantes es una muestra pequeña, y los cuatro proyectos son del mismo
autor humano, así que la convergencia puede reflejar un estilo compartido y no
una necesidad universal.

**Sesgo de selección:** `alubia` y `emd` no salieron de la medición. Los señaló
el humano después de que un primer análisis no los encontrara, porque viven
fuera del directorio inspeccionado. Es probable que existan otros adoptantes no
observados.

**Sesgo de supervivencia:** sólo se observan adopciones vivas. Un proyecto que
probó Skevi y lo abandonó no aparece en ninguna medición, y el abandono sería la
señal más informativa sobre qué partes del método estorban.

La medición es además un proxy: cuenta menciones, no uso. Ninguna de las
iniciativas siguientes debería aceptarse porque "los adoptantes lo hicieron",
sino porque el problema que resuelven es real y está descrito.

## 3. Iniciativas

### A-1 — Atestación de independencia de la revisión

**Problema:** la guía (`04` §5.3) define **cuándo** hace falta contexto fresco,
pero no exige registrar **quién** revisó ni con qué contexto. "Ronda adversarial
hecha" es hoy autocertificable, que es exactamente lo que el método prohíbe en
todo lo demás.

**Evidencia:** emd creó `INDEPENDENT-AUDIT` como tipo de artefacto recurrente y
ektel creó "revisión externa". Dos invenciones independientes de la misma pieza.
En sentido contrario: el piloto de autoaplicación de Skevi, la ronda de PROP-001
y el spike de AN-KLA del 2026-08-15 declararon todos ser juez y parte — la
detección dependió de que el ejecutor lo confesara.

**Propuesta:** todo registro de ronda adversarial declara tres campos:
`revisor` (identidad o rol), `contexto` (`fresco` | `mismo`) y, cuando aplique,
`modelo`. Un contexto `mismo` no invalida la ronda: la clasifica. Una ronda sin
los tres campos no cuenta como ronda para efectos de un gate que la exija.

**Polaridad cerrada sobre la procedencia.** El campo lo escribe el mismo
ejecutor, así que por sí solo no prueba nada: sustituiría una autocertificación
por otra. Por eso `fresco` sólo es admisible cuando existe un rastro verificable
por un tercero —identificador de subagente, sesión distinta, modelo distinto
registrado—. Sin ese rastro, el valor obligatorio es `mismo`. **La ausencia de
evidencia degrada, nunca promueve.**

**Aceptación:** ningún gate que exija ronda adversarial puede cerrarse con un
registro que omita los tres campos; un fixture con `contexto: fresco` sin rastro
verificable produce fallo, no advertencia.

### A-2 — Baseline por derivación, no por declaración

**Problema:** PROP-001 P0-06 propuso un estado `BASELINED` pero no un
procedimiento. Aplicar el método a un sistema que ya existe es el caso normal,
no el raro: cinco de los repositorios de este ecosistema son anteriores a Skevi.

**Evidencia:** emd derivó un workspace desde un snapshot de producción con tres
superficies mezcladas y 599 MiB de document root, y para hacerlo inventó un
procedimiento completo que Skevi no tenía.

**Condición de aplicación.** El procedimiento completo es proporcionado para
derivar un workspace desde 599 MiB de producción con datos clínicos; imponerlo a
un repositorio Git propio y limpio contradice la regla 3 del índice ("mínimo
necesario"). A-2 se activa por disparadores observables, reutilizando los que la
guía ya define en `04` §5.3: el origen no es un repositorio Git propio y limpio,
o contiene datos de terceros o secretos. Fuera de esos casos basta documentar
las fases anteriores como `recuperadas`.

**Propuesta:** cuando se activa, adoptar el vocabulario de emd tal cual, sin
acuñar sinónimos:

- **default deny** sobre el material de origen; nada entra por omisión;
- **allowlist** que permite llevar un candidato a **cuarentena** local ignorada
  por Git — y que explícitamente *no* afirma que el archivo sea seguro;
- **promoción** al repositorio sólo con manifiesto exacto, escaneo de secretos,
  y revisión de configuración, rutas y endpoints;
- fases anteriores documentables como `recuperadas`, nunca como evidencia
  histórica de cumplimiento.

**Aceptación:** un fixture con un origen mixto llega a baseline sin mutar el
origen, sin declarar `F0: OK` retroactivo, y con cada archivo promovido
trazable a su entrada de allowlist y a su manifiesto.

### A-3 — Separar hallazgo bloqueante de hallazgo registrable

**Problema:** Skevi tiene `BLOQ` y `PARCIAL`, pero no distingue entre lo que
detiene la tarea y lo que se corrige sin detener nada. En la práctica eso empuja
a dos errores opuestos: paralizar por un detalle de formato, o degradar a
`PARCIAL` un hallazgo que debía detener.

**Evidencia:** emd separó **hard gates** —secreto o dato personal fuera de la
bóveda, riesgo de pérdida de datos, operación destructiva sin autorización,
drift no atribuible, fallo de autorización, imposibilidad de verificar— de
**soft gates** —recibo con formato imperfecto, documentación auxiliar
incompleta, límite de tamaño heredado en contenido congelado, fallo de una
herramienta cuando existe evidencia equivalente reproducible.

**Propuesta:** incorporar la distinción a la capa normativa. Un hard gate
bloquea la tarea afectada; un soft gate se registra y se corrige sin paralizar
tareas independientes.

**La lista cerrada es la de soft, no la de hard.** Es la corrección crítica
respecto del modelo de emd. El fallo mejor documentado del método es que el
ejecutor, ante dos niveles de rigor, elige el bajo — 4 de 4 veces en el piloto
Skopos, sobre un componente con inyección de prompt explotable. Una categoría no
bloqueante abierta le entrega esa misma palanca. Por eso **todo hallazgo no
enumerado explícitamente como soft es hard por defecto**, que es la misma
polaridad cerrada que el estándar ya aplica a los límites de tamaño (§3.4).
emd puede sostener el modelo abierto porque tiene controlador humano y auditor
independiente; un adoptante en solitario, no.

**Aceptación:** cada gate del corpus queda clasificado; la lista de soft gates
es enumerada y finita; ningún hallazgo fuera de esa lista puede cerrarse como
`PARCIAL`. Sin el cierre, esta iniciativa se rechaza.

### A-4 — Clasificación de sensibilidad con cláusula anti-exceso

**Problema:** Skevi no dice nada sobre sensibilidad de datos. Un agente que
encuentra material sensible improvisa, y la improvisación falla en las dos
direcciones: filtrar, o paralizarse ante material que sólo *parece* sensible.

**Evidencia:** emd definió cinco clases —`D0` público, `D1` lógica de dominio,
`D2` operacional o secreto, `D3` dato personal vinculable, `D4` sintético o
desidentificado— y añadió una cláusula que Skevi no habría escrito sola: *"el
tema médico no convierte automáticamente un archivo en PHI"*. Código, catálogos
y cálculos son lógica de dominio que debe conservarse y probarse.

**Propuesta:** llevar al estándar una clasificación mínima y genérica, con la
cláusula anti-exceso explícita: la sensibilidad se decide por el vínculo con una
persona o un secreto, nunca por el tema del proyecto. La clasificación concreta
la fija cada proyecto; el estándar fija que debe existir y qué no puede hacer.

**Aceptación:** el corpus distingue "no se toca" de "se trata con cuidado", y un
fixture de lógica de dominio dentro de un proyecto sensible no queda bloqueado
por asociación temática.

### A-5 — El contrato de tarea son campos, no un formato

**Problema:** PROP-001 P0-03 propuso representar cada tarea en JSON para poder
validarla. Sin validador, un JSON obligatorio es ceremonia; con validador, es
una barrera para instrucciones breves que ya contienen todo lo necesario.

**Evidencia:** emd define ocho campos —ID y objetivo, base con SHA, entradas
permitidas, rutas legibles y editables, operaciones autorizadas, prohibiciones,
checks ejecutables, hard stops— y añade: *"no se exige una tarjeta extensa
cuando una instrucción breve contiene todos los campos. El formato nunca
prevalece sobre la corrección verificable."*

**Propuesta:** retirar P0-03 y normar los campos, no la representación. Lo que
se exige es que los ocho estén resueltos y sean citables; da igual si viven en
una tarjeta, un issue o un mensaje.

**Intercambio declarado:** esto gana flexibilidad y **pierde** la validación
automática que era el argumento de P0-03. Es deliberado —sin ejecutable, esa
validación no existía de todos modos— pero no es una mejora sin coste: si algún
día hay validador, A-5 habrá que revisarla.

**Aceptación:** una instrucción breve que resuelve los ocho campos pasa el
preflight; una tarjeta extensa a la que le falta el SHA base, no.

### A-6 — Gate extensible con exenciones declaradas

**Problema:** el gate de Skevi comprueba tamaños y estructura, y nada dice sobre
si un adoptante puede añadirle comprobaciones propias. Un proyecto con un riesgo
específico no sabe si extenderlo es adopción correcta o desviación del método.

**Alcance reducido tras verificación.** Las exenciones declaradas **ya están
normadas**: el estándar §3.4 dice que exentar es una decisión que se registra
con su motivo y que un documento histórico congelado se exenta. Esa mitad se
retira de esta iniciativa; emd aplicó una regla existente, no inventó una.

**Evidencia de lo que sí falta:** alubia añadió una comprobación
anti-credenciales por su cuenta (ADR-017), sin que el corpus dijera si eso era
legítimo.

**Propuesta:** el estándar declara que el gate es **extensible por proyecto**:
comprobaciones adicionales son adopción correcta, no desviación, y se registran
junto a las exenciones que ya norma §3.4.

**Aceptación:** un proyecto puede añadir un check propio sin quedar en
incumplimiento, y el check queda legible en su configuración de gate.

### A-7 — Declaración de adopción con procedencia fijada

**Problema:** copiar el corpus crea forks silenciosos. Hoy es imposible saber
qué tomó un adoptante y qué dejó deliberadamente.

**Evidencia:** el 100% de los adoptantes tomó un subconjunto. emd ya resolvió la
parte difícil por su cuenta: su estándar declara *"adaptación selectiva de
Skevi, commit `944e72e`… No es una copia del corpus Skevi"*. alubia instaló
`.skevi/` y un bloque `skevi:registry` en su `AGENTS.md`.

**Propuesta:** retirar el esquema de manifiesto de P0-02 y normar el patrón que
ya existe: el adoptante declara **procedencia fijada a un commit**, **qué
adoptó** y **qué dejó deliberadamente**. Tres líneas en un archivo que el
proyecto ya tiene. Nada de esquema de configuración nuevo.

**Aceptación:** dado un repositorio adoptante, un agente puede responder qué
versión del método sigue y qué partes no aplican, leyendo un solo archivo.

### A-8 — Disparadores objetivos donde hoy hay calificadores

**Problema:** `material`, `no trivial` y `críticos` aparecen sin definición y
son la condición que dispara ronda adversarial, contratos y threat model.

**Evidencia:** en el piloto Skopos, ante el calificador "cotidiano vs crítico",
el ejecutor eligió la barra baja 4 de 4 veces sobre un componente con inyección
de prompt explotable. Cuando se sustituyó por cuatro condiciones observables
(`04` §5.3), el problema desapareció. Es el único patrón de corrección con
eficacia demostrada en este repositorio.

**Propuesta:** aplicar el mismo tratamiento a los calificadores restantes,
derivando el rigor de disparadores observables. Es P1-03 de PROP-001, sin
cambios, incorporada aquí por continuidad de evidencia.

**Aceptación:** ningún calificador subjetivo queda como única condición de un
requisito de rigor.

### A-9 — Toda regla de revalidación nombra su ancla

**Problema:** una regla del tipo "revalida contra X antes de actuar" es
incumplible si el artefacto regulado no dice contra qué X revalidarse.

**Evidencia:** el 2026-08-15, un checkpoint de AN-KLA íntegro y firmado
declaraba un estado de hace dos días; el desfase fue indetectable porque el
schema no permitía ligar el checkpoint al commit que describía. Cumplir la regla
exigía descartar el artefacto que la regla gobierna.

**Propuesta:** regla transversal — todo artefacto sujeto a revalidación carga el
identificador verificable contra el cual se revalida. Y un barrido de las reglas
existentes del corpus que digan "revalidar", "verificar contra" o equivalente.

**Aceptación:** ninguna regla de revalidación del corpus queda sin ancla
nombrada.

## 4. Retiro de iniciativas de PROP-001

Esta propuesta pide **rechazar** lo siguiente, no diferirlo:

| Iniciativa | Motivo |
|---|---|
| P0-00 comandos de inspección | Los adoptantes produjeron evidencia auditable con hashes reproducidos **sin herramienta alguna**. Lo que les faltó fue vocabulario normativo, no tooling. Un agente ya lee el árbol y ejecuta git; un CLI añade superficie de seguridad para entregar lo que ya tiene. |
| P0-02 manifiesto de adopción | Sustituida por A-7 a una fracción del coste. |
| P0-03 contrato JSON | Sustituida por A-5. |
| P0-05 gates semánticos F0-F3 | El patrón real observado es gate extensible por proyecto (A-6), no verificador de fase centralizado. Ningún adoptante pidió gates de fase. |
| P0-07 adopción transaccional | Depende de `adopt`, que muere con P0-00. |
| P1-02 grafo de trazabilidad | Depende de P0-05. |
| P1-05 lease de escritor | Resuelve un problema de la orquestación `tmux`, no del método. |
| P2-02 contexto compilado | El corpus cabe en una lectura y `00-INDICE.md` ya cumple esa función. |
| P2-03 suite de evaluación | Depende del ejecutable inexistente. |
| P0-04 vocabulario de estados | Es lo que **menos** viaja de todo el corpus: 2 archivos en emd, 3 en alubia. Una versión anterior de esta propuesta lo revivió citando 130 archivos; esa cifra era un artefacto de medición y la ronda adversarial la refutó. |

Se conservan de PROP-001: **P0-01** (autoridad documental), **P0-06** (absorbida
y concretada por A-2), **P1-01** (recibos: emd los construyó a mano, luego el
problema existe), **P1-03** (= A-8) y **P1-04** (cambio de requisitos, única
deuda del piloto Skopos sin saldar).

**P2-01** (versión, distribución y desviaciones) queda **parcialmente
sustituida** por A-7, que cubre la declaración de procedencia fijada. La mitad
no cubierta sigue abierta y se registra aquí como pendiente: qué ocurre cuando
el método avanza y el adoptante quedó anclado a un commit. Un adoptante con
procedencia fijada y sin procedimiento de actualización acumula drift
silencioso, que es justo lo que P2-01 existía para evitar. Requiere decisión
propia; esta propuesta no la toma.

## 5. No objetivos

- No convertir a Skevi en una herramienta ejecutable.
- No obligar a ningún adoptante a adoptar el corpus completo: la adopción
  parcial es el caso normal y el método debe soportarla explícitamente.
- No importar el dominio de emd —clínico, PHI, Moodle— al corpus de Skevi. Se
  absorbe la forma, no el contenido.
- No tratar la convergencia entre adoptantes como prueba de necesidad universal.
- No normar nada de esta propuesta sin ADR propio por iniciativa aceptada.

## 6. Procedencia y razón

**Procedencia:** análisis solicitado por el humano el 2026-08-15, sobre los
repositorios `Skopos`, `ektel`, `alubia` y `emd`, y sobre los hallazgos de
`docs/history/piloto-skopos.md` y `docs/history/drift-checkpoint-an-kla-2026-08-15.md`.
El vocabulario de A-2, A-3, A-4 y A-5 procede de
`docs/standards/EMD-AGENT-WORK-STANDARD.md` y `EMD-DATA-CLASSIFICATION.md` del
repositorio `emd`, adoptados deliberadamente sin renombrar.

**Razón:** el análisis que produjo esta propuesta se corrigió **tres** veces, y
las tres correcciones dicen más sobre el método que varias de las iniciativas.

1. Se leyeron cinco repositorios anteriores a Skevi como si fueran adoptantes;
   las fechas de primer commit lo refutaron.
2. Se concluyó que "la capa de proceso no viaja"; cayó al incorporar `alubia` y
   `emd`, que el humano tuvo que señalar porque viven fuera del directorio
   inspeccionado.
3. Las cifras de adopción resultaron infladas hasta 65× por medir sin límites de
   palabra —`BLOQ` coincide con "bloqueado"—, y una de ellas había servido para
   revivir una iniciativa previamente rechazada. Lo detectó la ronda adversarial
   de esta misma propuesta.

Las tres tuvieron la misma raíz: **inferir sobre la muestra o la medición
disponible, sin establecer primero si eran las correctas.** Queda registrado
porque es exactamente el error que un agente comete al analizar un ecosistema
desde un solo directorio con un `grep` cómodo, y porque las tres veces la
corrección vino de fuera del razonamiento —de una fecha, de un humano, de una
comprobación con límites de palabra—, nunca de razonar más.

## 7. Decisión requerida

Por cada iniciativa A-1…A-9: `accepted | rejected | deferred`, con dependencias
y responsable del siguiente artefacto. Por cada retiro de §4: ratificar o
rechazar. Una iniciativa aceptada requiere ADR antes de modificar el estándar o
la guía.
