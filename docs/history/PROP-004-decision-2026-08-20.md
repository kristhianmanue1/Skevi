# PROP-004 — Decisión

> **Fecha:** 2026-08-20
> **Artefacto decidido:** [`PROP-004-metodos-desarrollo-agentes.md`](PROP-004-metodos-desarrollo-agentes.md) (v2)
> **Resultado:** A-1, A-2 y A-3 aceptadas; A-4 diferida con condición nombrada.
> **Responsable de la decisión:** maintainer de Skevi, en conversación, sobre
> la recomendación posterior a la ronda adversarial (`fix-and-retry`,
> 2026-08-20).
> **Efecto:** esta decisión produce ADR-009, ADR-010 y ADR-011, las
> ediciones de guía (`01` §2, `03` §2, `04` §1 y §3), la plantilla
> `templates/plan-de-implementacion.md` y el ajuste de `project-manifest.yaml`.

## 1. Decisiones

| ID | Decisión | Depende de | Evidencia exigida | Siguiente artefacto |
|---|---|---|---|---|
| A-1 | aceptar | — | ronda 2026-08-20 cerrada; disparadores de Bounded referencian `04` §5.3, no reformulados | ADR-009; guía `01` §2, `04` §1 |
| A-2 | aceptar como artefacto de escala | A-1 | fuente única frente a la TAREA; hogar y límite declarados | ADR-010; plantilla + `03` §2 + `04` §1 |
| A-3 | aceptar como default condicional | — | evidencia = salida del RED; condicionalidad heredada del estándar §3.2 | ADR-011; guía `04` §3 |
| A-4 | diferir | A-2 desplegada y pilotada | planes reales en uso en al menos un piloto con evidencia | ninguno hoy |

## 2. Por qué A-4 se difiere con condición y no se rechaza

El ámbito que A-4 declaraba escanear no existe hasta que A-2 produzca planes
reales; un gate siempre verde es el anti-patrón que `03` §3 prohíbe. La
detección por vocabulario de la v1 es eludible en un corpus en español y la
ronda midió 21 ocurrencias de la propia lista dentro de la v1. Cuando la
condición se cumpla, la reactivación evaluará **chequeo estructural** (cada
step referencia archivo/comando/test que existe y resuelve al momento del
gate, análogo al check CONTRATO↔código de `04` §9), no listas léxicas.

## 3. Lo que esta decisión no concede

- No des-pospone por completo los ítems 1 y 2 del manifiesto: A-1 define la
  puerta de entrada, pero el procedimiento completo y la generalización de
  plan/TDD quedan condicionados al piloto (secuencia §5 de la propuesta,
  paso 5).
- No adopta vocabulario de `obra/superpowers`: es Referencia que informa
  (tabla de fuentes de `01`), nunca evidencia que defina requisitos.
- No toca el estándar §1–§8; el BLOCKER de la ronda cerró esa rama para
  siempre en esta propuesta.
- No crea gate nuevo ni extiende `skevi-gate.json`; sólo añade la plantilla
  a los archivos requeridos del gate existente.

## 4. Secuencia cumplida

1. Ronda adversarial (2026-08-20), **anterior** a la decisión — el orden que
   PROP-001/002 establecieron y que la v1 de §4 invirtió.
2. v2 de la propuesta absorbiendo 1 BLOCKER + 6 HIGH + 6 MED.
3. Esta decisión.
4. ADRs + ediciones de guía + plantilla + manifiesto (este cambio).
5. Piloto real de A-1/A-2 sobre un cambio acotado en un repo del ecosistema
   — pendiente; condición para reactivar A-4.
