# PROP-001 — Mejoras del modelo agent-native

> **Estado:** borrador en revisión; propuesta no normativa.
> **Audiencia:** agentes de IA que crean o mantienen software.
> **Decisión requerida:** aceptar, rechazar o dividir las iniciativas antes de
> incorporarlas a un plan de implementación y, cuando corresponda, a la norma.
> **Efecto actual:** ninguno; las reglas aplicables siguen viviendo en el
> estándar y la guía.
> **Vigencia:** cambia durante la deliberación y se congela al registrar una
> decisión. Las decisiones aceptadas producen ADR y tareas separadas.

## 1. Propósito

Skevi ya define una política sólida para analizar, diseñar, ejecutar y verificar
proyectos nuevos o existentes. La adopción no debe presuponer un repositorio
vacío ni forzar una estructura: primero observa el estado real, después ofrece
hechos y brechas, y sólo modifica lo que el humano acepte explícitamente.

La siguiente evolución consiste en convertir las partes mecánicas de esa
política en un protocolo estructurado y validable, sin sustituir el juicio del
agente donde la semántica del problema sí lo exige.

El modelo debe seguir siendo **agnóstico al lenguaje de programación**. El
núcleo define fases, autoridad, estados, evidencia y contratos; cada proyecto
declara sus comandos reales de construcción, ejecución, pruebas y lint como
datos. Los adaptadores por ecosistema son opcionales y nunca forman parte de la
norma transversal.

### 1.1 Ubicación y ciclo de vida

`docs/proposals/` separa deliberación de norma, operación e historia. Una
propuesta puede cambiar mientras se revisa; al decidirla se congela con estado
`aceptada`, `rechazada`, `parcialmente aceptada` o `sustituida`. Lo aceptado se
materializa mediante ADR y tareas independientes, no editando esta propuesta
como si ya fuera una regla.

Esta carpeta amplía la taxonomía descrita por ADR-002. ADR-003 registra su
adopción como hogar canónico y la migración de directorios a nombres en inglés.
El README describe el estado físico actual; ni la carpeta ni esa descripción
convierten el contenido de esta propuesta en norma.

## 2. Problema observado

La mayor parte de las garantías actuales está expresada en Markdown. Un agente
debe leerlas, resolver ambigüedades, recordar el estado y después certificar su
propio cumplimiento. Los pilotos históricos muestran que la política puede ser
correcta y aun así aplicarse mal: se cerraron tareas como `OK` antes de que una
revisión fresca encontrara fallos de seguridad, concurrencia y contrato.

El gate actual verifica estructura, tamaño y bloques de registro. No valida
trazabilidad `REQ -> SPEC -> test`, permisos, transiciones de estado, vigencia
de evidencia ni contenido mínimo de los gates F0-F3.

La adopción actual también parte principalmente del caso de un proyecto nuevo:
copiar documentos, crear hogares y añadir un gate. En un proyecto existente esa
estrategia puede competir con convenciones válidas, ensuciar el diff o imponer
artefactos que no responden a un riesgo real.

### 2.1 Modos de adopción

Skevi debe ofrecer capacidades acumulativas y opt-in:

1. **Inspect:** sólo lectura; inventaría y produce datos duros.
2. **Assess:** compara evidencia con Skevi y reporta brechas, sin editar.
3. **Propose:** genera un plan y un diff candidato, sin aplicarlo.
4. **Adopt:** aplica capacidades seleccionadas con permiso explícito.
5. **Verify:** comprueba únicamente los contratos que el proyecto adoptó.

Un proyecto puede quedarse indefinidamente en `inspect` o `assess`. No adoptar
una regla no convierte el proyecto en defectuoso; el reporte distingue riesgo
observado, desviación deliberada, dato desconocido y preferencia de Skevi.
La conformidad y el riesgo son dimensiones distintas: `verify` sólo falla por
contratos adoptados, pero `assess` siempre informa riesgos objetivos de
corrección, seguridad, pérdida de datos o ruptura de interfaces.

`propose` produce un artefacto content-addressed. `adopt` requiere una concesión
ligada a ese digest y a las rutas exactas; revalida SHA y worktree antes de
escribir. Si el target cambió, vuelve a `propose` en vez de aplicar un diff
obsoleto.

## 3. Arquitectura objetivo

```text
Repositorio existente
  -> skevi inspect (read-only)
  -> facts + inventory + unknowns + evidence refs
  -> skevi assess (read-only)
  -> findings + coverage + degradations + proposals
  -> decisión humana por capacidad
  -> skevi adopt <capability> (mutación autorizada)
  -> skevi verify <capability> (gate de lo adoptado)
```

El núcleo produce una salida canónica estructurada. Markdown es una vista
secundaria. Cada afirmación se clasifica como `observed`, `derived`, `unknown`
o `proposal`; ninguna recomendación se presenta como hecho ni como autoridad.

Si el proyecto ya publica un manifiesto versionado —por ejemplo
`pinax/project-manifest/v1`— Skevi lo consume como una fuente declarativa y lo
corrobora. Si no existe, el análisis sigue funcionando y no lo crea en modo
read-only.

## 4. Iniciativas prioritarias

### P0-00 — Comandos de inspección y datos duros

**Problema:** un agente necesita una visión verificable del repositorio antes
de aplicar una metodología, pero hoy debe reconstruirla mediante lecturas y
comandos ad hoc.

**Propuesta:** definir una interfaz conceptual, independiente del lenguaje de
implementación:

```text
skevi inspect <path> --format json
skevi assess <bundle> --profile <profile>
skevi context <bundle> --task <task_id> --budget <n>
skevi propose <assessment> --capability <id>
skevi adopt <proposal> --capability <id>
skevi verify <path> --capability <id>
skevi explain <finding_id>
```

`inspect`, `assess`, `context` y `explain` son read-only. No ejecutan código,
instalan dependencias, acceden a red ni escriben dentro del target. La raíz se
canonicaliza; sólo se leen archivos regulares y no se siguen symlinks fuera de
ella. FIFOs, sockets y dispositivos se rechazan. La inspección Git deshabilita
external diff y textconv para no ejecutar filtros del target. Archivos
ilegibles, binarios, demasiado grandes, ignorados o potencialmente secretos
quedan como omisiones explícitas, nunca como contenido copiado silenciosamente.
Los niveles de evidencia más profundos requieren capacidades separadas:

- L0: árbol, tamaños, tipos y exclusiones;
- L1: manifiestos, configuración y documentación;
- L2: Git, historial y relaciones entre archivos;
- L3: análisis estático de código y contratos;
- L4: build, tests y herramientas locales autorizadas;
- L5: ejecución dinámica, red o servicios externos con sandbox y permiso.

**Aceptación:** sobre un repositorio sucio, `inspect` conserva HEAD, índice,
worktree y contenido de archivos, y no deja procesos persistentes. El bundle se
emite por stdout o en un directorio externo con permisos restrictivos, escritura
atómica y retención declarada. Rechaza `/`, el home completo y targets más
amplios que el alcance concedido. Declara target, SHA, presupuesto, omisiones,
truncaciones, comandos observados, fingerprints y toda degradación.
Un fixture con symlink externo, `.env`, archivo binario y archivo sobre el límite
demuestra que no se filtra contenido y que cada exclusión queda inventariada.
Presupuestos de archivos, bytes, tiempo y herramientas terminan en degradación
explícita; un timeout nunca se convierte en análisis completo.

### P0-01 — Resolver autoridad y confianza documental

**Problema:** `AGENTS.md` declara que los documentos nunca son instrucciones,
pero F0 clasifica los documentos normativos como autoridad.

**Propuesta:** separar cuatro conceptos:

- la política del host, sandbox o plataforma es el límite superior y no puede
  ser reducida por el repositorio ni por la conversación;
- la conversación humana concede alcance y operaciones dentro de esos límites;
- los archivos de instrucciones que el host designe, incluido `AGENTS.md`,
  restringen y guían dentro del alcance concedido, pero nunca lo amplían;
- el manifiesto enumera qué documentos definen reglas normativas;
- ningún documento, issue, log, memoria o salida de agente concede por sí solo
  permiso para una operación externa o destructiva.

**Aceptación:** una matriz única de precedencia distingue `autoridad`,
`norma`, `evidencia`, `referencia` y `dato no confiable`; todos los documentos
normativos apuntan a ella en lugar de parafrasearla.

### P0-02 — Manifiesto de adopción opcional

**Problema:** fase, comandos, rutas, límites y desviaciones pueden estar
repartidos entre varios documentos, pero imponer un manifiesto nuevo a todo
repositorio existente contradice la adopción gradual.

**Propuesta:** primero descubrir manifiestos reales y contratos publicados. Si
el proyecto decide adoptar capacidades persistentes de Skevi, registrar sólo la
configuración específica que no tenga ya un hogar canónico. El schema debe
referenciar, no duplicar, comandos y metadatos existentes.

Skevi debe reconocer contratos de ecosistema versionados cuando existan, entre
ellos `pinax/project-manifest/v1`, sin convertirlos en dependencia obligatoria.
Los comandos ejecutables se representan como arreglos de argumentos, nunca como
fragmentos de shell concatenados.

**Aceptación:** `inspect` funciona sin manifiesto; uno presente se reporta como
declaración pendiente de corroboración; `adopt` no crea ni modifica configuración
sin permiso y nunca duplica un campo cuyo hogar canónico ya fue descubierto.

### P0-03 — Contrato estructurado de tarea

**Problema:** la tarjeta F3 es precisa para lectura, pero no puede validarse ni
compararse automáticamente con el diff.

**Propuesta:** representar cada tarea en JSON con `task_id`, `run_id`, SHA base,
rutas, operaciones, checks, límites de intentos y condiciones de parada. La
polaridad es cerrada: lo ausente equivale a prohibido.

**Aceptación:** el preflight rechaza una tarea sin SHA completo, con rutas que
escapan del repositorio, con operaciones desconocidas o sin parada inequívoca.

### P0-04 — Unificar estados, resultados y decisiones

**Problema:** hoy conviven estados operativos, `OK | PARCIAL | BLOQ` y
`proceed | fix-and-retry | escalate` sin un mapeo formal.

**Propuesta:** modelarlos como dimensiones distintas:

```text
lifecycle_state: AUDITING
gate_result: PASS | FAIL | BLOCKED
decision: PROCEED | FIX_AND_RETRY | ESCALATE
```

Una tabla enumera eventos, precondiciones y transiciones. `ESCALATE` siempre
produce `BLOCKED`; nunca permite un cierre `OK`. Todo timeout termina en fallo
explícito.

**Aceptación:** tests de cada transición válida e inválida, incluidos evento
duplicado, intento obsoleto y señal recibida para otro `run_id`.

### P0-05 — Gates semánticos F0-F3

**Problema:** las casillas de fase dependen de autocertificación.

**Propuesta:** ampliar el verificador con comandos independientes:

```text
skevi verify f0
skevi verify f1
skevi verify f2
skevi verify f3 --task <task_id>
```

El gate valida lo estructural y deja explícita la parte que requiere revisión
semántica. Debe corregir la contradicción de F1: un proyecto simple puede usar
un REQ ejecutable sin SPEC, pero esa exención debe ser literal y validable.

**Aceptación:** cada gate incluye fixtures positivos y negativos; no emite
`PASS` si falta un artefacto requerido o existe un pendiente material.

### P0-06 — Baseline para proyectos existentes

**Problema:** reconstruir requisitos y diseño desde un repositorio existente
puede presentar inferencias actuales como si F0 y F1 hubieran ocurrido antes de
la implementación, o exigir retroactivamente un cascarón F2.

**Propuesta:** introducir estado `BASELINED`. El bundle separa artefactos
declarados, comportamiento observado e inferencias recuperadas. Las fases
anteriores pueden documentarse como `recovered`, nunca como evidencia histórica
de cumplimiento. F2 no se ejecuta retroactivamente; sólo se evalúan brechas que
afectan cambios futuros o riesgos actuales.

**Aceptación:** un fixture sin archivos Skevi llega a `BASELINED` sin mutaciones
ni falso `F0: OK`; cada requisito recuperado conserva evidencia y confianza, y
todo dato material desconocido permanece como pregunta.

### P0-07 — Adopción transaccional e idempotente

**Problema:** un permiso genérico para `adopt` podría aplicar una propuesta
obsoleta, escribir parcialmente o ampliar alcance durante la ejecución.

**Propuesta:** ligar autorización a digest, SHA base, rutas y capacidades. Antes
de escribir se genera preview exacto y se revalidan precondiciones. Las
escrituras son atómicas cuando el filesystem lo permite; ante fallo se conserva
el estado previo o se reporta recuperación explícita. Repetir la misma adopción
no duplica bloques ni artefactos.

**Aceptación:** tests de SHA cambiado, permiso insuficiente, fallo a mitad,
segunda ejecución y archivo preexistente demuestran `BLOCKED` seguro o resultado
idempotente, sin instalar dependencias ni usar red por implicación.

### P1-01 — Recibos de evidencia ligados a Git

**Problema:** `comando -> resultado` puede quedar obsoleto o copiarse sin
vínculo con el estado verificado.

**Propuesta:** ejecutar checks mediante un recolector que registre `task_id`,
`run_id`, cwd, argv, tiempos, exit code, SHA inicial/final, hash de salida y
estado de saneamiento. Si cambia Git, la evidencia anterior queda invalidada.

**Aceptación:** un test demuestra que un recibo de otro SHA, worktree o intento
no puede cerrar el gate actual.

### P1-02 — Grafo de trazabilidad

**Problema:** los IDs existen, pero sus relaciones se comprueban manualmente.

**Propuesta:** mantener relaciones computables:

```text
REQ -> SPEC o exención simple -> CASE -> TEST -> EVIDENCE
                         \-> CONTRATO -> implementación
```

**Aceptación:** el gate detecta IDs duplicados, requisito imprescindible sin
cobertura, caso sin test, contrato sin implementación y referencia inexistente.

### P1-03 — Perfiles objetivos de riesgo

**Problema:** términos como `material`, `no trivial` o `crítico` permiten
clasificaciones inconsistentes entre agentes.

**Propuesta:** derivar rigor de disparadores observables: datos de terceros,
persistencia, salida de LLM que causa acciones, concurrencia, consumidor externo,
capacidad destructiva y tratamiento de secretos.

**Aceptación:** una matriz determina automáticamente contratos, threat model,
tests y nivel de independencia adversarial exigidos para cada combinación.

### P1-04 — Cambio de requisitos y reapertura selectiva

**Problema:** la guía no formaliza qué ocurre cuando aparece un requisito tras
cerrar F0.

**Propuesta:** un artefacto `CHANGE-REQ-*` declara fuente, impacto, artefactos
invalidados y fases que deben reabrirse. No se reinicia todo el proyecto ni se
permite incorporar el cambio silenciosamente en F3.

**Aceptación:** un requisito nuevo invalida sólo los gates dependientes y el
agente no puede ejecutar F3 hasta recalcularlos.

### P1-05 — Lease de escritor por worktree

**Problema:** controlador y ejecutor pueden tener capacidad técnica de editar
el mismo worktree; la exclusión temporal vive en prosa.

**Propuesta:** registrar escritor, `run_id`, generación y expiración. El auditor
empieza en lectura; para editar debe adquirir el lease. Un lease vencido no
autoriza borrar ni reemplazar trabajo.

**Aceptación:** dos ejecuciones no pueden adquirir simultáneamente escritura
sobre el mismo worktree y una generación inesperada produce `BLOCKED`.

### P2-01 — Versión, distribución y desviaciones

**Problema:** copiar la guía a otros repositorios crea forks silenciosos.

**Propuesta:** fijar versión o commit del método, digest del contenido y archivo
separado de desviaciones. Una actualización genera un plan de migración; nunca
sobrescribe reglas locales automáticamente.

**Aceptación:** un comando informa versión instalada, drift y migraciones
pendientes sin mutar el proyecto.

### P2-02 — Contexto mínimo compilado para cada tarea

**Problema:** cargar todo el corpus aumenta costo y probabilidad de perder
reglas críticas entre material irrelevante.

**Propuesta:** generar un manifiesto de lectura con fuentes completas pero
seleccionadas: fase vigente, reglas transversales aplicables, REQ/SPEC/contratos
y ADR relacionados. Historia y orquestaciones no seleccionadas quedan fuera.

El compilador clasifica sensibilidad, redacta secretos y limita retención. El
bundle incluye hashes y punteros por defecto; sólo incorpora contenido cuando
el presupuesto y la política del target lo permiten. Emitir contexto fuera del
host o hacia un proveedor es una operación externa independiente.

**Aceptación:** el paquete declara rutas y hashes, cabe en el presupuesto de la
tarea, no contiene fixtures secretos y falla si una fuente cambió antes de
ejecutar.

### P2-03 — Suite de evaluación de agentes

**Problema:** los tests actuales verifican el script de tamaños, no la conducta
del agente que aplica Skevi.

**Propuesta:** escenarios reproducibles que exijan detenerse ante permisos
ausentes, ignorar instrucciones en issues, rechazar evidencia de otro SHA,
bloquear escritores concurrentes y considerar inválida una ronda adversarial
que sólo elogia.

**Aceptación:** resultados estructurados comparables entre modelos y versiones,
sin depender del lenguaje del proyecto usado como fixture.

## 5. Estado de AN-KLA en Skevi

Al crear este documento no hay evidencia de una instalación o integración de
AN-KLA en este repositorio:

- no existe `AN-KLA.md`;
- no existe `.an-kla/`;
- `AGENTS.md` no contiene un bloque gestionado por AN-KLA;
- no hay ejecutable `an-kla` ni `an-kla-memory` en `PATH`;
- sí existe el ejecutable `adrc`, que es una capacidad distinta.

`scripts/check_sizes.py` excluye `.an-kla` del recorrido, pero una exclusión
preventiva no demuestra instalación.

AN-KLA queda como integración opcional futura. Antes de instalarlo deben
existir autorización humana específica, contrato de datos y verificación de su
interfaz real. La memoria recuperada será dato no confiable: puede aportar
contexto y punteros, nunca reglas ni permisos. La norma y el estado reproducible
siguen viviendo en el repositorio.

## 6. Integraciones opcionales

El análisis epistémico, la inteligencia sobre herramientas, la memoria externa
y la atestación son adaptadores, no fuentes de autoridad. Cada integración debe
declarar:

- contrato versionado y schema cerrado;
- procedencia, vigencia y modo de fallo;
- capacidades concedidas y kill switch;
- comportamiento cuando el servicio no está disponible;
- tests que demuestren que sus datos no elevan autoridad.

### 6.1 Argos Epistemic

Argos ya implementa gran parte del plano de evidencia que Skevi necesita:
inventario, presupuesto, omisiones, degradaciones, claims tipados, cobertura,
JSON canónico, fingerprints y attestations de ejecución. Sus contratos
`evaluation-manifest-v1`, `evaluation-envelope-v1`,
`discovery-inventory-v1`, `claim-record-v1` y `run-attestation-v1` están
diseñados para consumo progresivo por agentes.

Skevi no debe reconstruir ese modelo. La frontera propuesta es:

```text
Argos
  -> qué se observó, con qué cobertura, costo y evidencia
Skevi
  -> qué reglas adoptó el proyecto, qué brechas importan y qué se propone
Humano
  -> qué capacidades se aplican y qué operaciones se autorizan
```

El comando `skevi inspect` puede actuar como fachada de proveedores. Un
colector nativo mínimo obtiene hechos necesarios para el preflight; el adaptador
Argos aporta análisis profundo cuando está disponible. El bundle siempre
declara proveedor, versión, perfil y degradaciones, de modo que la ausencia de
Argos no se confunda con cobertura completa. Si no está disponible, Skevi
continúa con el colector mínimo y marca explícitamente la capacidad ausente; no
bloquea ni eleva cobertura por omisión.

El adaptador conserva el bundle nativo y sus fingerprints. La capa Skevi
referencia `claim_id` y `evidence_id`; no renombra relaciones, recalcula
cobertura ni convierte `mentions`, `tests`, `implements` o `configures` en
soporte. Fixtures compartidos deben demostrar que consumir y volver a emitir una
referencia no cambia el significado del contrato Argos.

Estado observado el 14 de agosto de 2026 en el commit remoto `b5734ac0`: Argos
es `0.2.0rc2`, publica schemas machine-first y una librería Python 3.12, pero no
tiene todavía CLI analítica estable ni MCP; ambos pertenecen a su Incremento 4.
Por ello la primera integración debe ser experimental, version-pinned y
opcional. Usa un perfil estático por defecto; ejecución dinámica o herramientas
del target requieren una capacidad L4/L5 independiente. No se instala desde
esta propuesta.

### 6.2 AN-KLA y Escrubery

AN-KLA queda reservado para continuidad y punteros entre sesiones; su memoria
es dato no confiable. Escrubery se evaluará después como proveedor de evidencia
sobre identidad, capacidades y vigencia de modelos y CLIs.

## 7. Secuencia propuesta

1. Corregir contradicciones documentales y fijar la matriz de autoridad.
2. Definir `inspect -> assess -> propose -> adopt -> verify` y sus schemas.
3. Fijar seguridad de descubrimiento, sensibilidad y política de bundles.
4. Validar `BASELINED` y el flujo read-only en dos proyectos existentes.
5. Definir adopción content-addressed, transaccional e idempotente.
6. Definir la interfaz de proveedor y un adaptador experimental de Argos.
7. Implementar gates semánticos F0 y F1 sólo para capacidades adoptadas.
8. Añadir recibos de evidencia y gate F3 ligado a Git.
9. Incorporar trazabilidad, perfiles de riesgo y reapertura selectiva.
10. Añadir lease de escritor y pruebas de orquestación.
11. Versionar la distribución y compilar contexto por tarea.
12. Ejecutar la suite comparativa con varios agentes.
13. Evaluar AN-KLA y Escrubery mediante decisiones separadas.

Cada paso es una tarea distinta. Un paso no concede permiso para ejecutar el
siguiente ni para instalar dependencias, hacer commit o publicar artefactos.

### 7.1 Decisión de la propuesta

PROP-001 no se acepta como paquete indivisible. La decisión registra por cada
iniciativa `accepted | rejected | deferred | needs-spike`, dependencias, evidencia
exigida y responsable del siguiente artefacto. Una iniciativa aceptada todavía
requiere ADR si cambia arquitectura o autoridad, más contrato de tarea antes de
implementarse. `needs-spike` autoriza sólo investigación read-only expresamente
acotada; no autoriza instalación ni prototipo persistente.

## 8. No objetivos

- No elegir un lenguaje, framework o proveedor para implementar el validador.
- No obligar a modificar un proyecto para poder analizarlo.
- No declarar incumplimiento de conformidad por una práctica no adoptada; los
  riesgos objetivos se reportan de todos modos y nunca se silencian.
- No reimplementar en Skevi el modelo epistémico que publica Argos.
- No reemplazar el juicio semántico del agente por reglas sintácticas.
- No instalar AN-KLA, Argos ni Escrubery desde este documento.
- No convertir propuestas en norma sin revisión, procedencia y razón.
- No obligar a una interfaz humana como mecanismo primario de operación.

## 9. Procedencia y razón

**Procedencia:** análisis solicitado por el humano el 14 de agosto de 2026;
contraste del estándar, guía F0-F3, orquestación, gate y pilotos históricos de
Skevi; inspección read-only mediante `gh` de README, contratos, manifiesto y
roadmap de Argos Epistemic en `b5734ac0`.

**Razón:** los pilotos demuestran que una política correcta en prosa no basta
para producir aplicación consistente entre agentes. La estructura propuesta
automatiza lo mecánico, conserva el juicio donde importa, aprovecha herramientas
especializadas y mantiene a Skevi agnóstico al lenguaje de programación.
