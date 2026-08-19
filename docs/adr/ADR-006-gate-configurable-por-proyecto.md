# ADR-006: gate configurable por proyecto adoptante

Estado: aceptado; implementado en `scripts/check_sizes.py`. Resuelve la
iniciativa A-6 diferida en `docs/history/PROP-002-decision-2026-08-15.md`.

Contexto: `scripts/check_sizes.py` codifica dos cosas distintas en las mismas
constantes: los valores que Skevi usa sobre sí mismo (`REQUIRED`, `LIMITS`,
`SKIP_DIRS`) y el mecanismo genérico de contención de tamaño que el estándar
§3.4 exige a cualquier proyecto. Un adoptante que copia el script hereda
también `REQUIRED`, la lista de archivos canónicos de **Skevi** —
`docs/estandar-diseno-software-github.md`, la guía en inglés, las plantillas—,
que no existen en su repositorio salvo que copie la estructura completa.

`an-kla-memory` es el caso real que expone el problema: es anterior a Skevi,
usa `docs/architecture/` en vez de `docs/adr/`, tiene su propio índice de ADR y
su propio gate. Adoptar `check_sizes.py` tal cual le exigiría reestructurarse
para que el gate lo acepte, que es exactamente lo que §3.4 y la regla 3 del
índice prohíben: imponer estructura que el tamaño real del proyecto no
justifica.

PROP-002 diferió A-6 con el argumento de que nadie había reportado fricción.
La fricción es estructural, no reportada: el gate de Skevi es hoy inservible
fuera de Skevi sin editar el script copiado.

Decisión: `check_sizes.py` lee `skevi-gate.json` en la raíz del proyecto si
existe. Ausente, se comporta exactamente como hoy — es el caso de Skevi sobre
sí mismo, que no declara configuración propia.

El archivo admite seis claves, con dos semánticas distintas y deliberadas:

- `limits`, `exempt_paths`, `skip_dirs` y `root_markdown` se **añaden** a los
  valores de Skevi: declarar un límite propio no hace perder los de
  `AGENTS.md`/`README.md`, una exención no borra las que ya existían, y un
  proyecto con `CONTRIBUTING.md` o `SECURITY.md` en la raíz —como
  `an-kla-memory`— los declara sin perder `AGENTS.md`/`CLAUDE.md`/`README.md`.
- `required` **reemplaza** por completo: la lista de archivos canónicos de
  Skevi no tiene significado fuera de este repositorio, así que un proyecto
  adoptante declara la suya, incluida una lista vacía si no quiere exigir
  ninguno.

Núcleo cerrado: una clave desconocida en `skevi-gate.json` falla el gate en vez
de ignorarse, para que un error de escritura sea detectable — la misma
polaridad que el estándar ya aplica a los límites de tamaño. Cada valor se
valida por tipo antes de usarse: un `limits` mal formado o un `default_limit`
que no es entero producen `BLOQ` con el motivo exacto, nunca la traza cruda de
una excepción de Python — el mismo requisito que este gate le exige al resto
del corpus.

**Superficie de rutas cerrada.** `required` y `exempt_paths` aceptan rutas de
texto libre en el JSON, y `(ROOT / relative).is_file()` resuelve una ruta
absoluta fuera de `ROOT` sin protestar: sin validación, un `required` con
`/etc/passwd` se da por cumplido con un archivo del sistema operativo del
firmante de CI, no del repositorio. Cada ruta se resuelve contra `ROOT` con la
misma función que ya protegía el bloque `skevi:registry` (`_resolve_registry_path`,
generalizada a `_resolve_project_path`) y se rechaza si es absoluta, empieza
por `~` o escapa de la raíz. `skip_dirs` y `root_markdown` no llevan esa
validación porque no se resuelven como rutas: se comparan contra componentes
de ruta o nombres de archivo ya descubiertos dentro de `ROOT`, así que un valor
malicioso no tiene nada que igualar.

**Sin acumulación entre invocaciones.** `apply_config` muta constantes de
módulo (`LIMITS`, `REQUIRED`, `SKIP_DIRS`, `EXEMPT_PATHS`, `ROOT_MARKDOWN`,
`DEFAULT_LIMIT`) in situ. `main()` llama a `reset_to_skevi_defaults()` antes de
leer la configuración del proyecto, restaurando desde una instantánea congelada
al importar el módulo. Si `main()` se invocara dos veces en el mismo
proceso, la segunda no hereda por acumulación silenciosa lo que declaró la
primera.

Alternativas descartadas:

- **Reescribir `REQUIRED`/`LIMITS` a mano en cada copia del script**: es lo que
  ya ocurre y lo que produce la fricción; cada adopción diverge en silencio del
  script canónico y una corrección futura no se propaga.
- **Un segundo script separado para adoptantes**: duplica el mecanismo de
  contención de tamaño en dos archivos que deben mantenerse sincronizados,
  contra el principio de hogar canónico único.
- **`required` aditivo como los demás campos**: partir de la lista de Skevi y
  sumarle la propia seguiría exigiendo archivos de Skevi que el adoptante no
  tiene; se descarta por la misma razón que motiva este ADR.

Consecuencias: `check_sizes.py` se convierte en un artefacto copiable sin
edición — la línea que faltaba para que "instala el gate en su CI" (README) sea
literal y no una promesa que exige reescribir el script. Un proyecto adoptante
gana un archivo más que mantener, pero uno declarado y versionable, no una
divergencia silenciosa del script.

Riesgo residual aceptado, no mitigado en código: nada impide que alguien añada
`skevi-gate.json` al propio repositorio de Skevi y debilite su gate en
silencio — por ejemplo con `required: []`. Se descartó detectarlo con una
heurística que reconociera "archivos propios de Skevi", porque contradice
directamente el objetivo de este ADR: un script idéntico para Skevi y para
cualquier adoptante, sin lógica que distinga entre ellos. La mitigación es de
proceso, no de código: una revisión de PR que note un `skevi-gate.json` nuevo
en la raíz de este repositorio.

Verificación: `tests/test_check_sizes.py::ConfigTests`, 24 casos — ausencia de
configuración, clave desconocida, fusión y reemplazo por campo, rutas
absolutas y que escapan de `ROOT` en `required`/`exempt_paths`, tipos
incorrectos en `limits`/`default_limit`/`skip_dirs` (incluido `bool` como
entero), `root_markdown` aditivo, ausencia de traza cruda ante configuración
malformada, dos invocaciones consecutivas de `main()` sin fuga de estado, y un
caso extremo a extremo con la estructura real de `an-kla-memory`: otra
jerarquía de directorios y Markdown de gobierno de proyecto adicional en la
raíz. Más un smoke manual: el script copiado sin ninguna edición pasa sobre esa
misma estructura simulada.

Procedencia: PROP-002 §A-6 y su decisión del 2026-08-15; caso real de
`an-kla-memory` señalado por el humano el 2026-08-17. Ronda adversarial con
contexto fresco y proveedor distinto (`agy`/`gemini-3.1-pro-high`) sobre la
primera versión de este cambio: `fix-and-retry` con 1 BLOCKER, 2 HIGH, 1 MED y
1 LOW — el BLOCKER (`ROOT_MARKDOWN` fijo invalidaba el caso de `an-kla-memory`
que este ADR dice resolver) y los dos HIGH (rutas sin validar en `required`,
tipos sin validar filtrando trazas crudas) verificados y corregidos; el LOW
aceptado como riesgo residual de proceso, arriba.
