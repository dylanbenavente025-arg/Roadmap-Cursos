// Tests del hook useCursos (ticket C27-T6).
// La API se reemplaza por una función simulada: el test controla qué responde
// y comprueba con qué parámetros la llamó el hook.
import { act, renderHook, waitFor } from '@testing-library/react'
import { beforeEach, expect, test, vi } from 'vitest'
import { obtenerCursos } from '../api.js'
import { useCursos } from './useCursos.js'

vi.mock('../api.js', () => ({ obtenerCursos: vi.fn() }))

const CURSO = { id: 1, titulo: 'Python desde cero' }

function pagina(items, total = items.length) {
  return { items, total, page: 1, page_size: 20 }
}

// Renderiza el hook y espera a que termine la primera carga
async function hookCargado() {
  const hook = renderHook(() => useCursos())
  await waitFor(() => expect(hook.result.current.estado).not.toBe('cargando'))
  return hook
}

beforeEach(() => {
  vi.mocked(obtenerCursos).mockReset()
  vi.mocked(obtenerCursos).mockResolvedValue(pagina([CURSO], 1))
})

test('useCursos_carga_inicial_empieza_cargando', () => {
  // Arrange: la API responde con un curso (beforeEach)
  // Act
  const { result } = renderHook(() => useCursos())
  // Assert
  expect(result.current.estado).toBe('cargando')
})

test('useCursos_carga_inicial_termina_ok_con_los_datos', async () => {
  // Arrange: la API responde con un curso (beforeEach)
  // Act
  const { result } = renderHook(() => useCursos())
  // Assert
  await waitFor(() => expect(result.current.estado).toBe('ok'))
  expect(result.current.cursos).toEqual([CURSO])
})

test('useCursos_carga_inicial_pide_la_pagina_1', async () => {
  // Arrange: la API responde con un curso (beforeEach)
  // Act
  await hookCargado()
  // Assert
  expect(obtenerCursos).toHaveBeenCalledWith({ page: 1, pageSize: 20, q: '', categoria: null })
})

test('useCursos_error_de_red_estado_error_y_lista_vacia', async () => {
  // Arrange
  vi.mocked(obtenerCursos).mockRejectedValue(new TypeError('Failed to fetch'))
  // Act
  const { result } = renderHook(() => useCursos())
  // Assert
  await waitFor(() => expect(result.current.estado).toBe('error'))
  expect(result.current.cursos).toEqual([])
})

test('useCursos_respuesta_sin_cursos_estado_vacio', async () => {
  // Arrange
  vi.mocked(obtenerCursos).mockResolvedValue(pagina([], 0))
  // Act
  const { result } = renderHook(() => useCursos())
  // Assert
  await waitFor(() => expect(result.current.estado).toBe('vacio'))
})

test('useCursos_setPage_recarga_con_esa_pagina', async () => {
  // Arrange
  const { result } = await hookCargado()
  // Act
  act(() => result.current.setPage(3))
  // Assert
  await waitFor(() => expect(result.current.estado).toBe('ok'))
  expect(obtenerCursos).toHaveBeenLastCalledWith(expect.objectContaining({ page: 3 }))
})

test('useCursos_setPage_a_la_misma_pagina_no_recarga', async () => {
  // Arrange
  const { result } = await hookCargado()
  // Act
  act(() => result.current.setPage(1))
  // Assert
  expect(obtenerCursos).toHaveBeenCalledTimes(1)
})

test('useCursos_cambiar_filtro_vuelve_a_la_pagina_1', async () => {
  // Arrange: el usuario está en la página 3
  const { result } = await hookCargado()
  act(() => result.current.setPage(3))
  await waitFor(() => expect(result.current.estado).toBe('ok'))
  // Act
  act(() => result.current.setFiltros({ q: 'python' }))
  // Assert
  await waitFor(() => expect(result.current.estado).toBe('ok'))
  expect(obtenerCursos).toHaveBeenLastCalledWith(
    expect.objectContaining({ page: 1, q: 'python' }),
  )
})

test('useCursos_refetch_recarga_con_los_parametros_actuales', async () => {
  // Arrange: página 2 filtrando por "git"
  const { result } = await hookCargado()
  act(() => result.current.setFiltros({ q: 'git' }))
  await waitFor(() => expect(result.current.estado).toBe('ok'))
  act(() => result.current.setPage(2))
  await waitFor(() => expect(result.current.estado).toBe('ok'))
  const llamadasAntes = vi.mocked(obtenerCursos).mock.calls.length
  // Act
  act(() => result.current.refetch())
  // Assert
  await waitFor(() => expect(obtenerCursos).toHaveBeenCalledTimes(llamadasAntes + 1))
  expect(obtenerCursos).toHaveBeenLastCalledWith(
    expect.objectContaining({ page: 2, q: 'git' }),
  )
})

test('useCursos_refetch_despues_de_un_error_recupera_los_datos', async () => {
  // Arrange: la primera carga falla, la segunda funciona
  vi.mocked(obtenerCursos)
    .mockRejectedValueOnce(new TypeError('Failed to fetch'))
    .mockResolvedValueOnce(pagina([CURSO], 1))
  const { result } = await hookCargado()
  // Act
  act(() => result.current.refetch())
  // Assert
  await waitFor(() => expect(result.current.estado).toBe('ok'))
})

test('useCursos_total_paginas_redondea_hacia_arriba', async () => {
  // Arrange: 45 cursos en páginas de 20 → 3 páginas
  vi.mocked(obtenerCursos).mockResolvedValue(pagina([CURSO], 45))
  // Act
  const { result } = await hookCargado()
  // Assert
  expect(result.current.totalPaginas).toBe(3)
})