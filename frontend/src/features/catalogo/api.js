// Cliente del catálogo (BackendSchema §3.2).
export async function obtenerCursos({ page = 1, pageSize = 20 } = {}) {
  const params = new URLSearchParams({ page, page_size: pageSize })
  const respuesta = await fetch(`/api/v1/cursos?${params}`)
  if (!respuesta.ok) {
    throw new Error(`El servidor respondió ${respuesta.status}`)
  }
  return respuesta.json()
}