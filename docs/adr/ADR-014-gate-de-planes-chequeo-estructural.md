# ADR-014: Gate de planes con chequeo estructural mínimo — A-4 reactivada

Estado: aceptado; implementa A-4 de PROP-004 (diferida con condición
cumplida el 2026-08-20: PLAN-0002 de orbitaNova ejecutado con evidencia,
PR #11).

Contexto: la condición de reactivación exigía planes reales antes de
construir el gate, para no repetir el anti-patrón "siempre verde" que la
primera ronda de PROP-004 bloqueó (ámbito inexistente). Skevi no tenía
planes propios: el gate habría sido vacuo también aquí. La salida fue
dogfooding — el primer plan de skevi (`docs/plans/2026-08-20-a4-gate-de-planes.md`)
es el plan de este mismo gate, y el gate lo verifica.

Decisión: `scripts/check_plans.py`, separado de `check_sizes.py` (estructura
de planes ≠ estructura y tamaños; cada script una responsabilidad), con
configuración **compartida** vía `skevi-gate.json` y una clave nueva
`plans` (directorio de planes). Chequeo **estructural** E1–E5: ≥1 bloque
TAREA **dentro de fences**; cada TAREA con Consumes/Produce/Steps; ≥1
checkbox por TAREA; cada step con `verificación:` (dos puntos, steps
multilínea agrupados); en todo el bloque, cada ruta backtickada con
extensión conocida existente y **contenida en el repo** — las que escapan
fallan, las URLs se ignoran, y las líneas con crea/crear/creamos quedan
exentas. **Fail-closed doble**: sin clave `plans`, el gate declara
"inactivo" y sale 0; clave presente con tipo inválido es BLOQ — un typo no
puede apagar el gate. Modo de archivos explícitos para evidencia sobre
planes de cualquier repo, resolviendo cada uno contra su propio repo.

Alternativas descartadas:

- **Extender `check_sizes.py`**: mezcla dos responsabilidades y su nombre
  miente; la config compartida ya evita la divergencia que motivaría
  juntarlos.
- **Listas léxicas (TBD, TODO, "similar a")**: rechazadas por la ronda
  adversarial de PROP-004: eludibles cambiando palabras, falsos positivos
  con citas legítimas.
- **No construir el gate**: la condición estaba cumplida y el corpus exige
  que las reglas del método se verifiquen mecánicamente donde se pueda
  (§3.4 del estándar); sin gate, la plantilla de plan es una sugerencia.

Consecuencias: skevi verifica su propio plan (no vacuo por diseño);
adoptantes lo activan con una línea de config — **copiando ambos scripts**:
la clave `plans` vive en el conjunto cerrado compartido y un `check_sizes`
desactualizado la rechaza con BLOQ (el pre-push hook también corre ambos).
Límites declarados en el plan fundacional: E5 sólo ancla tokens backtickados
con extensión conocida y sin esquema — es un ancla, no un notario.
Hallazgo de la corrida de evidencia: PLAN-0001 de orbitaNova (plan técnico
**de deliberación**) falla E1 honestamente — es otro género; el gate
estructura planes **ejecutables** (ADR-010), no propuestas. Los tests viven
en `tests/test_check_plans.py`: 11 en RED antes del script; los 12 restantes
anclan los hallazgos de la ronda adversarial del 2026-08-20 (23 en total,
incluyendo `main()` vía subprocess).

Verificación: `python3 scripts/check_plans.py` → OK sobre el plan propio;
`python3 -m unittest discover -s tests` → 51 tests (39 + 12); corrida de
evidencia transcrita en el registro del piloto correspondiente.

Procedencia: PROP-004 decisión §A-4 y su condición;
`docs/plans/2026-08-20-a4-gate-de-planes.md` (REQ-1..4); ADR-006 (config
compartida de polaridad cerrada); rondas adversariales de PROP-004
(vocabulario eludible, gate vacuo).
