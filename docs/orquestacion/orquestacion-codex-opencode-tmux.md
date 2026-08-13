# Orquestación de desarrollo con Codex CLI, OpenCode y tmux

**Estado:** guía técnica reutilizable  
**Ámbito:** proyectos de software locales en macOS o Linux  
**Modelo principal:** humano orquestador → Codex CLI controlador → OpenCode ejecutor  
**Modo directo validado:** humano → Codex Desktop controlador → OpenCode interactivo  
**Dependencias conceptuales:** ADRC, sesiones persistentes, revisión adversarial y evidencia ejecutable  
**Dependencias de runtime:** ninguna respecto de Escrubery o Epistates  
**Material operativo:** `orquestacion-codex-opencode-tmux-runbook.md` (recuperación, fallas comunes, prompts base, checklist de adopción)  
**Ronda adversarial de esta guía:** `../historia/orquestacion-codex-opencode-tmux-adversarial.md`  
**Última verificación:** 2026-08-12, contra `codex-cli 0.147.0`, `opencode 1.18.16`,
`tmux 3.6a`. Esta guía caduca cuando cambien flags o comportamiento de
cualquiera de las tres herramientas; si al usarla algo no coincide, es señal
de que necesita revalidarse, no de que el operador se equivocó.

## 1. Propósito

Esta guía define un método para delegar trabajo de desarrollo a agentes CLI sin
mantener al controlador consultando constantemente el progreso.

El objetivo es que:

- el humano conserve la dirección del proyecto y la autorización de release;
- Codex CLI actúe como controlador, planificador y auditor;
- OpenCode implemente y pruebe el trabajo dentro de un worktree;
- tmux mantenga vivas y visibles las sesiones;
- Codex quede realmente inactivo mientras OpenCode trabaja;
- OpenCode despierte a Codex mediante un mensaje al terminar;
- las ventanas de Codex y OpenCode permanezcan visibles para el orquestador;
- exista una ronda adversarial antes de considerar terminado un hito;
- el resultado se verifique con Git, pruebas y evidencia real.

Este mecanismo no convierte la salida de un agente en verdad ni autorización.
El reporte del ejecutor es una afirmación que el controlador debe contrastar.

La guía admite dos topologías que no deben mezclarse durante una misma tarea:

- **modo automático:** Codex CLI y OpenCode viven en sesiones tmux distintas;
  OpenCode despierta a Codex con `AGENT_DONE`;
- **modo directo:** Codex Desktop conserva el control y sólo OpenCode vive en
  tmux; el humano avisa a Codex Desktop cuando ve la marca final.

El modo automático sigue siendo el recomendado para trabajos largos sin
supervisión. El modo directo es una alternativa deliberada para pilotos,
depuración del protocolo y tareas en las que el humano observa la ventana.

## 2. Principio central

```text
sesión viva ≠ trabajo activo ≠ trabajo correcto ≠ verificación ≠ autorización
```

- tmux demuestra que una sesión puede persistir.
- una salida en terminal puede indicar progreso, pero no corrección.
- una suite verde aporta evidencia, pero no autoriza una publicación.
- una notificación sólo indica que llegó el momento de inspeccionar.
- el humano conserva las decisiones de alcance importante y release.

## 3. Roles

### 3.1 Orquestador humano

- define objetivo y prioridades;
- autoriza el inicio del ciclo;
- resuelve decisiones importantes o ampliaciones de alcance;
- puede observar las ventanas tmux cuando lo desee;
- conserva la autorización exclusiva para merge final, tag y release;
- puede pedir una auditoría externa adicional.

### 3.2 Codex CLI — controlador y auditor

- lee las instrucciones del repositorio;
- revisa issues, PRs, memoria y estado Git cuando corresponda;
- divide el trabajo y crea una tarjeta verificable;
- prepara rama, worktree y sesiones;
- lanza OpenCode con permisos suficientes;
- termina su turno y queda en el prompt, sin polling;
- al despertar, inspecciona el diff y ejecuta verificaciones independientes;
- envía correcciones concretas si encuentra fallas;
- puede ejecutar CI local, crear ramas, commits y push de ramas cuando esté
  autorizado por la tarea;
- se detiene antes de merge final, tag o publicación de release.

### 3.3 OpenCode — ejecutor

- trabaja sólo sobre el objetivo y worktree asignados;
- modifica código, documentación y tests dentro del alcance;
- ejecuta los checks del Definition of Done;
- realiza o coordina una ronda adversarial con contexto fresco;
- corrige los hallazgos aplicables;
- deja un reporte con comandos y resultados reales;
- notifica a Codex por tmux y termina.

### 3.4 Auditor externo opcional

Un segundo controlador, agente de escritorio o humano puede inspeccionar el
estado cuando el orquestador lo solicite. No debe hacer polling permanente ni
interferir con el ejecutor salvo orden explícita.

## 4. Topología de procesos

### Invariantes obligatorios del modo automático

1. Codex y OpenCode se ejecutan en **sesiones tmux distintas**.
2. Cada sesión se muestra en una ventana o pestaña de terminal visible para el
   orquestador humano durante toda la ejecución.
3. No basta con que la sesión exista en segundo plano: después de crearla se
   abre o adjunta una terminal visible.
4. OpenCode **debe despertar a Codex por tmux para entregar el trabajo**.
5. OpenCode no puede marcar la tarea como entregada ni terminar silenciosamente
   antes de enviar `AGENT_DONE` y la pulsación `Enter` a la sesión Codex.
6. Si OpenCode no puede terminar, envía `AGENT_BLOCKED` con una causa breve para
   despertar a Codex; no queda esperando permisos indefinidamente.

```text
Terminal visible
└── tmux: <proyecto>-codex-<tarea>
    └── Codex CLI interactivo
        ├── prepara y supervisa el ciclo
        └── queda inactivo en el prompt

Terminal o ventana visible
└── tmux: <proyecto>-opencode-<tarea>
    └── OpenCode ejecutor
        ├── implementa
        ├── prueba
        ├── ejecuta revisión adversarial fresca
        ├── corrige
        └── envía AGENT_DONE a la sesión Codex
```

Para una independencia adversarial mayor puede usarse una tercera sesión:

```text
tmux: <proyecto>-review-<tarea>
└── OpenCode nuevo, otro agente o preferiblemente otro modelo
```

### 4.1 Modo directo validado: Codex Desktop → OpenCode interactivo

En este modo no se crea una segunda instancia de Codex CLI. Codex Desktop es el
único controlador técnico y OpenCode se ejecuta interactivamente en tmux:

```text
Codex Desktop (controlador y auditor)
└── Terminal visible
    └── tmux: <proyecto>-opencode-<tarea>
        └── opencode interactivo
```

Reglas específicas:

1. no existe una sesión tmux receptora de Codex y por tanto OpenCode no puede
   usar `AGENT_DONE` para despertar esta conversación Desktop;
2. el humano observa la marca final y avisa a Codex Desktop;
3. Codex Desktop inspecciona Git y ejecuta los gates igual que en el modo
   automático;
4. la sesión interactiva permanece abierta para correcciones conversacionales;
5. no se lanza otro controlador que pueda editar simultáneamente el worktree.

El arranque de este modo fue validado al iniciar H4 Slice3 de Epistates.
Conserva visibilidad y persistencia, pero no ofrece wake-up automático ni pausa
totalmente autónoma.

## 5. Máquina de estados operativa

```text
PREPARED
  → EXECUTOR_RUNNING
  → WAITING_EXTERNAL
  → EXECUTOR_DONE
  → AUDITING
  → CORRECTION_SENT → WAITING_EXTERNAL
  → ADVERSARIAL_REVIEW
  → CI_LOCAL
  → READY_FOR_HUMAN
  → RELEASED | BLOCKED
```

Reglas:

1. `WAITING_EXTERNAL` significa que Codex terminó su turno y está en el prompt.
2. No se implementa espera mediante `sleep`, bucles o capturas repetidas.
3. `AGENT_DONE` sólo habilita auditoría; no significa aceptación automática.
4. Una corrección conserva la misma tarea y aumenta el número de intento.
5. `READY_FOR_HUMAN` es el límite de autonomía para publicación.

## 6. Preparación del repositorio

Antes de lanzar agentes:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git worktree list
tmux list-sessions
```

Si un nombre de sesión ya existe, inspecciónalo y decide si corresponde al mismo
`run_id`; adjunta esa sesión o usa un nombre nuevo. No la reemplaces ni la mates
automáticamente, porque podría contener trabajo vigente.

El controlador debe identificar:

- repositorio y raíz esperados;
- SHA base;
- rama de trabajo;
- ruta absoluta del worktree;
- instrucciones `AGENTS.md` aplicables;
- issues y PRs abiertos cuando el repositorio use GitHub como backlog;
- pruebas base obligatorias;
- archivos autorizados y prohibidos;
- operaciones Git autorizadas;
- operación que requiere autorización humana final.

Ejemplo de nombres:

```text
task_id: issue-60-g-view
run_id: issue-60-g-view-20260812-01
attempt_id: 1
controller_session: an-kla-codex-issue60
controller_pane: %<pane-id>
executor_session: an-kla-opencode-issue60
executor_pane: %<pane-id>
worktree: /ruta/absoluta/proyecto-wt-issue60
branch: codex/issue-60
```

## 7. Tarjeta de trabajo

La tarjeta es el contrato operativo entre Codex y OpenCode. Debe vivir en un
archivo `.md` pequeño, legible y verificable.

### 7.1 Campos mínimos

```markdown
# Tarea: <task_id>

## Identidad
- Repositorio: <owner/repo>
- Worktree: <ruta absoluta>
- Rama: <rama>
- SHA base: <sha completo>
- Run: <run_id>
- Intento: <attempt_id>
- Sesión Codex: <controller_session>
- Pane Codex: <controller_pane>
- Sesión OpenCode: <executor_session>
- Pane OpenCode: <executor_pane>

## Objetivo
<un solo resultado concreto>

## Entradas obligatorias
- AGENTS.md
- documentación o ADR aplicable
- issue o especificación

## Alcance permitido
- <rutas y tipos de cambio>
- ejecutar tests, lint y gates
- corregir fallas dentro del alcance

## Fuera de alcance
- cambios no relacionados
- borrados destructivos
- reescritura de historia Git
- merge, tag o release

## Definition of Done
- [ ] <comando> → <resultado esperado>
- [ ] <test focal>
- [ ] suite completa
- [ ] git diff --check
- [ ] reporte final con evidencia
- [ ] ronda adversarial con decisión proceed

## Ronda adversarial
Usar un contexto fresco. Buscar BLOCKER/HIGH/MED/LOW, corregir los hallazgos
aplicables y repetir los checks. No limitarse a estilo.

## Cierre
Guardar el reporte en <ruta>. Después enviar a Codex:
AGENT_DONE task=<task_id> run=<run_id> attempt=<attempt_id> report=<ruta>
```

### 7.2 Regla de tamaño

Una tarea debe caber holgadamente en una sesión. Si mezcla múltiples contratos,
formatos o subsistemas críticos, se divide en fases. Cada fase deja un diff
pequeño y revisable.

## 8. Lanzamiento de Codex CLI en tmux

Codex debe ejecutarse en modo interactivo, no como proceso `exec` que termina al
final de una respuesta.

Antes de crear sesiones, confirma una vez que las opciones usadas existen:

```bash
codex --version
codex --help
opencode --version
opencode run --help
tmux -V
```

Si una versión no expone `--approve-for-me`, `--auto`, `--model` o `--continue`,
adapta el comando antes de lanzar; no entres a `WAITING_EXTERNAL` con un CLI que
terminó inmediatamente por una opción inválida.

Ejemplo conceptual:

```bash
tmux new-session -d -s an-kla-codex-issue60 \
  -c /ruta/absoluta/al/worktree

tmux display-message -p -t an-kla-codex-issue60:0.0 '#{pane_id}'

tmux send-keys -t %<controller-pane-id> \
  "codex -C /ruta/absoluta/al/worktree --sandbox workspace-write --approve-for-me --no-alt-screen" Enter
```

Registra el `%pane-id` devuelto en la tarjeta. Es el destino estable para los
mensajes de OpenCode aunque el humano cree otras ventanas o cambie el pane
activo de la sesión.

La sesión se muestra inmediatamente al orquestador. En macOS con Terminal:

```bash
osascript -e 'tell application "Terminal" to do script "tmux attach-session -t an-kla-codex-issue60"'
```

En Linux, el equivalente depende del emulador disponible; por ejemplo:

```bash
gnome-terminal -- tmux attach-session -t an-kla-codex-issue60
```

La ventana visible es parte del contrato operativo: no se considera lanzado el
controlador hasta que el orquestador pueda observarla.

Después se entrega a Codex una tarjeta de controlador. El texto debe indicarle:

- que puede trabajar con autonomía dentro del worktree;
- que puede lanzar OpenCode y administrar tmux;
- que puede ejecutar CI local, crear commits y gestionar la rama autorizada;
- que debe auditar independientemente los reportes;
- que debe finalizar cada turno y quedar en el prompt;
- que no debe hacer polling;
- que debe detenerse antes de merge/tag/release.

`--approve-for-me` permite que Codex resuelva de forma automática las
aprobaciones compatibles con `workspace-write`. No debe usarse bypass total de
sandbox salvo que exista un sandbox externo real y el humano lo haya decidido.

## 9. Lanzamiento de OpenCode

Codex crea una segunda sesión visible:

```bash
tmux new-session -d -s an-kla-opencode-issue60 \
  -c /ruta/absoluta/al/worktree

tmux display-message -p -t an-kla-opencode-issue60:0.0 '#{pane_id}'
```

Puede iniciar OpenCode con el modelo definido para el proyecto:

```bash
tmux send-keys -t %<executor-pane-id> \
  "opencode run --auto --model <proveedor/modelo> 'Lee completamente <tarjeta.md> y ejecútala'" Enter
```

Registra también este `%pane-id`. Tras el arranque realiza **una sola**
inspección acotada:

```bash
tmux list-panes -t an-kla-opencode-issue60 \
  -F '#{pane_id}|#{pane_dead}|#{pane_current_command}|#{pane_current_path}'
```

Entra a `WAITING_EXTERNAL` únicamente si el pane está vivo, su ruta corresponde
al worktree y el comando observado es OpenCode. Esto es un preflight único, no
polling.

Codex debe abrir también esta sesión en otra ventana o pestaña visible. En
macOS con Terminal:

```bash
osascript -e 'tell application "Terminal" to do script "tmux attach-session -t an-kla-opencode-issue60"'
```

El orquestador debe poder ver simultáneamente o alternar directamente entre:

- ventana Codex: planificación, espera, auditoría y correcciones;
- ventana OpenCode: implementación, pruebas y ronda adversarial.

Que OpenCode sea lanzado por Codex no autoriza dejar su sesión oculta.

Para evitar problemas de quoting en tareas grandes, la instrucción enviada al
CLI debe ser breve y apuntar al archivo de tarjeta; el contenido completo no se
incrusta en el comando.

### 9.1 Dos formas de iniciar OpenCode

#### One-shot con entrega automática

`opencode run` recibe la instrucción en el propio comando, por lo que no existe
una carrera entre el arranque de la TUI y la inyección del primer prompt. Es la
forma recomendada para el modo automático:

```bash
tmux new-session -d -s <executor-session> -c <worktree>
tmux send-keys -l -t %<executor-pane-id> -- \
  "opencode run --auto 'Lee completamente <tarjeta.md> y ejecútala'"
tmux send-keys -t %<executor-pane-id> Enter
```

Al terminar vuelve normalmente al shell; las correcciones requieren otro
`opencode run --continue` o una ejecución nueva.

#### Interactivo persistente para el modo directo

Para mantener conversación y contexto visibles dentro del mismo OpenCode:

```bash
tmux new-session -d -s <executor-session> -c <worktree> opencode
```

Hay una carrera de arranque real: `pane_current_command=opencode` no demuestra
que la TUI ya acepte entrada. Si se envía el prompt inmediatamente, éste puede
perderse. El orden validado es:

1. crear la sesión;
2. abrir la ventana visible;
3. hacer una inspección única y confirmar que aparece el prompt `Ask anything`;
4. sólo entonces enviar el texto literal y `Enter` en llamadas separadas;
5. confirmar una vez que la tarea aparece en la TUI o que OpenCode comenzó a
   pensar/leer la tarjeta.

```bash
tmux capture-pane -p -t <executor-session>:0 -S -40

tmux send-keys -l -t <executor-session>:0 -- \
  'Lee completamente <tarjeta.md> y ejecuta la tarea. No hagas commit.'
tmux send-keys -t <executor-session>:0 Enter
```

Si la inspección muestra que la TUI terminó de iniciar pero la tarea no aparece,
se permite reenviar **una vez** la misma instrucción exacta. Esto es recuperación
del lanzamiento, no polling ni un nuevo intento contractual.

### 9.2 Permisos prácticos de OpenCode

En desarrollo normal se recomienda autonomía amplia:

- lectura, búsqueda, edición y patches: permitidos;
- bash necesario para tests, linters y herramientas del proyecto: permitido;
- subagentes o tareas de revisión: permitidos;
- escritura dentro del worktree: permitida;
- acceso a dependencias o red: permitido cuando la tarea lo requiera;
- commit: puede reservarse a Codex para mantener separación de responsabilidades;
- push, merge, tag y release: reservados al controlador/humano.

El objetivo no es pedir aprobación por cada comando, sino impedir únicamente
acciones claramente fuera del ciclo de desarrollo.

## 10. Pausa real de Codex

Después de confirmar que OpenCode arrancó, Codex debe responder con un estado
breve y terminar su turno. Ejemplo:

```text
OpenCode ejecutándose en an-kla-opencode-issue60.
Estado: WAITING_EXTERNAL.
```

En ese momento:

- Codex permanece abierto dentro de tmux;
- el cursor queda en el prompt de entrada;
- no hay generación de tokens;
- no se ejecutan `sleep`, polling ni `capture-pane` repetidos;
- el humano puede observar ambas ventanas.

Un proceso vivo consume recursos locales mínimos, pero no inferencia mientras
no reciba un nuevo mensaje.

En el modo directo, Codex Desktop no tiene un pane que OpenCode pueda despertar.
El controlador termina su turno y el humano lo reactiva al observar la marca
final. No debe simularse el wake-up mediante polling desde Desktop.

## 11. Ronda adversarial

La revisión adversarial debe usar contexto fresco. Hay dos modalidades.

### Modalidad A — coordinada por OpenCode

El ejecutor termina la implementación y lanza un subagente o sesión de revisión
nueva. El revisor inspecciona el diff, los requisitos y las pruebas. El ejecutor
corrige hallazgos y repite hasta obtener `proceed` o `escalate`.

Es la modalidad más rápida y suficiente para trabajo cotidiano.

### Modalidad B — coordinada por Codex

OpenCode completa su ciclo normal y notifica `AGENT_DONE`. Codex audita la
entrega y luego lanza una sesión de revisión nueva, preferiblemente con otro
modelo. Si el reviewer es externo, Codex puede volver a `WAITING_EXTERNAL`
hasta recibir su propio `AGENT_DONE`. Es más adecuada para cambios críticos o
releases y no introduce un segundo protocolo de notificación.

### Formato del reporte adversarial

```markdown
## Hallazgos
- [BLOCKER] problema — evidencia — corrección requerida
- [HIGH] problema — evidencia — corrección requerida
- [MED] problema — evidencia — corrección sugerida
- [LOW] problema — evidencia — seguimiento opcional

## Verificaciones
- comando → resultado real

## Decisión
proceed | fix-and-retry | escalate
```

No se considera adversarial una revisión que sólo elogia el cambio o señala
estilo. Debe atacar invariantes, compatibilidad, errores silenciosos, casos edge
y correspondencia exacta con el contrato.

## 12. Notificación OpenCode → Codex

Al terminar el trabajo y escribir todos los archivos, OpenCode **obligatoriamente
despierta a Codex** enviando una línea breve a su sesión tmux. Este envío es el
mecanismo de entrega entre agentes, no un paso opcional.

Ejemplo:

```text
AGENT_DONE task=issue-60-g-view run=issue-60-g-view-20260812-01 attempt=1 report=docs/planning/issue-60-report.md
```

La entrega se realiza en dos llamadas:

```bash
tmux send-keys -l -t %<controller-pane-id> -- \
  'AGENT_DONE task=issue-60-g-view run=issue-60-g-view-20260812-01 attempt=1 report=docs/planning/issue-60-report.md'

tmux send-keys -t %<controller-pane-id> Enter
```

La primera llamada escribe texto literal. La segunda pulsa Enter. Separarlas
evita que el mensaje se quede visible sin ejecutarse o que tmux interprete parte
del texto como nombres de teclas.

El mensaje despierta a Codex, pero no sustituye el reporte ni las pruebas.

OpenCode sólo puede considerar entregada la tarea después de que ambas llamadas
`send-keys` hayan finalizado. El texto sin `Enter` no despierta a Codex.

Si existe un bloqueo que impide completar el trabajo:

```text
AGENT_BLOCKED task=issue-60-g-view run=issue-60-g-view-20260812-01 attempt=1 reason=permission-required
```

Se entrega con el mismo patrón literal + `Enter`. Codex despierta, inspecciona
el estado y decide si puede resolverlo o si debe informarlo al humano.

## 13. Auditoría de Codex al despertar

Codex no debe aceptar el mensaje como prueba de corrección. Debe inspeccionar:

```bash
git status --short
git diff --stat
git diff --check
git diff
```

Después ejecuta:

1. tests focales de los archivos cambiados;
2. suite completa exigida por `AGENTS.md`;
3. linters, type checks y gates de tamaño;
4. CI local equivalente al remoto cuando exista;
5. verificación de schemas, documentación y versión si aplica;
6. revisión de secretos y cambios accidentales;
7. correspondencia entre DoD, diff y reporte adversarial.

El resultado debe clasificarse:

- `OK`: contrato completo y evidencia suficiente;
- `PARCIAL`: trabajo útil, pero falta un gate no bloqueante o una operación
  externa;
- `BLOQ`: baseline rota, hallazgo crítico o decisión humana necesaria.

## 14. Correcciones y nuevos intentos

Si Codex encuentra fallas:

1. formula una instrucción pequeña y concreta;
2. incrementa `attempt_id`;
3. crea una tarjeta inmutable para el nuevo intento con el mensaje de cierre
   exacto (`run`, `attempt` y `report`);
4. relanza OpenCode desde el shell de su pane usando `opencode run --continue`
   o, si no hay sesión reanudable, abre una ejecución nueva que lea la tarjeta
   original y la tarjeta de corrección;
5. confirma una sola vez que OpenCode arrancó;
6. termina su turno y vuelve a `WAITING_EXTERNAL`.

Ejemplo:

```markdown
# Corrección — issue-60-g-view — intento 2

- Tarjeta original: </ruta/tarjeta-intento-1.md>
- Run: issue-60-g-view-20260812-01
- Intento: 2
- Hallazgo: el cursor no está ligado al SHA de revisión.
- Corrección: añadir el binding y un test de cursor cruzado; repetir los gates.
- No ampliar el scope.
- Reporte: docs/planning/issue-60-report-attempt-2.md
- Cierre exacto: AGENT_DONE task=issue-60-g-view run=issue-60-g-view-20260812-01 attempt=2 report=docs/planning/issue-60-report-attempt-2.md
```

`opencode run` es one-shot: después de `AGENT_DONE` normalmente termina y deja
el shell en el pane. Por eso **no** se envía texto `CORRECTION ...` directamente
al pane; el shell intentaría ejecutarlo como comando. Se inicia otro
`opencode run`, con `--continue` cuando esté disponible. Para una auditoría
independiente se utiliza contexto fresco, no `--continue`.

Ejemplo de relanzamiento desde el pane de OpenCode:

```bash
tmux send-keys -l -t %<executor-pane-id> -- \
  "opencode run --continue --auto --model <proveedor/modelo> 'Lee completamente /ruta/correccion-intento-2.md y ejecútala'"

tmux send-keys -t %<executor-pane-id> Enter
```

La tarjeta del intento 2 contiene la entrega exacta `AGENT_DONE ... attempt=2`;
no depende de que el modelo recuerde sustituir el número anterior.

## 15. Git y CI

Una configuración práctica de autonomía es:

| Operación | OpenCode | Codex | Humano |
|---|---:|---:|---:|
| editar worktree | sí | sí | sí |
| tests/lint/CI local | sí | sí | sí |
| crear rama/worktree | no habitual | sí | sí |
| commit | opcional | sí | sí |
| push de rama | no habitual | sí | sí |
| abrir/actualizar PR | no | según autorización | sí |
| merge a main | no | no por defecto | sí |
| tag/release | no | prepara evidencia | autoriza/ejecuta |

Antes de commit:

```bash
git diff --check
git status --short
<tests focales>
<suite completa>
<CI local>
```

El commit debe ser pequeño, convencional y corresponder a una sola fase. El
release nunca se deduce de una suite verde: se presenta al humano con SHA,
gates, limitaciones y reporte adversarial.

## 16. Niveles recomendados de rigor

### Trabajo cotidiano

- OpenCode con autonomía amplia;
- adversarial coordinado por OpenCode;
- Codex audita diff y tests;
- commit y push de rama permitidos;
- humano interviene al final.

Cuando el humano desea observación continua y correcciones conversacionales,
puede usarse el modo directo con OpenCode interactivo y marca final visible.

### Cambio crítico

- worktree dedicado;
- fases pequeñas;
- adversarial en sesión y modelo frescos;
- CI local completa;
- Codex revisa cada invariante con evidencia;
- humano autoriza integración y release.

### Release

- SHA exacto;
- árbol limpio;
- suite completa y paquete instalable;
- ronda adversarial `proceed`;
- limitaciones externas declaradas;
- autorización humana explícita antes de tag/publicación.

## 17. Material operativo complementario

La recuperación de sesiones, las fallas comunes con su diagnóstico, los prompts
base para controlador y ejecutor, y el checklist de adopción viven en
`orquestacion-codex-opencode-tmux-runbook.md`. Se separaron porque se consultan
durante la operación, no al leer el protocolo, y porque ningún archivo de este
estándar debe superar 800 líneas.

## 18. Regla final

La autonomía debe ser amplia dentro de la tarea y estrecha fuera de ella.

No se busca interrumpir al desarrollador con aprobaciones rutinarias. Se busca
que los agentes puedan producir software de forma continua, verificable y
visible, mientras el humano conserva las decisiones que cambian el alcance o
publican resultados al exterior.
