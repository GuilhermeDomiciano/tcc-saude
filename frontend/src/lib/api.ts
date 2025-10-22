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
  rdqaConsistencia: '/rdqa/consistencia',
  rdqaCobertura: '/rdqa/cobertura',
  rdqaDiff: '/rdqa/diff',
  rdqaExportPackage: '/rdqa/export/pacote',
  ragResumo: '/rag/resumo',
  ragFinanceiro: '/rag/financeiro',
  ragProducao: '/rag/producao',
  ragMetas: '/rag/metas',
  ragExportPdf: '/rag/export/pdf',
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
  RAGResumo,
  RAGFinanceiroItem,
  RAGProducaoItem,
  RAGMetaItem,
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
  try {
    const res = await api.post(routes.rdqaExportPdf, payload, { responseType: 'blob' })
    const execId = res.headers?.['x-exec-id'] as string | undefined
    const hash = res.headers?.['x-hash'] as string | undefined
    const blob: Blob = res.data
    return { blob, execId, hash }
  } catch (err) {
    if (isAxiosErrorNarrow(err) && err.response?.data instanceof Blob) {
      try {
        const text = await err.response.data.text()
        throw new Error(`Exportação PDF falhou (${err.response.status}): ${text}`)
      } catch {
        throw err
      }
    }
    throw err
  }
}

export async function getRDQAConsistencia(periodo?: string): Promise<Array<{ indicador: string; periodo?: string; mape?: number; pares: number }>> {
  const res = await api.get(routes.rdqaConsistencia, { params: { periodo } })
  return res.data
}

export async function getRDQAConsistenciaDetalhes(indicador: string, periodo?: string): Promise<Array<{ indicador: string; chave: string; periodo: string; ref: number; calc?: number; erro_abs?: number; erro_pct?: number }>> {
  const res = await api.get(`${routes.rdqaConsistencia}/${encodeURIComponent(indicador)}/detalhes`, { params: { periodo } })
  return res.data
}

export async function getRDQACobertura(periodo?: string): Promise<{ percent: number; total: number; gerados: number; faltantes: Array<{ quadro: string; periodo: string; motivo: string }> }> {
  const res = await api.get(routes.rdqaCobertura, { params: { periodo } })
  return res.data
}

export async function getRDQADiff(periodoAtual: string, periodoAnterior: string, indicadores?: string): Promise<Array<{ indicador: string; chave: string; valor_atual?: number; valor_anterior?: number; delta?: number; tendencia: string }>> {
  const res = await api.get(routes.rdqaDiff, { params: { periodo_atual: periodoAtual, periodo_anterior: periodoAnterior, indicadores } })
  return res.data
}

export async function exportRDQAPackage(params?: { periodo?: string }): Promise<{ blob: Blob; execId?: string; hash?: string }> {
  const res = await api.post(routes.rdqaExportPackage, null, { params, responseType: 'blob' })
  const execId = res.headers?.['x-exec-id'] as string | undefined
  const hash = res.headers?.['x-hash'] as string | undefined
  return { blob: res.data as Blob, execId, hash }
}

export async function getRAGResumo(periodo?: string, territorioId?: number): Promise<RAGResumo> {
  const res = await api.get(routes.ragResumo, { params: { periodo, territorio_id: territorioId } })
  return res.data
}

export async function getRAGFinanceiro(periodo?: string, territorioId?: number): Promise<RAGFinanceiroItem[]> {
  const res = await api.get(routes.ragFinanceiro, { params: { periodo, territorio_id: territorioId } })
  return res.data
}

export async function getRAGProducao(periodo?: string, territorioId?: number): Promise<RAGProducaoItem[]> {
  const res = await api.get(routes.ragProducao, { params: { periodo, territorio_id: territorioId } })
  return res.data
}

export async function getRAGMetas(periodo?: string, territorioId?: number): Promise<RAGMetaItem[]> {
  const res = await api.get(routes.ragMetas, { params: { periodo, territorio_id: territorioId } })
  return res.data
}

export async function exportRAGPdf(payload: ExportPdfPayload): Promise<{ blob: Blob; execId?: string; hash?: string }> {
  try {
    const res = await api.post(routes.ragExportPdf, payload, { responseType: 'blob' })
    const execId = res.headers?.['x-exec-id'] as string | undefined
    const hash = res.headers?.['x-hash'] as string | undefined
    return { blob: res.data as Blob, execId, hash }
  } catch (err) {
    if (isAxiosErrorNarrow(err) && err.response?.data instanceof Blob) {
      try {
        const text = await err.response.data.text()
        throw new Error(`Falha ao exportar PDF (RAG) (${err.response.status}): ${text}`)
      } catch {
        throw err
      }
    }
    throw err
  }
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

export async function deleteTempo(id: number) {
  await api.delete(`${routes.tempo}/${id}`)
}
export async function deleteTerritorio(id: number) {
  await api.delete(`${routes.territorios}/${id}`)
}
export async function deleteUnidade(id: number) {
  await api.delete(`${routes.unidades}/${id}`)
}
export async function deleteEquipe(id: number) {
  await api.delete(`${routes.equipes}/${id}`)
}
export async function deleteFonte(id: number) {
  await api.delete(`${routes.fontes}/${id}`)
}
export async function deletePopFaixa(id: number) {
  await api.delete(`${routes.popFaixa}/${id}`)
}





