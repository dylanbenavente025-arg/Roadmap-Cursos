import { useEffect, useState } from 'react'
import { obtenerCursos } from '../api.js'

// Estados: 'cargando' | 'ok' | 'vacio' | 'error' (APPFlow §3, pantalla Catálogo).
export function useCursos() {
  const [estado, setEstado] = useState('cargando')
  const [datos, setDatos] = useState(null)
  const [intento, setIntento] = useState(0)

  useEffect(() => {
    let cancelado = false
    obtenerCursos()
      .then((pagina) => {
        if (cancelado) return
        setDatos(pagina)
        setEstado(pagina.items.length === 0 ? 'vacio' : 'ok')
      })
      .catch(() => {
        if (!cancelado) setEstado('error')
      })
    return () => {
      cancelado = true
    }
  }, [intento])

  function reintentar() {
    setEstado('cargando')
    setIntento((n) => n + 1)
  }

  return { estado, datos, reintentar }
}