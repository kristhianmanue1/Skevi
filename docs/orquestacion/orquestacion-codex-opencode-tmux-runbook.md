# Runbook operativo — Codex/OpenCode/tmux

**Tipo:** material de consulta con el teclado en la mano.
**Protocolo asociado:** `orquestacion-codex-opencode-tmux.md`, que define roles,
topologías, máquina de estados, tarjeta de trabajo y reglas de autoridad.
**Cuándo se usa este archivo:** al adoptar el método en un proyecto nuevo, al
lanzar una sesión y cuando algo se rompe durante la ejecución.

Este archivo no contiene reglas nuevas: es la parte copiable y consultable del
protocolo, separada para que ninguno de los dos exceda el límite de tamaño y
ambos puedan leerse completos de una vez.

## 1. Recuperación de sesiones

### Codex sigue vivo

```bash
tmux attach-session -t <controller_session>
```

### OpenCode sigue vivo

```bash
tmux attach-session -t <executor_session>
```

### Codex terminó inesperadamente

Abrir una sesión nueva en el mismo worktree y reanudar la sesión persistida:

```bash
codex resume --last -C <worktree>
```

Cuando haya varias sesiones, registrar el ID exacto de Codex en el reporte del
controlador y reanudar por ID en lugar de `--last`.

### OpenCode terminó sin notificar

El humano puede avisar a Codex o escribir manualmente `AGENT_DONE`. Codex debe
auditar el worktree de la misma forma; la ausencia de notificación no invalida
automáticamente los cambios.

En modo directo esto no es una anomalía: la notificación humana es el mecanismo
de entrega esperado. La tarjeta usa una marca final inequívoca como
`FIN <TASK>-IMPLEMENTATION` y ordena conservar la sesión conversacional.

## 2. Fallas comunes

### El mensaje aparece en Codex pero no se procesa

Causa: se envió texto literal sin una segunda llamada `Enter`.

Solución: enviar `tmux send-keys -t <sesión> Enter` por separado.

### La ventana parece congelada

Posibles causas:

- el agente espera un permiso;
- está ejecutando una prueba larga;
- el proceso terminó y quedó un shell;
- el mensaje se envió al nombre de sesión equivocado;
- Codex todavía estaba generando y la entrada quedó en cola.

Inspeccionar una sola vez:

```bash
tmux list-panes -t <sesión> -F '#{pane_dead}|#{pane_current_command}|#{pane_current_path}'
tmux capture-pane -t <sesión> -p -S -80
```

Después decidir; no convertir esta inspección en polling continuo.

### OpenCode pide permisos repetidamente

Configurar permisos amplios para lectura, edición, bash y subagentes dentro del
worktree, o usar `--auto` con las prohibiciones importantes ya definidas.

### El agente modificó archivos fuera del alcance

Codex separa cambios relacionados de cambios accidentales. No borra trabajo a
ciegas; informa el conflicto o pide al ejecutor que lo corrija.

### El primer prompt nunca apareció en OpenCode

Causa: se inició `opencode` interactivamente y se enviaron teclas antes de que
la TUI estuviera lista.

Solución: comprobar una sola vez que el prompt visible ya existe, enviar texto
literal y `Enter` por separado y confirmar una vez que la instrucción aparece.
No usar un `sleep` fijo como prueba de readiness: la latencia de inicio varía.

### La suite pasa, pero el requerimiento no está completo

Los tests son una dimensión. Codex también compara el diff contra cada criterio
del DoD y revisa compatibilidad, documentación y comportamiento observable.

## 3. Prompt base para Codex controlador

```text
Eres el controlador técnico de esta tarea. Lee AGENTS.md y la tarjeta completa.
Tienes autonomía para administrar el worktree y la rama, lanzar OpenCode en una
sesión tmux visible, ejecutar CI local, corregir problemas menores y crear
commits/push de la rama si la tarjeta lo permite.

OpenCode será el ejecutor. Dale una tarea verificable, permite que implemente,
pruebe y realice una ronda adversarial en contexto fresco. Después de lanzarlo,
termina tu turno y queda en WAITING_EXTERNAL: no hagas polling ni sleep.

OpenCode te despertará enviando AGENT_DONE a esta sesión tmux. Al recibirlo,
audita críticamente Git, diff, tests, gates y reporte adversarial. Si hay fallas,
envía una corrección pequeña y vuelve a esperar. Si todo está correcto, prepara
el commit y la evidencia final. No hagas merge, tag ni release sin autorización
actual del orquestador humano.
```

## 4. Prompt base para OpenCode ejecutor

```text
Lee completamente la tarjeta indicada y las instrucciones del repositorio.
Implementa el alcance con autonomía dentro del worktree. Ejecuta los checks del
DoD y corrige sus fallas.

Antes de terminar, realiza una ronda adversarial con contexto fresco enfocada en
corrección, requisitos, compatibilidad y casos edge. Corrige BLOCKER/HIGH y los
MED aplicables, repite las verificaciones y deja un reporte con evidencia real.

Cuando todos los archivos estén escritos y los comandos hayan terminado, envía
exactamente el mensaje AGENT_DONE indicado en la tarjeta a la sesión tmux de
Codex usando send-keys literal y Enter en llamadas separadas. Después termina.
No hagas merge, tag ni release.
```

## 5. Checklist de adopción en otro proyecto

- [ ] existe `AGENTS.md` o instrucciones equivalentes;
- [ ] se conoce el comando de tests y CI local;
- [ ] el repositorio está limpio o la suciedad existente está inventariada;
- [ ] la tarea tiene objetivo único y DoD ejecutable;
- [ ] existe worktree y rama aislados;
- [ ] los nombres tmux son únicos y conocidos por ambos agentes;
- [ ] Codex está en modo interactivo y visible;
- [ ] OpenCode está en otra ventana o pestaña visible;
- [ ] OpenCode tiene permisos suficientes dentro del worktree;
- [ ] la tarjeta declara quién puede hacer commit/push;
- [ ] el mensaje `AGENT_DONE` está definido;
- [ ] OpenCode tiene orden explícita de despertar a Codex por tmux antes de salir;
- [ ] existe ronda adversarial fresca;
- [ ] Codex audita independientemente;
- [ ] release permanece bajo autorización humana.

Para modo directo, sustituir los checks específicos de Codex/OpenCode visibles
y de `AGENT_DONE` por:

- [ ] Codex Desktop es el único controlador y no existe otro controlador
  editando el worktree;
- [ ] OpenCode interactivo está listo antes de enviar el primer prompt;
- [ ] la tarjeta define una marca `FIN ...` y el humano notificará su aparición.

