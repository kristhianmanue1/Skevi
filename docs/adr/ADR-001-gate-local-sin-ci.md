# ADR-001: gate de estructura y tamaños corre local, no en CI remoto

Estado: aceptado

Contexto: el proyecto necesita un gate que impida commits/push que rompan
la estructura canónica o los límites de tamaño (`estandar-diseno-software-github.md`
§3.4). La cuenta que aloja este repositorio tiene minutos de CI limitados en
GitHub Actions: se agotan rápido y se reinician mensualmente. Un gate que se
salta por falta de minutos, o que bloquea otros usos legítimos de esa cuota,
no protege nada.

Decisión: `scripts/check_sizes.py` corre como hook de Git local
(`scripts/hooks/pre-push`, instalado con
`git config core.hooksPath scripts/hooks`), no como workflow de GitHub
Actions. Ramas, commits, PRs, revisiones y push se siguen administrando con
`gh`; sólo la ejecución del gate se mantiene fuera de Actions.

Alternativas descartadas:
  - GitHub Actions en cada push: consume la cuota de minutos limitada de la
    cuenta en cada intento, incluidos los fallidos; no escala con el volumen
    de commits de un agente iterando.
  - Sin gate automatizado, sólo revisión manual: viola la regla "evidencia
    o no pasó" — un humano revisando a ojo no es una verificación repetible
    ni ejecutable.
  - Gate local sin hook (ejecución manual antes de cada push): mismo
    verificador, pero depende de que el ejecutor se acuerde de correrlo;
    el hook lo hace no opcional.

Consecuencias: el gate no corre en GitHub para un colaborador que clona el
repo sin instalar el hook — se pierde protección para pushes hechos sin
`core.hooksPath` configurado. No hay verificación visible en la interfaz de
PRs de GitHub (sin check de CI). Si en el futuro cambian los límites de
minutos de la cuenta, esta decisión se reevalúa explícitamente con un ADR
nuevo que la sustituya — no se agrega un workflow de Actions en silencio.
