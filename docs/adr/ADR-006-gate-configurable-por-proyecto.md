# ADR-006: gate configurable por proyecto adoptante

Estado: aceptado; implementado en `scripts/check_sizes.py`. Resuelve la
iniciativa A-6 diferida en `docs/proposals/PROP-002-decision-2026-08-15.md`.

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

El archivo admite cinco claves, con dos semánticas distintas y deliberadas:

- `limits`, `exempt_paths` y `skip_dirs` se **añaden** a los valores de Skevi:
  declarar un límite propio no hace perder los de `AGENTS.md`/`README.md`, y
  una exención no borra las que ya existían.
- `required` **reemplaza** por completo: la lista de archivos canónicos de
  Skevi no tiene significado fuera de este repositorio, así que un proyecto
  adoptante declara la suya, incluida una lista vacía si no quiere exigir
  ninguno.

Núcleo cerrado: una clave desconocida en `skevi-gate.json` falla el gate en vez
de ignorarse, para que un error de escritura sea detectable — la misma
polaridad que el estándar ya aplica a los límites de tamaño.

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

Verificación: `tests/test_check_sizes.py::ConfigTests` — ausencia de
configuración, clave desconocida, fusión de límites y exenciones, reemplazo de
`required`, y un caso extremo a extremo con una estructura que no es la de
Skevi.

Procedencia: PROP-002 §A-6 y su decisión del 2026-08-15; caso real de
`an-kla-memory` señalado por el humano el 2026-08-17.
