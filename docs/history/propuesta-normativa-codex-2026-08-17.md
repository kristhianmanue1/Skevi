# Propuesta normativa de un proveedor independiente — Codex

**Fecha:** 2026-08-17
**Encargo:** redactar el texto concreto que aplica ADR-004 y ADR-005 al
estándar y a la guía.
**Proponente:** `codex exec` con `codex-cli 0.147.0`, sesión y proveedor
distintos del autor del corpus.
**Modo:** `--sandbox read-only` sobre un clon desechable.
**Resultado:** diez cambios propuestos con texto literal, ubicación exacta,
conteo de líneas y una sección propia de riesgos.

## Por qué se pidió a otro proveedor

Hasta ahora la decorrelación de este repositorio cubría sólo la crítica: un
revisor adversarial de otro proveedor atacaba lo que el autor escribía. La
generación seguía siendo de una sola fuente.

Aquí se separan los tres papeles: **autor** (Opus), **proponente
independiente** (Codex) y **revisor adversarial** (Gemini). Ningún proveedor
propone y juzga el mismo artefacto.

## Lo que la propuesta encontró y el autor no

**El principio fail-closed estaba escrito de cinco maneras distintas**, en un
corpus cuyo README declara que los principios *"no se resumen ni se parafrasean:
una paráfrasis es una segunda copia con otras palabras, y envejece igual de mal
que una copia literal"*:

| Ubicación | Formulación |
|---|---|
| estándar §1.5 | "ante la incertidumbre… nunca asume permiso ni éxito por defecto" |
| estándar §6.7 | "evidencia inconsistente, alcance excedido o permiso ausente: detener y escalar" |
| guía `00-INDICE` regla 6 | "permiso ausente, requisito ambiguo o estado inconsistente: detente, reporta y pregunta" |
| `AGENTS.md` | copia literal de la anterior |
| guía `02` §2 | "(fail-closed: estado seguro, nunca éxito inferido)" |

El autor pensaba modificar una. La propuesta las convierte en **referencias al
hogar canónico** en lugar de actualizar cada copia, que es lo que el propio
corpus exige y no se estaba cumpliendo.

También localizó dos sitios donde la marca de ADR-005 aplica y el autor no había
considerado: el registro `EV-*` de F0 y el bloque de verificaciones de la ronda
adversarial en F3.

## Lo que se aplicó con distinta forma

**La derivación del estado de fase.** Codex propuso que `fail` o `inconclusive`
produzcan `PARCIAL` *"mientras el criterio pueda corregirse u obtenerse dentro
del alcance"*, y `BLOQ` cuando no. Se descartó esa formulación: introduce un
juicio —"dentro del alcance"— que es exactamente la clase de calificador
subjetivo que ADR-004 y el piloto Skopos demostraron que un ejecutor resuelve a
su favor. Se conserva la derivación mínima: `OK` exige que las líneas que
cierran el gate sean `pass`, e `inconclusive` nunca cierra un gate.

**La densidad del principio 5.** La propuesta lo reconoce como riesgo propio: la
lista de clases protegidas lo deja más denso que los otros seis. Se aceptó igual
—partirlo crearía un segundo hogar normativo— y se acortó la redacción.

## Riesgos que la propuesta declaró de sí misma

- Dos sintaxis válidas conviven durante la transición.
- Los tokens `pass`, `fail` e `inconclusive` rompen el registro en español; se
  conservan porque traducirlos crearía incompatibilidad con validadores
  externos y con el vocabulario de `praxis/project-governance`.
- Las fronteras de "datos de terceros", "políticas" y "recursos compartidos"
  pueden generar dudas de clasificación, y la regla de duda-como-protegida
  aumentará los bloqueos.
- Un validador podría interpretar los corchetes de la plantilla como literales.

## Nota de método

Un proponente independiente encontró en una pasada una incoherencia de cinco
copias que llevaba en el corpus desde su origen y que ni el autor ni cuatro
rondas adversariales previas habían visto. La crítica independiente detecta lo
que está mal en lo escrito; la **propuesta** independiente detecta lo que nadie
escribió.
