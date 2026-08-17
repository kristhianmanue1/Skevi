# ADR-007: validar en la frontera implica fallar controlado

Estado: aceptado; añade un bullet a `estandar-diseno-software-github.md` §2.4.

Contexto: §2.4 ya exige *"validar toda entrada en la frontera, contra un
esquema cerrado"*, pero no dice qué debe ocurrir cuando la validación
encuentra algo inválido. En la práctica, "validar" se leyó como "comprobar
tipos con el feliz camino cubierto" y se dejó sin cubrir el infeliz: una
entrada mal tipada escapaba como la excepción cruda del lenguaje —
`AttributeError`, `TypeError`— en vez de un mensaje con el campo y el motivo.

El defecto apareció **dos veces, en dos repositorios distintos, en la misma
sesión**, lo que lo saca de la categoría de accidente puntual:

1. `an-kla-memory`, issue #84: el CLI aborta con traceback ante una excepción
   no prevista, filtrando rutas absolutas del sistema de archivos del
   firmante.
2. `scripts/check_sizes.py` de este mismo repositorio, durante la
   implementación de ADR-006: `apply_config({"limits": ["no", "dict"]})`
   lanzaba `AttributeError: 'list' object has no attribute 'items'` por
   encima del `except (ValueError, OSError)` de `main()`, verificado con
   ronda adversarial de contexto fresco antes de corregirse.

Ambos casos comparten la misma forma: un punto de entrada que lee
configuración externa —flags de CLI, un archivo JSON de proyecto— asume que
llegará con el tipo esperado, y dejaba escapar la excepción nativa cuando no
era así.

Decisión: *"validar en la frontera"* incluye fallar controlado. Toda entrada
externa —argumentos de CLI, archivos de configuración, variables de entorno,
payloads de red— que resulte inválida produce un mensaje que nombra el campo y
el motivo, nunca la traza cruda del lenguaje. Un stack trace no es un mensaje
de error: es una fuga de implementación, y con frecuencia lleva rutas
absolutas del sistema donde corre — que es información no confiable filtrada
justo donde el estándar prohíbe filtrarla (§2.3: *"nunca se registran
secretos... en logs, capturas o reportes"*; una ruta absoluta del host no es
un secreto, pero es la misma clase de fuga de entorno).

Esto no exige capturar `Exception` de forma indiscriminada en todo el
programa — eso convertiría errores de programación reales en códigos opacos y
dificultaría depurar. Se aplica **en el punto donde se lee la entrada externa**:
el parseo y la validación de esa entrada deben ser exhaustivos por tipo antes
de usarla, de modo que ninguna excepción nativa tenga oportunidad de escapar
desde ahí. Lo que ocurre después, con datos ya validados, puede seguir
fallando como errores de programación normales.

Alternativas descartadas:

- **Capturar `Exception` en el borde del programa (CLI `main`, handler HTTP)**:
  contiene la fuga, pero oculta errores de programación genuinos detrás de un
  código opaco y dificulta depurar el propio Skevi o sus adoptantes. Se
  prefiere prevenir la excepción en el punto de entrada de datos externos, no
  amortiguarla después de que ya ocurrió.
- **Dejarlo como buena práctica implícita en "validar toda entrada"**: es lo
  que ya regía y produjo el defecto dos veces; una regla que no se puede citar
  ni verificar no se aplica de forma consistente.

Consecuencias: cada frontera de entrada externa gana una obligación explícita
de validación por tipo, no sólo de forma. El coste es proporcional al riesgo:
un script pequeño sin entrada externa no necesita nada nuevo; un CLI o un
lector de configuración sí.

Verificación: no hay gate automático para esta regla —sería equivalente a
analizar estáticamente que ninguna excepción nativa cruza una frontera
declarada, fuera de alcance de `check_sizes.py`—. Se verifica por revisión: el
checklist de cumplimiento (§7) y la ronda adversarial (`04` §5) deben
comprobarlo explícitamente en cualquier tarea que introduzca un punto de
entrada de configuración externa. `tests/test_check_sizes.py::ConfigTests`
sirve de ejemplo de referencia: cada tipo mal formado tiene su caso y se
verifica que produce `ValueError` con mensaje, nunca la excepción cruda.

Procedencia: `an-kla-memory` issue #84 (2026-08-16); ronda adversarial sobre
ADR-006 (2026-08-17), hallazgo HIGH "tipos incorrectos en el JSON causan
excepciones no controladas", registrado en
`docs/adr/ADR-006-gate-configurable-por-proyecto.md`.
