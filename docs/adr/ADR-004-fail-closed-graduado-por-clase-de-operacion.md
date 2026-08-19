# ADR-004: graduar el fail-closed por clase de operación

Estado: aceptado; implementado en f46dcca. Modifica el principio §1.5 del
estándar, que hasta ahora era absoluto.

Contexto: el principio 5 del estándar dice *"ante la incertidumbre, el sistema
se detiene en estado seguro; nunca asume permiso ni éxito por defecto"*. Es
simple y difícil de torcer, y ésa es su virtud.

Su defecto es de diseño, no de aplicación: **un principio sin gradación no da
vocabulario para distinguir dónde detenerse importa**. Obliga al ejecutor a
elegir entre parar ante todo —inaplicable— o decidir en silencio dónde no
aplicarlo, que es lo que acaba ocurriendo y no deja rastro.

Una ilustración de esta sesión muestra la forma del coste, aunque no lo pruebe
por sí sola: un clasificador de permisos bloqueó tres veces una operación
acotada y verificable, y la salida no fue una excepción estrecha sino conceder
`--dangerously-skip-permissions`, que autoriza cualquier herramienta. El caso es
anecdótico y el defecto inmediato era del clasificador, no del principio; se cita
porque **el patrón —cuando parar sale demasiado caro, el operador amplía la
autorización en bloque— es el que la gradación evita**, no como demostración.

`praxis/project-governance` resuelve esto colgando el bloqueo de la clase de
operación —*"para seguridad, publicación, políticas y decisiones aceptadas,
`unknown` bloquea"`*— en vez de la fase del proyecto. El eje es correcto: un
agente siempre encontrará que "está en desarrollo", y casi nunca notará por sí
solo que está tocando seguridad.

Decisión: el fail-closed se gradúa por clase de operación, con dos condiciones
que no son negociables.

**Clases protegidas — sin excepción posible.** Seguridad y autorización;
publicación y cualquier efecto fuera del entorno local; políticas y decisiones
ya aceptadas; datos de terceros; consumo de cuotas tarifadas o de recursos
compartidos; y toda operación irreversible. Ante incertidumbre en cualquiera de
ellas, el ejecutor se detiene.

**Quién clasifica, y qué pasa ante la duda.** La clase se deriva del **tipo de
operación**, no del juicio del ejecutor sobre su importancia. Y la regla que
cierra el hueco: **si hay duda sobre a qué clase pertenece una operación, es
protegida.** El fail-closed se aplica también a la clasificación, que es donde
un ejecutor podría reintroducir el sesgo que este ADR evita.

Cuando el contrato de tarea declara la clase por adelantado, el ejecutor **no
puede rebajarla en tiempo de ejecución**; sólo elevarla.

**Esto no toca §6.7.** El escalado ante evidencia inconsistente, alcance
excedido o permiso ausente sigue siendo incondicional: los tres disparadores
pertenecen a clases protegidas y ninguna gradación los alcanza.

**Fuera de esas clases**, la incertidumbre puede no detener el trabajo, y
entonces:

- el resultado se emite como **degradación declarada, con su razón**, nunca como
  silencio ni como éxito;
- la degradación no cierra ningún gate por sí sola;
- queda contable: un tercero debe poder enumerar después cuántas hubo y de qué
  tipo.

La clasificación es del **tipo de operación**, no del estado del proyecto ni de
la sensación del ejecutor sobre su importancia. No se adopta el término
`trabajo ordinario` de Praxis Dev: aparece cinco veces en su corpus sin
definirse, y tiene la misma forma que el `cotidiano vs crítico` que el piloto
Skopos demostró que un ejecutor resuelve a su favor 4 de 4 veces.

Alternativas descartadas:

- **conservar el absoluto**: mantiene una regla más simple, pero la evidencia de
  esta sesión muestra que su cumplimiento estricto empuja a la autorización en
  bloque, que es estrictamente peor;
- **copiar la excepción de Praxis Dev tal cual**: hereda un término sin definir
  y ata la excepción a la fase, que es el eje que un agente siempre encuentra
  favorable;
- **dejar la excepción a criterio del ejecutor sin declararla**: reproduce el
  fallo que el método ya midió — lo que no se emite, no se puede contar ni
  corregir.

Consecuencias: el principio §1.5 deja de ser una frase y pasa a necesitar la
lista de clases protegidas. Un ejecutor que hoy se detiene ante cualquier duda
podrá continuar en trabajo local reversible, y a cambio deberá emitir más
degradaciones explícitas. El corpus gana una obligación de emisión que antes no
tenía.

Verificación: la implementación debe incluir un caso por clase protegida en el
que la incertidumbre detiene, y un caso fuera de ellas en el que continúa
emitiendo degradación declarada. Una degradación sin razón, o un gate cerrado
sobre una degradación, son incumplimientos.

Procedencia: PROP-003 §3.1 y su decisión del 2026-08-17. Evidencia del coste del
absoluto: esta sesión, tres bloqueos consecutivos seguidos de autorización
amplia. Evidencia del fallo del calificador subjetivo:
`docs/history/piloto-skopos.md` F3.
