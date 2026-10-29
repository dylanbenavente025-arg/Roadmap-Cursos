export default function CursoCard({ curso }) {
  const insignias = [
    curso.extiende_certificado && 'Certificado',
    curso.requiere_examen && 'Examen',
    curso.tiene_cuestionarios && 'Cuestionarios',
    curso.aval_organizacion && `Avalado por ${curso.aval_organizacion}`,
  ].filter(Boolean)

  return (
    <article className="card">
      <h2 className="card__titulo">
        <a href={curso.url} target="_blank" rel="noopener noreferrer">
          {curso.titulo}
        </a>
      </h2>
      <span className="chip">{curso.categoria.nombre}</span>
      <p className="card__meta">
        {curso.docentes} · versión {curso.version} · {curso.anio_edicion}
      </p>
      {insignias.length > 0 && (
        <ul className="insignias">
          {insignias.map((texto) => (
            <li key={texto}>{texto}</li>
          ))}
        </ul>
      )}
      <p className="card__meta">
        {curso.lo_tomo_aportante
          ? 'Quien lo aportó lo tomó'
          : 'Quien lo aportó no lo tomó'}
      </p>
    </article>
  )
}