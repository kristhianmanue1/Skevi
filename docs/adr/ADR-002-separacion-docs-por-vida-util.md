# ADR-002: docs/ se separa por vida útil, no por tema

Estado: aceptado

Contexto: Skevi mezcla contenido con ritmos de cambio muy distintos: un
estándar de diseño que debería cambiar poco, una guía de fases que se ajusta
con la práctica, un método de orquestación acoplado a herramientas concretas
que caduca cuando esas herramientas cambian, y registro histórico que no
debería reescribirse nunca. Guardar todo eso en un único documento (o en
carpetas agrupadas por tema en vez de por vida útil) obliga a revisar lo
estable cada vez que se toca lo volátil, y arriesga que una edición de
"historia" reescriba silenciosamente lo que en realidad pasó.

Decisión: `docs/` se divide en cuatro carpetas por vida útil, no por tema:
`estandar-diseno-software-github.md` (capa normativa transversal,
atemporal), `guia-agentes-ia/` (pipeline F0→F3, cambia con la práctica),
`orquestacion/` (método concreto acoplado a herramientas, caduca con
ellas) e `historia/` (registro, no normativo, no se reescribe). Un
documento nuevo se coloca según cuánto se espera que dure sin cambiar, no
según su tema.

Alternativas descartadas:
  - Un único documento normativo con todo: minimiza archivos pero fuerza a
    releer y revisar lo atemporal cada vez que cambia una herramienta de
    orquestación; el diff de una edición vuelve ilegible qué cambió de
    verdad.
  - Carpetas por tema (`git/`, `agentes/`, `seguridad/`): agrupa contenido
    relacionado pero mezcla de nuevo vida útiles distintas dentro de la
    misma carpeta (p. ej. reglas de Git atemporales junto a notas de una
    herramienta específica de orquestación).

Consecuencias: una regla que aplica en dos fases (p. ej. contención de
tamaño) se referencia desde varios archivos en vez de vivir en uno solo por
tema — el propio estándar y estilo del proyecto exigen no parafrasear, sólo
referenciar la fuente única, así que esto no duplica contenido, sólo
enlaces. Mover un documento entre carpetas por un cambio de expectativa de
vida útil es una operación válida y esperada, no un error de organización.
