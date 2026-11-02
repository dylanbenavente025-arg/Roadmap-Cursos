import { useEffect, useState } from 'react'
import { obtenerCursos } from '../api.js'

const TAMANIO_PAGINA = 20
const FILTROS_INICIALES = { q: '', categoria: null }

// Estado del catálogo: página, filtros y datos (APPFlow §3, pantalla Catálogo).
// estado: 'cargando' | 'ok' | 'vacio' | 'error'
export function useCursos({ pageSize = TAMANIO_PAGINA } = {}) {
  const [page, setPageActual] = useState(1)
  const [filtros, setFiltrosActuales] = useState(FILTROS_INICIALES)
  const [intento, setIntento] = useState(0)
  const [estado, setEstado] = useState('cargando')
  const [cursos, setCursos] = useState([])
  const [total, setTotal] = useState(0)

  // Cada vez que cambia la página, los filtros o se pide reintentar, se vuelve a pedir
  useEffect(() => {
    let cancelado = false
    obtenerCursos({ page, pageSize, ...filtros })
      .then((pagina) => {
        if (cancelado) return
        setCursos(pagina.items)
        setTotal(pagina.total)
        setEstado(pagina.items.length === 0 ? 'vacio' : 'ok')
      })
      .catch(() => {
        if (cancelado) return
        setCursos([])
        setTotal(0)
        setEstado('error')
      })
    return () => {
      cancelado = true
    }
  }, [page, pageSize, filtros, intento])

  function setPage(nueva) {
    if (nueva === page) return
    setEstado('cargando')
    setPageActual(nueva)
  }

  // Un filtro nuevo cambia los resultados: se vuelve a la página 1
  function setFiltros(cambios) {
    setEstado('cargando')
    setFiltrosActuales((actuales) => ({ ...actuales, ...cambios }))
    setPageActual(1)
  }

  // Vuelve a pedir la misma página con los mismos filtros
  function refetch() {
    setEstado('cargando')
    setIntento((n) => n + 1)
  }

  const totalPaginas = Math.max(1, Math.ceil(total / pageSize))

  return { estado, cursos, total, page, totalPaginas, filtros, setPage, setFiltros, refetch }
}