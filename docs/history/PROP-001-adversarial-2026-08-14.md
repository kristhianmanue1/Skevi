# Ronda adversarial — PROP-001

**Fecha:** 2026-08-14
**Artefacto:** `../proposals/PROP-001-agent-native-model-improvements.md`
**Alcance:** coherencia, autoridad, seguridad y verificabilidad de la propuesta;
no evalúa una implementación todavía inexistente.
**Revisor:** revisión propia con contexto acotado al artefacto y contratos
aplicables. No se usó contexto fresco real porque el cambio es documental y no
activa los criterios obligatorios de F3 §5.3.
**Decisión inicial:** `fix-and-retry`

## Hallazgos

### F1 — HIGH — techo de autoridad incompleto

**Problema:** la propuesta colocaba conversación y `AGENTS.md` como fuentes de
autoridad sin reconocer que la política del host, sandbox o plataforma tiene
precedencia y que un archivo del target no puede ampliar capacidades.

**Impacto:** un repositorio analizado podría presentarse como fuente de permiso
para red, escritura o acciones externas y convertir al agente en confused
deputy.

**Corrección aplicada:** P0-01 ahora fija la política del host como techo, deja
la concesión de alcance a la conversación humana y limita los archivos
designados por el host a restringir o guiar dentro de ese alcance.

**Estado:** cerrado.

### F2 — HIGH — conformidad podía ocultar riesgo objetivo

**Problema:** `verify` sólo comprueba capacidades adoptadas y el no objetivo
prohibía declarar incumplimiento por prácticas no adoptadas, sin separar
conformidad de riesgo.

**Impacto:** un proyecto podría no adoptar una regla de seguridad y recibir un
reporte aparentemente limpio pese a una condición de pérdida de datos o ruptura
de interfaz observada.

**Corrección aplicada:** los modos separan conformidad y riesgo. `verify` se
limita a contratos adoptados; `assess` informa siempre riesgos objetivos de
corrección, seguridad, pérdida de datos y compatibilidad.

**Estado:** cerrado.

### F3 — HIGH — `inspect` no tenía una frontera de lectura segura

**Problema:** la primera versión declaraba read-only, pero no regulaba symlinks,
FIFOs, sockets, dispositivos, filtros Git ejecutables, targets demasiado amplios
ni agotamiento de presupuesto.

**Impacto:** un análisis de código no confiable podía escapar de la raíz, quedar
bloqueado leyendo un archivo especial, ejecutar un filtro del target o recorrer
el home completo mientras seguía llamándose read-only.

**Corrección aplicada:** P0-00 canonicaliza la raíz, acepta sólo archivos
regulares, rechaza targets amplios y symlinks externos, deshabilita external diff
y textconv, y convierte límites de archivos, bytes, tiempo y herramientas en
degradaciones explícitas.

**Estado:** cerrado.

### F4 — HIGH — bundles y contexto podían filtrar secretos

**Problema:** emitir fuera del target no definía clasificación, redacción,
permisos, atomicidad ni retención.

**Impacto:** `context` podía copiar credenciales o contenido privado a logs,
temporales o proveedores externos sin una autorización separada.

**Corrección aplicada:** P0-00 y P2-02 exigen inventariar omisiones, redactar
secretos, emitir con permisos restrictivos y retención declarada, preferir hashes
y punteros, y tratar toda salida fuera del host como operación externa.

**Estado:** cerrado.

### F5 — HIGH — `adopt` no era transaccional

**Problema:** permiso explícito no bastaba para impedir aplicar una propuesta
obsoleta, parcial o con alcance ampliado después de la revisión.

**Impacto:** un cambio entre `propose` y `adopt` podía sobrescribir trabajo o
dejar una adopción a medias sin recuperación reproducible.

**Corrección aplicada:** el artefacto queda content-addressed y la concesión se
liga a digest, SHA, rutas y capacidades. P0-07 exige preview, revalidación,
escritura atómica, recuperación e idempotencia con tests negativos.

**Estado:** cerrado.

### F6 — HIGH — no existía baseline honesto para proyectos existentes

**Problema:** recuperar requisitos y diseño podía aparentar que F0/F1 habían
ocurrido antes del código o exigir retrospectivamente un cascarón F2.

**Impacto:** Skevi fabricaría cumplimiento histórico y forzaría estructura en
repositorios que funcionan con otras convenciones.

**Corrección aplicada:** P0-06 introduce `BASELINED`, separa declarado,
observado e inferido, marca fases recuperadas como `recovered` y prohíbe cerrar
retroactivamente `F0: OK` sin evidencia contemporánea.

**Estado:** cerrado.

### F7 — MED — el adaptador Argos podía alterar semántica probatoria

**Problema:** la frontera sólo decía que Argos aportaba análisis profundo; no
prohibía renombrar relaciones, recalcular cobertura o perder fingerprints al
normalizar.

**Impacto:** Skevi podría convertir relaciones no probatorias en soporte o
presentar un bundle modificado como evidencia Argos intacta.

**Corrección aplicada:** el adaptador conserva el bundle nativo, referencia
`claim_id`/`evidence_id`, no reinterpreta relaciones ni cobertura y usa perfil
estático por defecto. Los fixtures compartidos deben probar preservación de
significado.

**Estado:** cerrado.

### F8 — MED — PROP-001 podía aceptarse como paquete monolítico

**Problema:** había muchas iniciativas con aceptación individual, pero no un
procedimiento para decidirlas por separado.

**Impacto:** aceptar la propuesta podía interpretarse como autorización para
implementar o instalar toda la secuencia.

**Corrección aplicada:** §7.1 exige decisión por iniciativa con estado,
dependencias y evidencia. `needs-spike` sólo permite investigación read-only;
cada implementación conserva ADR y contrato propios.

**Estado:** cerrado.

## Verificaciones

- `python3 scripts/check_sizes.py` → `OK — 27 archivos de texto dentro de
  límites; estructura y hogares canónicos verificados`.
- `python3 -m unittest discover -s tests` → 16 tests, `OK`.
- `git diff --check` → sin salida, exit 0.

## Riesgos residuales

- PROP-001 define interfaces conceptuales; aún no hay schemas ni ejecutable que
  demuestren el comportamiento.
- Argos está en prerelease y su CLI analítica pertenece a un incremento futuro;
  la integración debe permanecer opcional y fijada a versión.
- El estado de AN-KLA en Skevi sigue siendo no integrado; esta ronda no concede
  permiso para instalarlo.

## Decisión

`proceed`
