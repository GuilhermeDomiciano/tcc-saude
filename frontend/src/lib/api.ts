import axios from 'axios'

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
} as const

export type ListParams = {
  limit?: number
  offset?: number
  [key: string]: any
}

export const buildParams = (p?: ListParams) => ({ ...p })

export const isAxiosError = (err: unknown): err is import('axios').AxiosError => {
  return !!(err && typeof err === 'object' && (err as any).isAxiosError)
}

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
