# PRD — Product Requirements Document — AprovechaElBug

> **Qué es:** el QUÉ y el POR QUÉ de AprovechaElBug: para quién se construye, qué problema
> resuelve, qué hace y qué no hace. No habla de tecnología (eso es el [TRD](TRD.md)).
> **Contexto:** nace de la [SPEC](SPEC.md); las decisiones sobre sus vacíos están en SPEC §8.

## 1. Resumen ejecutivo

AprovechaElBug es una webapp donde una comunidad de estudiantes construye en conjunto un
catálogo de cursos gratuitos de cualquier plataforma. Cualquier usuario registrado puede
aportar un curso con su enlace y sus datos (categoría, versión, docentes, si tiene examen,
si entrega certificado, si lo avala una organización) y declarar si lo tomó. Un moderador
valida el aporte; una vez publicado, entra al catálogo comunitario. Desde allí, cada
usuario arma su roadmap personal de aprendizaje, con orden y seguimiento de avance.

## 2. Objetivos y métricas de éxito

| Objetivo | Cómo sabemos que lo logramos |
|----------|------------------------------|
| Que el catálogo reúna cursos validados de múltiples plataformas | Al menos 3 plataformas distintas representadas; la mayoría de los aportes recibe decisión (aprobado o rechazado) |
| Que la información del catálogo sea confiable | Todo curso publicado pasó por validación; cada curso indica si quien lo aportó lo tomó |
| Que el roadmap sirva para planificar el aprendizaje | Los usuarios incluyen cursos y marcan su avance; la proporción de ítems "en curso" o "completado" crece con el uso |
| Que aportar sea rápido | Un aporte completo se envía en un solo formulario, sin pasos intermedios |

## 3. Personas

### Persona 1 — Lucía, estudiante autodidacta

- **Contexto:** estudia una carrera de sistemas y complementa con cursos online. Entra desde el celular, entre clases.
- **Motivaciones:** aprender temas que la facultad no cubre, sin gastar plata, y llegar a un objetivo concreto (por ejemplo, empezar a trabajar con datos).
- **Frustraciones hoy:** pierde horas comparando plataformas, no sabe si un curso gratuito sigue vigente ni si da certificado, y su lista de pendientes vive en marcadores sueltos.
- **Historias tipo:**
  - "Quiero ver qué cursos gratuitos de datos hay y cuáles dan certificado."
  - "Quiero armar el orden en que voy a hacerlos y marcar cuáles ya terminé."

### Persona 2 — Martín, profesional en reconversión

- **Contexto:** trabaja en otra área y estudia de noche para cambiar de rubro. Usa el sitio desde la computadora.
- **Motivaciones:** aprovechar lo que ya descubrió, ayudar a otros y que su recorrido no se pierda.
- **Frustraciones hoy:** cuando encuentra un buen curso lo comparte por chat y se pierde; nadie confirma que el curso valga la pena.
- **Historias tipo:**
  - "Quiero aportar el curso que terminé y decir que lo hice yo."
  - "Quiero saber si mi aporte fue aprobado y, si no, por qué."

### Persona 3 — Valeria, moderadora de la comunidad

- **Contexto:** voluntaria con experiencia en formación online; revisa aportes un rato por día.
- **Motivaciones:** mantener un catálogo limpio, sin cursos duplicados, caídos o de pago encubierto.
- **Frustraciones hoy:** en foros y listas informales no hay forma ordenada de revisar ni de dejar constancia del motivo de un rechazo.
- **Historias tipo:**
  - "Quiero ver los aportes pendientes de a pocos, sin abrumarme."
  - "Quiero rechazar un aporte dejando el motivo por escrito."


## 4. User stories

> 10 historias: 6 P0 (el MVP no funciona sin ellas) y 4 P1.

| ID | Prioridad | Historia | Criterios de aceptación |
|----|-----------|----------|-------------------------|
| US-001 | P0 | Como visitante, quiero ver el catálogo comunitario paginado, para descubrir cursos sin registrarme | - [ ] Dado que visito `/catalogo`, veo la primera página (20 cursos), solo publicados<br>- [ ] Dado que hay más de 20 cursos, aparece el paginador y puedo cambiar de página<br>- [ ] Dado que no hay cursos publicados, veo un estado vacío con invitación a aportar<br>- [ ] Dado que abro un curso, veo su detalle completo y el enlace externo |
| US-002 | P0 | Como visitante, quiero registrarme con email y contraseña, para tener mi propia cuenta | - [ ] Dado un email nuevo y una contraseña de al menos 8 caracteres, la cuenta se crea y puedo iniciar sesión<br>- [ ] Dado un email ya registrado, veo un error claro y no se crea otra cuenta<br>- [ ] Dados datos inválidos, veo el error junto a cada campo y no pierdo lo escrito<br>- [ ] La contraseña nunca se guarda ni se muestra en claro (BR-010) |
| US-003 | P0 | Como usuario registrado, quiero iniciar y cerrar sesión, para acceder a mis funciones de forma segura | - [ ] Dadas credenciales válidas, entro y veo mi nombre en el header<br>- [ ] Dadas credenciales inválidas, veo un mensaje genérico que no indica cuál dato falló<br>- [ ] Dado que fallo 5 veces en 15 minutos con el mismo email e IP, quedo bloqueado temporalmente y veo cuánto esperar (BR-009)<br>- [ ] Dado que cierro sesión, no puedo entrar a rutas protegidas sin volver a iniciarla<br>- [ ] Dado que entro a una ruta protegida sin sesión, voy al login y luego regreso a esa ruta |
| US-004 | P0 | Como usuario, quiero aportar un curso gratuito con sus datos, para enriquecer el catálogo | - [ ] Dado el formulario completo y válido, el aporte se crea "en revisión" y veo la confirmación<br>- [ ] Dado un enlace que ya existe en el sistema, veo un error de duplicado (BR-004)<br>- [ ] Dado que no declaro si tomé el curso, no puedo enviar (BR-002)<br>- [ ] Dado un campo obligatorio vacío o un enlace inválido, veo el error y no pierdo lo escrito<br>- [ ] Mientras está en revisión, el curso no aparece en el catálogo (BR-001) |
| US-005 | P0 | Como moderador, quiero revisar los aportes pendientes y aprobarlos o rechazarlos, para mantener la calidad del catálogo | - [ ] Dado que soy moderador, veo la lista paginada de aportes en revisión<br>- [ ] Dado que apruebo un aporte, pasa a publicado y aparece en el catálogo<br>- [ ] Dado que rechazo sin escribir motivo, el sistema no me deja (BR-005)<br>- [ ] Dado que rechazo con motivo, el aporte queda rechazado y no aparece en el catálogo<br>- [ ] Dado que no soy moderador, no puedo acceder al panel de validación |
| US-006 | P0 | Como usuario, quiero incluir un curso del catálogo en mi roadmap y verlo allí, para armar mi plan de aprendizaje | - [ ] Dado que estoy logueado y veo un curso publicado, puedo incluirlo en mi roadmap (BR-006)<br>- [ ] Dado que ya lo incluí, no puedo incluirlo otra vez (BR-007)<br>- [ ] Dado que abro "Mi roadmap", veo mis cursos incluidos, paginados<br>- [ ] Dado que no incluí nada, veo un estado vacío con acceso al catálogo<br>- [ ] Dado otro usuario, no puede ver ni modificar mi roadmap (BR-003) |
| US-007 | P1 | Como visitante o usuario, quiero buscar por texto y filtrar por categoría, para encontrar rápido lo que me interesa | - [ ] Dado un texto, veo solo cursos publicados cuyo título o tema lo contienen<br>- [ ] Dada una categoría, veo solo cursos de esa categoría<br>- [ ] Dados texto y categoría juntos, se aplican ambos y el paginador refleja el total filtrado<br>- [ ] Dado que no hay resultados, veo un estado vacío con opción de limpiar filtros |
| US-008 | P1 | Como usuario, quiero recuperar mi contraseña si la olvido, para volver a entrar a mi cuenta | - [ ] Dado que ingreso mi email, veo siempre el mismo mensaje, exista o no la cuenta (BR-008)<br>- [ ] Dado un token válido, defino una nueva contraseña y puedo iniciar sesión con ella<br>- [ ] Dado un token vencido o ya usado, veo un error y puedo pedir otro<br>- [ ] Dado que uso un token, deja de servir (un solo uso) |
| US-009 | P1 | Como usuario, quiero ver el estado de mis aportes, para saber si fueron aprobados o rechazados | - [ ] Veo mis aportes paginados con su estado (en revisión, publicado, rechazado)<br>- [ ] Dado un aporte rechazado, veo el motivo<br>- [ ] Solo veo mis propios aportes |
| US-010 | P1 | Como usuario, quiero ordenar mi roadmap, marcar mi avance y quitar cursos, para mantener mi plan actualizado | - [ ] Puedo cambiar el estado de un curso (pendiente, en curso, completado)<br>- [ ] Puedo cambiar el orden de mis cursos<br>- [ ] Puedo quitar un curso con confirmación previa<br>- [ ] Los cambios se mantienen al recargar la página |

## 5. Requisitos funcionales

| ID | Requisito | Historia relacionada |
|----|-----------|----------------------|
| RF-001 | El sistema permite registrar usuarios con nombre, email y contraseña | US-002 |
| RF-002 | El sistema autentica con email y contraseña y entrega una sesión | US-003 |
| RF-003 | El sistema permite cerrar sesión | US-003 |
| RF-004 | El sistema limita los intentos fallidos de login (BR-009) | US-003 |
| RF-005 | El sistema permite solicitar la recuperación de contraseña por email | US-008 |
| RF-006 | El sistema permite definir una nueva contraseña con un token válido | US-008 |
| RF-007 | El sistema lista el catálogo paginado, solo con cursos publicados | US-001 |
| RF-008 | El sistema muestra el detalle de un curso publicado | US-001 |
| RF-009 | El sistema permite buscar por texto y filtrar por categoría | US-007 |
| RF-010 | El sistema expone la lista cerrada de categorías | US-004, US-007 |
| RF-011 | El sistema permite aportar un curso con todos los datos y la declaración de si se tomó | US-004 |
| RF-012 | El sistema rechaza aportes cuyo enlace ya existe (BR-004) | US-004 |
| RF-013 | El sistema lista los aportes propios con estado y motivo de rechazo | US-009 |
| RF-014 | El sistema lista, para el moderador, los aportes en revisión (paginado) | US-005 |
| RF-015 | El sistema permite al moderador aprobar o rechazar un aporte (BR-005) | US-005 |
| RF-016 | El sistema permite incluir un curso publicado en el roadmap propio (BR-006, BR-007) | US-006 |
| RF-017 | El sistema lista el roadmap propio, paginado | US-006 |
| RF-018 | El sistema permite cambiar el orden y el estado de avance de un ítem del roadmap | US-010 |
| RF-019 | El sistema permite quitar un ítem del roadmap | US-010 |
| RF-020 | El sistema restringe rutas y acciones según sesión y rol | US-003, US-005 |