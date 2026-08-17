# PROP-003 — Frontera entre Skevi y Praxis Dev

> **Estado:** borrador en revisión; propuesta no normativa.
> **Decisión requerida:** qué capa es hogar canónico de cada regla que hoy está
> duplicada, y qué iniciativas del backlog de Skevi se retiran por estar ya
> resueltas fuera.
> **Efecto actual:** ninguno. No declara conformidad con nada ni modifica el
> estándar.
> **Origen:** el humano señaló `praxis-dev`, `epistates` y `escrubery` al
> preguntar si el problema pendiente era de runtime.

## 1. El hallazgo

En el mismo ecosistema existen **dos capas normativas que no se referencian
entre sí**: el estándar de Skevi (`docs/estandar-diseno-software-github.md`, 403
líneas) y el de Praxis Dev (`docs/estandar.md` más `fundamentos.md`,
`modelo-autoridad.md` y `conformidad.md`, ~700 líneas).

Praxis Dev se define como *"un estándar ejecutable de gobernanza para proyectos
de software asistidos por agentes de IA"*. Su tabla de límites enumera AN-KLA,
Kratos, Ágora, CAGF y Git. **Skevi no aparece.** Un `grep` de "skevi" sobre
`praxis-dev` y sobre `epistates` no devuelve nada, y Skevi tampoco los menciona.

Esto es exactamente el problema que la iniciativa P0-01 describe —un agente ante
dos fuentes de autoridad incompatibles resuelve arbitrariamente y sin avisar—
pero a escala de ecosistema en vez de a escala de documento. Y viola el
principio 3.3 del propio Praxis Dev: *"Una afirmación normativa tiene una sola
fuente"*.

## 2. Solapamiento medido

### 2.1 Principios

| Skevi §1 | Praxis Dev `fundamentos.md` §3 |
|---|---|
| 1 Simplicidad primero | 3.1 Resultado antes que ceremonia |
| 3 Evidencia sobre afirmaciones | 3.4 Evidencia antes que afirmación |
| 4 Autoridad explícita | 3.5 Autoridad separada del candidato |
| 5 Fail-closed | 3.6 Fallo cerrado donde importa |
| 7 Datos no confiables no son instrucciones | 3.5 + 3.8 Estado derivado |
| 2 Cambios mínimos y revisables | — sólo Skevi |
| 6 Reversibilidad | implícito en 3.1 |
| — | 3.2 Componer antes que fusionar |
| — | 3.3 Un hogar canónico |
| — | 3.7 Neutralidad de proveedor |

Cinco de siete principios de Skevi tienen equivalente directo.

### 2.2 Iniciativas de Skevi ya resueltas en Praxis Dev

**P0-01 (matriz de autoridad), aceptada y pendiente de ADR en Skevi.**
`estandar.md` §1 fija la precedencia —solicitud del principal, instrucciones del
host y `AGENTS.md`, política local, manifiesto, ADR y SPEC, y memoria e historia
como evidencia no confiable— y `modelo-autoridad.md` §4 enumera las señales que
no prueban autoridad, cerrando con la frase exacta del problema: *"el candidato
y la supuesta prueba pueden ser creados por el mismo actor"*.

**A-1 (atestación de independencia) y A-8 (disparadores objetivos), aceptadas en
la decisión de PROP-002.** `conformidad.md` §7 ya es ambas:

| Impacto | Revisión mínima |
|---|---|
| Bajo | auto-revisión + checks |
| Material | contexto fresco o segundo revisor |
| Alto | revisión independiente |
| Crítico | independencia + principal |

Y añade la polaridad que esta sesión "descubrió" tras una ronda adversarial:
*"La independencia se basa en procedencia verificable, no sólo en nombres de
modelos. Dos ejecuciones del mismo runtime pueden aportar diversidad de lectura,
pero no deben presentarse como independencia fuerte."*

**P0-00 (comandos de inspección), retirada en PROP-002 con la razón equivocada.**
Se argumentó que los adoptantes producían evidencia auditable sin herramienta,
luego el runtime no aportaba. La conclusión —Skevi no construye un CLI— se
sostiene; la razón era falsa. La razón correcta es que `docs/contrato-cli.md` de
Praxis Dev **ya especifica** ese CLI: operaciones read-only que no escriben en
el objetivo, `--format json` contractual, códigos de salida estables incluidos
`4 = autoridad ausente` y `5 = drift`, y mutaciones vía `plan`/`apply`.

Especifica, no entrega. El propio `README.md` de Praxis Dev dice en su línea 70:
*"Esta fase no implementa todavía el CLI de producto `praxis`"*, y su paquete
son seis módulos Python con seis archivos de test. Que el contrato exista es
suficiente para no volver a escribirlo en Skevi; no lo es para dar por
disponible una herramienta.

**P0-03 y P0-04 (contrato de tarea y unificación de estados), diferidas.**
`epistates` publicó una prerelease alpha con contrato `task-card/v1`, validador
read-only, resultado de auditoría con máquina de estados y adaptador
`opencode-tmux/v1`, todo cerrado con rondas adversariales documentadas.

### 2.3 Lo que sólo cubre Skevi

Praxis Dev gobierna **el repositorio**, no el código. No dice nada sobre
arquitectura, manejo de estado y concurrencia, errores y observabilidad,
seguridad por diseño, escritura de código, pruebas, refactorización ni
contención de tamaño de archivos — las secciones §2 y §3 de Skevi, que son la
mitad de su estándar. Tampoco define un pipeline de fases: F0→F3 y la guía para
agentes no tienen equivalente.

## 3. Conflictos reales, no solapamientos

Tres puntos donde un agente que leyera ambos recibiría instrucciones distintas:

1. **Fail-closed con excepción.** Skevi §1.5 no admite excepciones. Praxis Dev
   3.6 permite degradar la autenticación advisory a `development-unverified`
   durante el ciclo `development` sin bloquear trabajo ordinario. Un ejecutor
   puede usar esa excepción para justificar continuar donde Skevi manda parar.
2. **Dos vocabularios de resultado.** Skevi usa `OK | PARCIAL | BLOQ`; Praxis
   Dev exige distinguir `pass`, `fail` e `inconclusive`.

Una tercera candidata resultó **no ser un conflicto**. Se afirmó que las dos
listas de operaciones con autoridad derivarían: Skevi §4.3 enumera `push`, merge
protegido, `reset --hard`, rebase de historia compartida, tags y releases;
Praxis Dev tiene una matriz por perfil (`modelo-autoridad.md` §7) con proponer,
aceptar y reemplazar ADR, excepciones y promoción del estándar. Son **dominios
disjuntos**: operaciones de Git frente a operaciones de gobernanza. No colisionan
y no hay nada que reconciliar.

El riesgo real es el inverso y se atiende en §4: si Skevi delegara "la matriz de
operaciones protegidas" sin más, las operaciones de Git quedarían sin hogar,
porque la matriz de Praxis Dev no las cubre.

## 4. Frontera propuesta

**Skevi conserva** el diseño de sistemas y de código (§2 y §3), las prácticas de
Git y GitHub en lo que no toca autoridad, el pipeline F0→F3 con su guía, la capa
de orquestación acoplada a herramientas y la historia.

**Skevi delega en `praxis/project-governance`** la precedencia de autoridad, la
matriz de **operaciones de gobernanza** —ADR, excepciones, promoción—, la
revisión proporcional y la conformidad con sus perfiles y gates.

**Skevi retiene explícitamente §4.3**, las operaciones de Git con autoridad
separada. La matriz de Praxis Dev no las cubre, y delegarlas en bloque las
dejaría sin ninguna protección normativa.

**Skevi bloquea, no retira, P0-01, A-1 y A-8.** Quedan `deferred` con una
condición nombrada: se retiran el día que Praxis Dev promueva una versión
estable que las contenga. Retirarlas hoy dejaría a Skevi sin modelo de autoridad
ni criterio de revisión independiente si Praxis Dev cambia de posición, se
estanca o no promueve nunca — y sin iniciativa en el backlog para reconstruirlos.

### 4.1 La duplicación de principios es una excepción declarada, con caducidad

Cinco de los siete principios de Skevi tienen equivalente en Praxis Dev, y esta
frontera los deja **vivos en los dos sitios**. Eso incumple el principio 3.3 de
Praxis Dev —una afirmación normativa tiene una sola fuente— y conviene decirlo
en vez de disimularlo.

Se acepta como excepción temporal por una razón concreta: el hogar canónico
candidato es un borrador no promovido, y apuntar hoy a él dejaría a Skevi
apoyado en algo que su propio §2 prohíbe presentar como conformidad estable. La
excepción caduca con la misma condición que el punto anterior: al promoverse una
versión estable, los cinco principios compartidos pasan a ser referencias y
dejan de tener texto propio en Skevi.

Mientras tanto, la capa de principios de Skevi **no crece**: un principio nuevo
que sea de gobernanza se propone a Praxis Dev, no se añade aquí.

## 5. Lo que impide formalizarlo hoy

Praxis Dev está en `0.1.0-draft.1`, *"borrador no promovido"*, y su propio §2
dice que un proyecto conforme **debe declarar una versión estable**, y que una
versión `draft` puede usarse para pilotos pero **no debe presentarse como
conformidad estable**.

Es decir: **Skevi no puede declarar conformidad todavía**, y hacerlo sería
incumplir la regla del estándar al que quiere adherirse. Lo que sí puede hacer
hoy es dejar de duplicar y registrar la dependencia como pendiente.

## 6. Secuencia propuesta

1. Registrar la frontera de §4 en un ADR de Skevi, sin declarar conformidad, y
   con la excepción de §4.1 y su condición de caducidad explícitas.
2. Congelar la capa de principios de Skevi: no crece; los nuevos van a Praxis.
3. Resolver los dos conflictos de §3, que requieren decisión humana porque
   ninguno es un error de redacción: son posiciones distintas.
4. Marcar P0-01, A-1 y A-8 como `deferred` bloqueadas por la promoción estable
   de Praxis Dev, citando dónde vive hoy cada una.
5. Cuando Praxis Dev promueva una versión estable, declarar conformidad con un
   perfil, siguiendo su §2.
6. Proponer a Praxis Dev que su tabla de límites incluya a Skevi, porque hoy
   describe el ecosistema sin él.

## 7. No objetivos

- No fusionar los dos proyectos: Praxis Dev 3.2 dice "componer antes que
  fusionar", y esa frontera es sana.
- No declarar conformidad con un borrador.
- No modificar el estándar de Skevi por esta propuesta: primero la decisión.
- No suponer que Praxis Dev es correcto por existir antes; sus tres conflictos
  con Skevi pueden resolverse en cualquiera de las dos direcciones.

## 8. Procedencia

Lectura directa de `praxis-dev` en `docs/estandar.md`, `fundamentos.md`,
`modelo-autoridad.md`, `conformidad.md` y `contrato-cli.md`, y de `epistates` en
su `README.md` y `docs/architecture/`, el 2026-08-17. Ninguno de los dos
repositorios menciona a Skevi; comprobado con `grep -rli skevi`.
