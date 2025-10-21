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

