# Ronda adversarial — PROP-002

**Fecha:** 2026-08-15
**Artefacto:** [`../history/PROP-002-correcciones-desde-adoptantes.md`](../history/PROP-002-correcciones-desde-adoptantes.md)
**Alcance:** validez de la evidencia citada, solidez de cada iniciativa y
cobertura de los retiros propuestos.
**Revisor:** el mismo agente que redactó la propuesta.
**Contexto:** `mismo` — no fresco, no decorrelacionado, sin segundo modelo.
**Decisión inicial:** `fix-and-retry`

> Los tres campos anteriores son los que A-1 propone exigir. Se declaran aquí
> por coherencia: esta ronda incumple el criterio de independencia que la propia
> propuesta pide, y por tanto no puede sustituir a una revisión con contexto
> fresco antes de aceptar ninguna iniciativa.

## Hallazgos

### F1 — BLOCKER — las cifras de §2.2 son falsas por medición defectuosa

**Problema:** los conteos de adopción se obtuvieron con `grep -E` sin límites de
palabra. El patrón `PARCIAL|BLOQ` cuenta cada aparición de "bloque", "bloquea",
"bloqueado"; `F0|F1|F2|F3` cuenta dígitos hexadecimales dentro de hashes;
`contexto fresco|independiente` cuenta la palabra común "independiente".

**Evidencia:**

| Afirmación de §2.2 | Medición original | Con `\b…\b` | Factor |
|---|---:|---:|---:|
| emd usa el vocabulario de estados | 130 archivos | **2** | 65× |
| emd usa las fases F0–F3 | 81 archivos | **3** | 27× |
| emd declara contexto fresco/independencia | 111 archivos | **6** | 18× |
| emd hace rondas adversariales | 163 archivos | 41 (frase exacta) | 4× |

`fail-closed` (61) resiste la comprobación: es un término sin colisiones.

**Impacto:** tres de las cuatro cifras que sostienen la sección de evidencia
están infladas entre 18× y 65×. Una propuesta cuyo argumento central es "medí lo
que hicieron los adoptantes" no puede apoyarse en una medición que no distingue
`BLOQ` de `bloqueado`.

**Corrección exigida:** reescribir §2.2 con las cifras verificadas y añadir el
método de medición, para que sea reproducible y refutable.

### F2 — HIGH — P0-04 se revivió sobre la cifra falsa

**Problema:** §4 conserva P0-04 (unificar el vocabulario de estados) con la
justificación "130 archivos de emd lo usan". El número real es **2 archivos en
emd y 3 en alubia**.

**Impacto:** la iniciativa se rescató de un rechazo previo con evidencia
inexistente. Con los datos correctos, el vocabulario `OK | PARCIAL | BLOQ` es lo
que **menos** viaja de todo el corpus.

**Corrección exigida:** P0-04 vuelve a `rejected`, con la misma razón que tenía
antes de la medición errónea.

### F3 — HIGH — A-1 sustituye una autocertificación por otra

**Problema:** A-1 exige declarar `revisor`, `contexto` y `modelo`, pero los tres
campos los escribe el mismo ejecutor que hizo (o no hizo) la ronda. Nada impide
escribir `contexto: fresco` sin que lo sea. El método pasa de "ronda
autocertificada" a "independencia autocertificada", y el segundo estado es peor
que el primero: produce falsa seguridad y un campo que un gate puede leer como
si probara algo.

**Impacto:** un agente podría cerrar un gate que exige revisión independiente
sin ninguna revisión independiente, y el registro parecería conforme.

**Corrección exigida:** polaridad cerrada sobre la procedencia del campo. El
valor `fresco` sólo es admisible cuando existe un rastro verificable por un
tercero —identificador de subagente, sesión distinta, modelo distinto
registrado—; sin ese rastro el valor obligatorio es `mismo`. La ausencia de
evidencia degrada, nunca promueve.

### F4 — HIGH — A-3 abre una vía de escape en el punto exacto donde el método ya falló

**Problema:** A-3 introduce la clase "soft gate", que se registra sin detener la
tarea. El fallo mejor documentado de este método es que el ejecutor, ante una
clasificación de rigor con dos niveles, elige el bajo: el piloto Skopos lo hizo
4 de 4 veces sobre un componente con inyección de prompt explotable.

Añadir una categoría no bloqueante sin cerrarla es entregarle al ejecutor
exactamente la palanca que ya demostró que usa mal. emd puede sostenerla porque
tiene controlador humano y auditor independiente; un adoptante en solitario, no.

**Corrección exigida:** la lista de soft gates es **cerrada y enumerada**, y todo
lo no enumerado es hard por defecto. Es la misma polaridad cerrada que el
estándar ya aplica a los límites de tamaño (§3.4). Sin ese cierre, A-3 se
rechaza.

### F5 — MED — A-2 impone a un repositorio limpio un procedimiento diseñado para 599 MiB de producción

**Problema:** default deny, allowlist, cuarentena y promoción con manifiesto son
proporcionados para derivar un workspace desde un snapshot de producción con
tres superficies mezcladas y datos clínicos. Aplicarlos a un repositorio Git
propio, limpio y sin datos de terceros contradice la regla 3 del índice
("mínimo necesario").

**Corrección exigida:** condicionar A-2 a disparadores observables —el origen no
es un repositorio Git propio y limpio, o contiene datos de terceros o secretos—
reutilizando los disparadores que la guía ya define en `04` §5.3. En el caso
simple basta declarar las fases como `recuperadas`.

### F6 — MED — el retiro no cubre las 16 iniciativas

**Problema:** PROP-001 tiene 16 iniciativas. PROP-002 retira 9 y conserva 6:
quince. **P2-01** (versión, distribución y desviaciones) no aparece en ninguna
lista.

**Impacto:** no es un olvido inocuo. A-7 se apropia de la mitad de P2-01 —la
declaración de procedencia fijada— y deja sin decidir la otra mitad: qué ocurre
cuando el método avanza y el adoptante quedó anclado a un commit. Un adoptante
con procedencia fijada y sin procedimiento de actualización acumula drift
silencioso, que es el problema que P2-01 existía para resolver.

**Corrección exigida:** decidir P2-01 explícitamente, o declarar A-7 como su
sustituta parcial y registrar la mitad no cubierta como pendiente.

### F7 — MED — A-6 duplica norma existente y le atribuye a emd una invención ajena

**Problema:** el estándar §3.4 ya dice: *"Polaridad cerrada. Todo archivo de
texto queda sujeto al límite salvo exención explícita… Exentar es una decisión
que se registra con su motivo: un documento histórico congelado se exenta, uno
que sigue creciendo se parte."*

La mitad de A-6 —exenciones declaradas, contenido congelado como caso
canónico— **ya está normada**. Y la tabla de §2.3 lista "exención de gate para
contenido congelado" como pieza que emd tuvo que inventar: emd aplicó una regla
que ya existía.

**Impacto:** infla la lista de huecos del método, que es el argumento central de
la propuesta.

**Corrección exigida:** reducir A-6 a lo único nuevo —la extensibilidad del gate
por proyecto, evidenciada por alubia— y corregir la tabla de §2.3.

### F8 — MED — sesgo de selección y de supervivencia no declarados

**Problema:** §2.4 admite muestra pequeña y autor común, pero omite dos sesgos
mayores. Primero, `alubia` y `emd` no salieron de la medición: los señaló el
humano después de que el análisis inicial no los encontrara, porque viven fuera
del directorio inspeccionado. Segundo, sólo se observan adopciones vivas: un
proyecto que probó Skevi y lo abandonó no aparece, y el abandono es
precisamente la señal más informativa sobre qué partes del método estorban.

**Corrección exigida:** declarar ambos sesgos y bajar la fuerza de las
afirmaciones que dependen de la convergencia entre adoptantes.

### F9 — LOW — A-5 renuncia a la validación automática sin declararlo

**Problema:** A-5 norma ocho campos y no su representación, con lo que gana
flexibilidad y **pierde** la validabilidad automática que era el argumento de
P0-03. Es un intercambio defendible, pero la propuesta lo presenta como mejora
sin coste.

**Corrección exigida:** declarar el intercambio en el texto de A-5.

## Verificaciones

- `grep -rlE "\b(PARCIAL|BLOQ)\b"` sobre `emd` → 2 archivos, frente a 130 del
  patrón sin límites de palabra.
- `grep -rlE "\bF[0-3]\b"` → 3 en `emd`, 18 en `alubia`.
- `grep -rl "contexto fresco"` → 6 en `emd`, 2 en `alubia`.
- `grep -rl "ronda adversarial"` → 41 en `emd`, 1 en `alubia`.
- `grep -nE "^### P[0-9]-[0-9]{2}"` sobre PROP-001 → 16 iniciativas; PROP-002
  menciona 15.
- `sed -n '144,152p'` del estándar → confirma que las exenciones declaradas ya
  están normadas.

## Hallazgo positivo, no corregir

Las cifras corregidas revelan algo que la versión inflada ocultaba: **los dos
adoptantes profundos tomaron subconjuntos disjuntos**. `alubia` tomó la
maquinaria de fases (18 archivos) y casi nada de la ronda adversarial (1);
`emd` tomó la ronda adversarial (41) y el rigor fail-closed (61), y casi nada de
las fases (3). Ninguno tomó el vocabulario de estados.

Eso refuerza A-7 mucho más que las cifras infladas: si dos adoptantes serios
eligen partes disjuntas del mismo corpus, declarar qué se adoptó deja de ser
higiene y pasa a ser la única forma de que un agente sepa qué reglas rigen en el
repositorio donde acaba de aterrizar.

## Riesgos residuales

- La propuesta sigue basándose en cuatro adoptantes de un solo autor humano.
- Ninguna iniciativa tiene todavía ADR ni fixture; la aceptación de A-1…A-9 no
  autoriza modificar el estándar ni la guía.
- Esta ronda no es independiente. Antes de aceptar A-1, A-3 o A-4 —las tres que
  cambian cómo se clasifica el rigor— corresponde una revisión con contexto
  fresco real.

## Estado tras la corrección

| Hallazgo | Corrección aplicada | Estado |
|---|---|---|
| F1 | §2.2 reescrita con cifras verificadas y método de medición declarado | cerrado |
| F2 | P0-04 vuelve a `rejected`, con la cifra real y la nota del artefacto de medición | cerrado |
| F3 | A-1 incorpora polaridad cerrada: sin rastro verificable por un tercero, el valor obligatorio es `mismo` | cerrado |
| F4 | A-3 invierte el cierre: la lista enumerada es la de soft; lo no enumerado es hard | cerrado |
| F5 | A-2 se condiciona a disparadores observables de `04` §5.3 | cerrado |
| F6 | P2-01 declarada parcialmente sustituida por A-7, con la mitad no cubierta registrada como pendiente | cerrado |
| F7 | A-6 reducida a extensibilidad; la exención de contenido congelado se retira de la tabla de huecos | cerrado |
| F8 | §2.4 declara sesgo de selección y de supervivencia | cerrado |
| F9 | A-5 declara el intercambio: pierde validación automática | cerrado |

Verificación posterior: `python3 scripts/check_sizes.py` → `OK — 31 archivos`;
`python3 -m unittest discover -s tests` → 16 tests, `OK`; barrido de enlaces
relativos de ambos artefactos → 0 rotos.

## Decisión

`fix-and-retry` aplicado → **`proceed` condicionado**. La propuesta puede
discutirse, pero A-1, A-3 y A-4 —las tres que cambian cómo se clasifica el
rigor— no deberían aceptarse sin una revisión con contexto fresco real, por la
razón que esta misma ronda ejemplifica: fue el propio autor quien revisó, y los
dos hallazgos bloqueantes salieron de ejecutar comandos, no de releer el texto.
