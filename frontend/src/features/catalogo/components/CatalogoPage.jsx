import { useCursos } from '../hooks/useCursos.js'
import CursoCard from './CursoCard.jsx'

export default function CatalogoPage() {
  const { estado, cursos, total, refetch } = useCursos()

  return (
    <section aria-labelledby="titulo-catalogo">
      <h1 id="titulo-catalogo" className="titulo-pantalla">
        Catálogo comunitario
      </h1>

      {estado === 'cargando' && (
        <p className="estado" role="status">
          Cargando cursos…
        </p>
      )}

      {estado === 'error' && (
        <div className="estado estado--error" role="alert">
          <p>No pudimos cargar el catálogo.</p>
          <button type="button" className="boton" onClick={refetch}>
            Reintentar
          </button>
        </div>
      )}

      {estado === 'vacio' && (
        <p className="estado">
          Todavía no hay cursos publicados. ¡Aportá el primero!
        </p>
      )}

      {estado === 'ok' && (
        <>
          <p className="card__meta">
            Mostrando {cursos.length} de {total} cursos
          </p>
          <div className="catalogo-grid">
            {cursos.map((curso) => (
              <CursoCard key={curso.id} curso={curso} />
            ))}
          </div>
        </>
      )}
    </section>
  )
}