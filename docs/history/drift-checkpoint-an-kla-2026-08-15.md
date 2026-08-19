# Drift de checkpoint en AN-KLA — evidencia del método

> **Fecha:** 2026-08-15
> **Alcance:** incidente observado en el repositorio `an-kla-memory`, usado aquí
> como evidencia sobre el método de Skevi. No es normativo y no describe una
> regla nueva: registra un caso donde una regla ya escrita se cumplió al pie de
> la letra y aun así el resultado fue malo.
> **Relación:** confirma el tratamiento de memoria como dato no confiable de
> [`PROP-001`](../history/PROP-001-agent-native-model-improvements.md) §5.

## 1. Qué pasó

`an-kla-memory` mantiene una memoria local gobernada con checkpoints inmutables.
El 2026-08-13 se capturó el checkpoint de la revisión 29, que declaraba:

- `phase: beta13_published_gfresh_spike_next`;
- `origin/main = 27fa44f4c70540b8a5498e4e03e2cf17500ae300`;
- 13 issues abiertos;
- `next_step`: ejecutar el spike adversarial read-only de G-FRESH.

El 2026-08-15, el estado real del repositorio era `v0.1.0-beta.14` publicada,
`origin/main = 30e67606e9c0807aa8bf2080331cb0405bfb9241` y 12 issues abiertos. El
spike de G-FRESH nunca se ejecutó: el trabajo se desvió a beta.14.

Un agente que arrancara con `resume` habría recibido un mapa coherente,
verificable, firmado, íntegro — y equivocado en las cuatro afirmaciones.

## 2. Por qué el drift fue invisible

El trabajo de beta.14 se hizo desde un `git worktree`. Como `.an-kla/` es estado
local ignorado por Git, el worktree tenía su propio store: revisión 1, un solo
fact, otro `project_uuid`. Dos namespaces físicos, ningún vínculo declarado. El
checkpoint canónico no se actualizó porque nadie escribía en él.

El agravante es de schema. `working-state-v2` admite `source_state` únicamente
con `profile: none/v1` y `head`, `branch` y `dirty_digest` en `unavailable`. Por
diseño, **un checkpoint no puede ligarse al SHA que describe**. Nada permitía
detectar el desfase desde la propia memoria: no había contra qué comparar.

## 3. Qué confirma sobre el método

**La memoria envejece en silencio, y la integridad no es vigencia.** El
checkpoint era criptográficamente íntegro y epistémicamente falso. Las dos
propiedades son independientes, y la primera se confunde con la segunda porque es
la que se puede verificar barato.

**"La memoria es dato no confiable" no basta como regla si el dato no trae con
qué revalidarse.** La norma dice revalidar contra Git antes de actuar. El
checkpoint no incluía el SHA contra el cual revalidar, así que cumplir la regla
exigía trabajo de reconstrucción que es exactamente el que la memoria pretendía
ahorrar. Una regla que sólo se puede cumplir descartando el artefacto que regula
está mal planteada.

**El estado local ignorado por Git rompe la continuidad en cuanto hay más de un
checkout.** No es un fallo de implementación: es la consecuencia directa de
derivar la ubicación del store del `project_root`.

## 4. Correcciones aplicadas

En `an-kla-memory`, no en Skevi:

- checkpoint de reparación en la revisión 30, con el SHA, el tag y los conteos
  registrados en `evidence` — paliativo, porque `evidence` es texto libre que
  nadie valida;
- regla operativa en `AGENTS.md`: los worktrees no inicializan memoria propia y
  toda invocación usa `--project-root` del checkout canónico;
- issue [#76](https://github.com/kristhianmanue1/an-kla-memory/issues/76) acotado
  al diagnóstico read-only de arranque, dejando la reubicación de store y los
  hooks de host a sus propios issues;
- deuda registrada: un `source_state` con perfil `git/v1` y procedencia
  `tool_observed` convertiría el drift en detectable.

## 5. Qué significa para Skevi

El caso respalda la decisión de mantener toda memoria externa como integración
opcional y no autoritativa, y añade un matiz que el corpus todavía no dice: un
artefacto de continuidad debería **cargar consigo el ancla contra la cual se
revalida**. Sin ancla, "revalidar antes de actuar" es una instrucción que se
obedece o se ignora sin que nadie pueda notar la diferencia.

No se convierte en regla por este documento. Si se quiere normar, corresponde a
un ADR propio.
