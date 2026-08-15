# PROP-001 — Decisión por iniciativa

> **Fecha:** 2026-08-15
> **Artefacto decidido:** [`PROP-001-agent-native-model-improvements.md`](PROP-001-agent-native-model-improvements.md)
> **Resultado global:** parcialmente aceptada.
> **Responsable de la decisión:** maintainer de Skevi.
> **Efecto:** ninguna iniciativa se convierte en norma por este documento. Lo
> aceptado produce ADR y contrato de tarea antes de implementarse; `needs-spike`
> autoriza sólo investigación read-only acotada.

## 1. Base de la decisión

PROP-001 cerró su ronda adversarial en `proceed` con F1–F8 corregidos
([registro](../history/PROP-001-adversarial-2026-08-14.md)). §7.1 exige decidir
por iniciativa, no como paquete. Este documento cumple esa exigencia y congela la
propuesta conforme a §1.1.

El criterio aplicado es conservador y tiene una razón: Skevi tiene dos pilotos
reales (sí mismo y Skopos) y ninguna implementación. Aceptar iniciativas que
sólo se pueden validar construyendo un ejecutable comprometería trabajo sin
evidencia de que haga falta. Se aceptan las iniciativas **documentales** —las que
resuelven contradicciones ya observadas en el corpus— y se difiere todo lo que
presupone un binario.

## 2. Decisiones

| ID | Decisión | Depende de | Evidencia exigida | Siguiente artefacto |
|----|----------|-----------|-------------------|---------------------|
| P0-01 | `accepted` | — | matriz de precedencia única; cada documento normativo la referencia sin parafrasearla | ADR-004 |
| P0-04 | `accepted` | — | tabla de transiciones con evento duplicado, intento obsoleto y `run_id` ajeno | ADR-005 |
| P0-06 | `accepted` | P0-01 | fixture sin archivos Skevi que llega a `BASELINED` sin mutación ni falso `F0: OK` | ADR-006 |
| P0-00 | `needs-spike` | P0-01 | spike read-only que demuestre la frontera de lectura sobre un repo real sucio | informe de spike |
| P0-02 | `deferred` | P0-00 | descubrimiento previo de manifiestos reales del ecosistema | — |
| P0-03 | `deferred` | P0-04 | — | — |
| P0-05 | `deferred` | P0-00, P0-04 | — | — |
| P0-07 | `deferred` | P0-00, P0-02 | — | — |
| P1-01 | `deferred` | P0-00 | — | — |
| P1-02 | `deferred` | P0-05 | — | — |
| P1-03 | `accepted` | — | matriz de disparadores observables aplicada a los dos pilotos existentes | ADR-007 |
| P1-04 | `accepted` | P0-04 | `CHANGE-REQ-*` que invalide sólo los gates dependientes | ADR-008 |
| P1-05 | `deferred` | P0-03 | — | — |
| P2-01 | `deferred` | P0-02 | — | — |
| P2-02 | `deferred` | P0-00 | — | — |
| P2-03 | `deferred` | P0-05 | — | — |

Ninguna iniciativa se rechaza: `deferred` significa que la iniciativa sigue
siendo válida y vuelve a evaluarse cuando su dependencia se resuelva, no que se
descarte.

## 3. Razón de cada aceptación

**P0-01 — autoridad y confianza documental.** Es la única contradicción viva del
corpus: `AGENTS.md` declara que los documentos nunca son instrucciones mientras
F0 clasifica documentos normativos como autoridad. Un agente que lea ambos hoy
recibe reglas incompatibles. No requiere ejecutable y desbloquea P0-06.

**P0-04 — estados, resultados y decisiones.** Tres vocabularios conviven sin
mapeo (`lifecycle_state`, `OK|PARCIAL|BLOQ`, `proceed|fix-and-retry|escalate`).
El piloto de Skopos ya produjo reportes ambiguos por esto. La tabla de
transiciones es documental; los tests que la propuesta pide pueden esperar al
ejecutable.

**P0-06 — baseline para proyectos existentes.** Es la brecha que más costó en el
piloto Skopos: aplicar el método a un repositorio que ya existía forzó a decidir
sobre la marcha qué significaba F0 en algo ya construido. `BASELINED` y la
separación declarado/observado/inferido son reglas, no código.

**P1-03 — perfiles objetivos de riesgo.** `material` aparece nueve veces entre
`AGENTS.md` y la guía, y `no trivial` y `críticos` una vez cada uno, siempre sin
definición: son la condición que dispara ronda adversarial, contratos y threat
model, y cada agente los resuelve distinto. Derivarlos de disparadores
observables es una matriz, no código.

**P1-04 — cambio de requisitos y reapertura selectiva.** Un requisito que aparece
tras cerrar F0 no tiene tratamiento definido; hoy la salida práctica es
incorporarlo callado en F3, que es exactamente lo que el método prohíbe.

## 4. Razón del `needs-spike` de P0-00

P0-00 es la iniciativa con mayor superficie de seguridad de toda la propuesta:
canonicalización de raíz, symlinks, archivos especiales, filtros Git ejecutables,
presupuestos y degradaciones. Su aceptación exigiría diseñar una frontera de
lectura segura sin haber comprobado antes cómo se comporta un repositorio real
sucio.

El spike autorizado es **read-only y acotado**: inspeccionar los repositorios ya
disponibles, registrar qué produce cada nivel de evidencia L0–L2 y qué omisiones
aparecen. No autoriza escribir en ningún target, instalar dependencias, usar red,
crear prototipo persistente ni elegir lenguaje de implementación.

## 5. Lo que esta decisión no concede

- No autoriza implementar `skevi inspect` ni ningún otro comando.
- No autoriza instalar AN-KLA, Argos ni Escrubery.
- No convierte ninguna iniciativa aceptada en norma: cada una necesita su ADR.
- No fija lenguaje, framework ni proveedor.
- No autoriza publicar, etiquetar ni distribuir el método.

## 6. Verificación

- `python3 scripts/check_sizes.py` → `OK`.
- `python3 -m unittest discover -s tests` → 16 tests, `OK`.
