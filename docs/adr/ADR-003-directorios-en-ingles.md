# ADR-003: directorios canónicos en inglés

Estado: aceptado; sustituye la parte de nombres de ADR-002, conserva su
criterio de separación por vida útil.

Contexto: la instrucción directa del humano del 14 de agosto de 2026 exige que
todas las carpetas del repositorio estén en inglés y que la estructura siga
convenciones habituales de software. ADR-002 decidió separar documentación por
vida útil, pero fijó tres nombres de directorio en español. La nueva propuesta
agent-native necesita además un hogar temporal de deliberación que no se
confunda con norma, operación ni historia.

Decisión: conservar la separación por vida útil de ADR-002 y usar estos hogares
canónicos:

- `docs/ai-agent-guide/`: guía normativa por fases;
- `docs/orchestration/`: métodos acoplados a herramientas;
- `docs/history/`: evidencia histórica inmutable;
- `docs/proposals/`: cambios bajo deliberación, sin efecto normativo;
- `templates/`: artefactos copiables.

Los nombres de archivos existentes no cambian en esta decisión. Una propuesta
se congela al aceptarse, rechazarse, aceptarse parcialmente o ser sustituida.
Las partes aceptadas producen ADR y tareas independientes antes de modificar la
norma. El README describe los hogares actuales y el gate verifica sus rutas.

Alternativas descartadas:

- conservar nombres mixtos: evita un diff amplio, pero contradice la convención
  explícita y mantiene una interfaz de repositorio inconsistente;
- traducir también todos los archivos: daría uniformidad total, pero amplía la
  migración sin necesidad para cumplir la regla sobre carpetas y multiplica las
  referencias históricas afectadas;
- usar `docs/roadmap/` para PROP-001: presupone iniciativas aceptadas; una
  propuesta todavía puede rechazarse o dividirse.

Consecuencias: referencias, templates, gate y tests deben usar los nombres
nuevos en el mismo cambio. Los registros históricos conservan las rutas que
eran reales cuando se produjeron; sólo sus enlaces vivos pueden apuntar a los
hogares actuales. Cualquier consumidor externo de las rutas anteriores necesita
migración explícita. La decisión no autoriza commit, push ni publicación.
