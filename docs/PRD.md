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