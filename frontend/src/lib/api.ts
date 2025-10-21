import axios, { isAxiosError, type AxiosError } from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE as string,
  withCredentials: false,
})

api.interceptors.request.use((config) => {
  const apiKey = typeof localStorage !== 'undefined' ? localStorage.getItem('apiKey') : null
  if (apiKey) {
    config.headers = config.headers ?? {}
    config.headers['X-API-Key'] = apiKey
  }
  return config
})

export const routes = {
  territorios: '/dw/territorios',
  tempo: '/dw/tempo',
  popFaixa: '/dw/pop-faixa',
  unidades: '/dw/unidades',
  equipes: '/dw/equipes',
  fontes: '/dw/fontes',
  fatosCobertura: '/dw/fatos/cobertura',
  rdqaExportPdf: '/rdqa/export/pdf',
} as const

export type ListParams = {
  limit?: number
  offset?: number
  [key: string]: unknown
}

export const buildParams = (p?: ListParams) => ({ ...p })

export const isAxiosErrorNarrow = (err: unknown): err is AxiosError<unknown> => isAxiosError(err)

export async function getList<T>(path: string, params?: ListParams): Promise<T[]> {
  const res = await api.get<T[]>(path, { params: buildParams(params) })
  return res.data
}

export * from './types'
import type {
  DimTempo,
  DimTerritorio,
  DimPopFaixaEtaria,
  DimUnidade,
  DimEquipe,
  DimFonteRecurso,
} from './types'

export const listTempo = (params?: ListParams) => getList<DimTempo>(routes.tempo, params)
export const listTerritorios = (params?: ListParams) => getList<DimTerritorio>(routes.territorios, params)
export const listPopFaixa = (params?: ListParams) => getList<DimPopFaixaEtaria>(routes.popFaixa, params)
export const listUnidades = (params?: ListParams) => getList<DimUnidade>(routes.unidades, params)
export const listEquipes = (params?: ListParams) => getList<DimEquipe>(routes.equipes, params)
export const listFontes = (params?: ListParams) => getList<DimFonteRecurso>(routes.fontes, params)

export type ExportPdfPayload = {
  html?: string
  url?: string
  format?: string
  margin_mm?: number
}

export async function exportRDQAPdf(payload: ExportPdfPayload): Promise<{ blob: Blob; execId?: string; hash?: string }> {
  const res = await api.post(routes.rdqaExportPdf, payload, { responseType: 'blob' })
  const execId = res.headers?.['x-exec-id'] as string | undefined
  const hash = res.headers?.['x-hash'] as string | undefined
  const blob: Blob = res.data
  return { blob, execId, hash }
}

import type { DimTempoCreate, DimTempoUpdate, DimTerritorioCreate, DimTerritorioUpdate } from './types'

export async function createTempo(body: DimTempoCreate) {
  const res = await api.post(routes.tempo, body)
  return res.data
}
export async function updateTempo(id: number, body: DimTempoUpdate) {
  const res = await api.put(`${routes.tempo}/${id}`, body)
  return res.data
}

export async function createTerritorio(body: DimTerritorioCreate) {
  const res = await api.post(routes.territorios, body)
  return res.data
}
export async function updateTerritorio(id: number, body: DimTerritorioUpdate) {
  const res = await api.put(`${routes.territorios}/${id}`, body)
  return res.data
}
