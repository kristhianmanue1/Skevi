# Skevi

Cuerpo normativo para diseñar software y para operar agentes de IA que crean y
mantienen proyectos. Dos capas: un **estándar** atemporal e independiente de
herramientas, y una **guía por fases** escrita para que la ejecute un agente.

**Nombre.** Del griego σκεύη (*skeví*, plural de σκεῦος/*skevos*: vasija,
utensilio, instrumento, equipamiento, arnés, aparejo) — un conjunto de
herramientas, no una sola. También se lee como forma corta de Παρασκευή
(*Paraskeví*, "preparación"): la fase F0 de la guía es, literalmente, eso.

**Audiencia primaria.** Este corpus está escrito para que lo ejecute un
agente de IA, no para que lo lea un humano de principio a fin. `AGENTS.md`
y `docs/ai-agent-guide/` asumen un ejecutor automatizado como lector. Las
secciones de revisión existen para que una persona audite el resultado, no
para que sea la vía principal de lectura.

No depende de ningún lenguaje, framework ni proveedor. Sólo asume Git y un
hospedaje tipo GitHub.

## Estructura

```text
Skevi/
├── AGENTS.md                  # punto de entrada para ejecutores automatizados
├── README.md
├── project-manifest.yaml      # qué ofrece y qué NO ofrece, frente al ecosistema
├── docs/
│   ├── adr/                                  # decisiones estructurales inmutables
│   ├── estandar-diseno-software-github.md   # capa normativa transversal
│   ├── ai-agent-guide/                     # pipeline F0→F3 para agentes
│   │   ├── 00-INDICE.md
│   │   ├── 01-analisis-y-requerimientos.md
│   │   ├── 02-specs-adr-contratos.md
│   │   ├── 03-cascaron-proyecto.md
│   │   └── 04-ejecucion-y-verificacion.md
│   ├── orchestration/                        # método concreto, acoplado a herramientas
│   │   ├── orquestacion-codex-opencode-tmux.md
│   │   └── orquestacion-codex-opencode-tmux-runbook.md
│   ├── proposals/                           # cambios bajo deliberación, no normativos
│   │   ├── PROP-001-agent-native-model-improvements.md
│   │   ├── PROP-001-decision-2026-08-15.md
│   │   ├── PROP-002-correcciones-desde-adoptantes.md
│   │   ├── PROP-002-decision-2026-08-15.md
│   │   └── PROP-003-frontera-con-praxis-dev.md
│   └── history/                            # registro, no normativo
│       ├── PROP-00N-adversarial-*.md        # rondas por propuesta
│       ├── drift-checkpoint-an-kla-2026-08-15.md
│       ├── orquestacion-codex-opencode-tmux-adversarial.md
│       ├── piloto-autoaplicacion-skevi.md
│       ├── piloto-skopos.md
│       └── supervision-agente-externo.md
├── templates/                 # formatos copiables, no se improvisan (§3.5)
│   ├── registro-contexto.md
│   └── skevi/
│       ├── usage-guide.md
│       └── architecture-overview.md
└── scripts/
    └── check_sizes.py         # gate de estructura y tamaños
```

La separación no es estética: cada carpeta tiene una **vida útil distinta**.
El estándar cambia poco, la guía cambia con la práctica, `orchestration/`
caduca cuando cambian las herramientas, `proposals/` vive mientras se delibera
un cambio y `history/` no debería cambiar nunca. Mezclarlas en un archivo obliga
a revisar lo estable cada vez que se mueve lo volátil.

## Cómo se usa

**Un agente que empieza un proyecto** lee `AGENTS.md`, luego
`docs/ai-agent-guide/00-INDICE.md`, y avanza por fases: análisis (F0) →
specs/ADRs/contratos (F1) → cascarón (F2) → ejecución y verificación (F3).
Cada fase tiene un gate que se cierra con evidencia, no con una declaración.

**Una persona que revisa trabajo** usa el checklist de cumplimiento del
estándar (§7) y el formato de ronda adversarial de la guía (`04` §5).

**Un proyecto que adopta el método** copia el estándar y la guía, fija sus
propios límites de tamaño por escrito, e instala el gate en su CI. Si su
estructura de directorios difiere de la de Skevi — otros nombres de ADR,
guía o plantillas, o ninguno de ellos —, declara `skevi-gate.json` en su raíz
en vez de editar `scripts/check_sizes.py`: el script se copia sin
modificación (ADR-006).

## Verificación

```bash
python3 scripts/check_sizes.py
```

Comprueba que existen los archivos canónicos, que no hay Markdown operativo
suelto en la raíz y que ningún archivo de texto excede su límite. `OK` o
`BLOQ` con código de salida distinto de cero.

```bash
python3 -m unittest discover -s tests
```

Corre la suite de `tests/` sobre `scripts/check_sizes.py` — el único
artefacto ejecutable del proyecto.

**Gate local, no GitHub Actions.** La cuenta que aloja este repositorio tiene
minutos de CI limitados (se agotan rápido y se reinician mensualmente). Por
eso el gate corre localmente, vía hook de Git (`scripts/hooks/`, instalado
con `git config core.hooksPath scripts/hooks`), en vez de un workflow de
GitHub Actions. Ramas, commits, PRs, revisiones y push se administran por
`gh` con la cuenta de administrador; sólo la ejecución del gate se mantiene
fuera de Actions. Si en el futuro cambian los límites de la cuenta, esto se
reevalúa explícitamente — no se agrega un workflow en silencio.

## Principios que lo sostienen

Ver `docs/estandar-diseno-software-github.md` §1 — fuente única. No se
resumen ni se parafrasean aquí: una paráfrasis es una segunda copia con otras
palabras, y envejece igual de mal que una copia literal.

## Estado

**Alpha.** El estándar y la guía pueden cambiar sin aviso previo; ninguna
fase F0→F3 corrió todavía de punta a punta sobre un proyecto real, y el gate
sólo se verifica localmente (sin CI remoto). Sube a versión estable cuando
exista un piloto F0→F3 completo con evidencia.

`docs/history/` conserva los registros del piloto que originó estas reglas,
incluida la ronda adversarial que corrigió el protocolo de orquestación. Ese
material es evidencia de procedencia, no norma vigente.
