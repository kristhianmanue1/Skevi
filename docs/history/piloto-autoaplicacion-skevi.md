# Piloto: Skevi aplicado a sí mismo

> Registro del primer piloto F0→F3 que exige el `README.md` para salir de
> Alpha. Documento de evidencia, no norma: si algo aquí contradice el
> estándar o la guía vigentes, ganan ellos (`AGENTS.md` §Prioridad).

## F0 — Análisis

### Problema y resultado observable

Problema: Skevi define un método para que agentes construyan proyectos,
pero nunca corrió su propio pipeline F0→F3 sobre un proyecto real — ni
siquiera sobre sí mismo. Sin eso, el método es una afirmación sin evidencia
de que funciona en la práctica.

Resultado observable: existe un piloto documentado con requisitos,
evidencia y ADRs reales, que un humano puede auditar para decidir si Skevi
sale de Alpha.

### Requisitos

```text
REQ-1 [funcional] [fuente: instrucción directa del humano, 2026-08-12]
Enunciado: producir un documento F0 (problema, resultado, REQ-*,
no-objetivos, restricciones, EV-*) sobre Skevi mismo.
Criterio de aceptación: docs/historia/piloto-autoaplicacion-skevi.md
existe y contiene todas las secciones del Definition of Ready de
01-analisis-y-requerimientos.md §3.2.
Prioridad: imprescindible

REQ-2 [funcional] [fuente: AGENTS.md "una regla sin fuente no es aplicable"]
Enunciado: formalizar en ADR las decisiones fundacionales que hoy sólo
viven como prosa en el README (gate local sin CI, separación de docs/ por
vida útil).
Criterio de aceptación: docs/adr/ADR-001-gate-local-sin-ci.md y
docs/adr/ADR-002-separacion-docs-por-vida-util.md existen con el formato de
02-specs-adr-contratos.md §3.2.
Prioridad: imprescindible

REQ-3 [funcional] [fuente: AGENTS.md "Verificación"]
Enunciado: el gate de estructura y tamaños sigue en OK después de agregar
los documentos del piloto.
Criterio de aceptación: `python3 scripts/check_sizes.py` devuelve exit 0 y
texto que empieza con "OK".
Prioridad: imprescindible

REQ-4 [funcional] [fuente: 04-ejecucion-y-verificacion.md §5]
Enunciado: cerrar el piloto con una ronda adversarial sobre los documentos
nuevos antes de reportarlo hecho.
Criterio de aceptación: existe un bloque "Ronda adversarial" en este
documento con Hallazgos, Verificaciones y Decisión.
Prioridad: imprescindible
```

### No objetivos

- No se reconstruye el cascarón (F2): ya existe. Se audita contra su
  checklist en vez de recrearlo.
- No se escriben specs (F1) ni contratos formales: Skevi no tiene código de
  aplicación ni fronteras de datos que contratar más allá del propio
  `check_sizes.py` (ver hallazgo abajo).
- No se agregan tests a `check_sizes.py` en este piloto — se registra como
  hallazgo, no se corrige aquí (una tarea, un objetivo).
- No se cambia el estado "Alpha" del README. Es una afirmación pública
  sobre el proyecto entero; queda como recomendación para decisión humana
  explícita, no la tomo unilateralmente.
- No se modifica `docs/estandar-diseno-software-github.md`,
  `docs/guia-agentes-ia/*` ni `docs/orquestacion/*`.
- Sin commit ni push como parte de este documento: se piden aparte.

### Restricciones

- Español, Markdown, formato exacto de las plantillas de `01`, `02` y `04`
  de `docs/guia-agentes-ia/`.
- Cualquier archivo nuevo debe pasar `scripts/check_sizes.py` (límite
  genérico de 800 líneas; sin Markdown operativo suelto en la raíz).
- `docs/adr/` no existía antes de este piloto; se crea porque
  `03-cascaron-proyecto.md` §2 ya la define como hogar canónico de ADRs.

### Evidencia

```text
EV-1: el repo no tenía carpeta docs/adr/ antes de este piloto |
`ls docs/` (previo a este cambio) → estandar-diseno-software-github.md,
guia-agentes-ia/, orquestacion/, historia/ (sin adr/)

EV-2: el gate pasaba antes de este piloto |
`python3 scripts/check_sizes.py` → "OK — 19 archivos de texto dentro de
límites; estructura y hogares canónicos verificados", exit 0

EV-3: scripts/check_sizes.py no tiene suite de tests |
`find . -iname "*test*" -not -path "*/.git/*"` → sin resultados relevantes
en scripts/; no existe tests/ ni test_check_sizes.py
```

### Preguntas abiertas (cerradas para este piloto)

```text
PREGUNTA-1: ¿hasta dónde forzar F1/F2 sobre un repo sin código?
Por qué importa: aplicar specs/contratos/cascarón al pie de la letra
generaría documentos vacíos o forzados, violando "sin generalidad
especulativa" (00-INDICE.md regla 4).
Opciones: (a) forzar las cuatro fases completas; (b) aplicar sólo lo que
el tamaño y naturaleza real del proyecto justifica (regla "mínimo
necesario", 00-INDICE.md regla 3).
Decisión: (b) — documentado y aprobado en el plan previo a esta tarea.
```

## F3 — Reporte de tarea

```text
TAREA piloto-autoaplicacion-skevi
Objetivo: cerrar un piloto F0→F3 sobre Skevi mismo, con ADRs formalizados
y evidencia real, sin alterar contenido normativo existente.
Base: commit b2f8ee9 (main)
Permitido: crear docs/adr/ADR-001-*.md, docs/adr/ADR-002-*.md,
docs/historia/piloto-autoaplicacion-skevi.md; ejecutar
scripts/check_sizes.py.
Prohibido: editar docs/estandar-diseno-software-github.md,
docs/guia-agentes-ia/*, docs/orquestacion/*, plantillas/*; cambiar el
estado Alpha del README; commit, push o cualquier operación de autoridad
separada.
DoD: REQ-1..4 cumplidos con criterio verificable; gate en OK; ronda
adversarial con decisión proceed o escalate.
Parada: cualquier hallazgo BLOCKER/HIGH sin corregir, o necesidad de tocar
un archivo fuera de "Permitido".
```

TAREA piloto-autoaplicacion-skevi: OK
DoD: cumplido — ver Evidencia abajo.
Evidencia:
- `python3 scripts/check_sizes.py` → "OK — 22 archivos de texto dentro de
  límites; estructura y hogares canónicos verificados", exit 0
- `git status --short` → sólo los 3 archivos nuevos listados en
  "Permitido"
Hallazgos fuera de alcance:
- `scripts/check_sizes.py` no tiene tests propios (EV-3). El checklist de
  F2 (`03-cascaron-proyecto.md` §8) exige un test real que pase; Skevi no
  lo cumple para su único artefacto ejecutable. Sugerido como tarea futura
  independiente, no se corrige aquí.

## Ronda adversarial

### Hallazgos

- [MED] El propio piloto es juez y parte: lo ejecuté yo, sin contexto
  fresco real ni otro modelo, para un cambio que la regla de rigor
  (`04` §5.3) califica como "cotidiano" (documentación, sin código ni
  release). Aceptado como riesgo: es la categoría correcta según esa
  regla, pero significa que un sesgo de "querer que el piloto salga bien"
  no está tan cubierto como en una ronda con sesión nueva. Seguimiento:
  si se usa este documento para justificar el cambio de Alpha a otro
  estado, esa decisión sí debería pasar por revisión humana o de modelo
  distinto antes, no sólo por esta ronda.
- [LOW] `docs/adr/` es carpeta nueva sin un `README.md` propio ni índice
  que la enumere (a diferencia de `guia-agentes-ia/00-INDICE.md`). Con dos
  ADRs no hace falta todavía; si crece a varios más, un índice evita que
  se vuelva una lista sin orden. Seguimiento opcional.
- [LOW] REQ-2 dice "decisiones fundacionales" en plural pero sólo cubre
  dos; hay otras decisiones implícitas en el repo (p. ej. por qué
  `plantillas/` existe como carpeta separada de `docs/`) sin ADR. Aceptado
  como riesgo: el alcance de este piloto se limitó explícitamente a las
  dos decisiones citadas en el plan aprobado; no es scope creep, es un
  límite declarado.

### Verificaciones

- `python3 scripts/check_sizes.py` → OK, exit 0 (ver Evidencia de F3)
- Relectura completa de ADR-001, ADR-002 y este documento contra el
  formato de `02-specs-adr-contratos.md` §3.2 y `01` §3.1/§6 → formato
  coincide campo a campo
- `git status --short` → sólo los 3 archivos nuevos esperados, sin
  cambios fuera de alcance

### Decisión

proceed

**Recomendación para decisión humana** (fuera del alcance de esta tarea):
con este piloto cerrado en `OK`, el README ya tiene la evidencia que él
mismo pide para salir de Alpha. Si quieren que actualice el estado, díganlo
explícitamente — no lo cambio por mi cuenta.
