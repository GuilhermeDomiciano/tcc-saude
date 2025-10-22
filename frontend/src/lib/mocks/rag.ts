import type { RAGResumo, RAGFinanceiroItem, RAGProducaoItem, RAGMetaItem } from '../types'

export const mockRagResumo: RAGResumo = {
  periodos: ['2024'],
  itens: [
    {
      territorio_id: 1,
      territorio_nome: 'Municipio A',
      periodo: '2024',
      dotacao_atualizada: 5_000_000,
      receita_realizada: 4_300_000,
      empenhado: 3_800_000,
      liquidado: 3_500_000,
      pago: 3_300_000,
      execucao_percentual: 66,
      producao_total: 28_000,
      metas_cumpridas: 2,
      metas_total: 3,
    },
    {
      territorio_id: 2,
      territorio_nome: 'Municipio B',
      periodo: '2024',
      dotacao_atualizada: 3_200_000,
      receita_realizada: 2_950_000,
      empenhado: 2_600_000,
      liquidado: 2_400_000,
      pago: 2_350_000,
      execucao_percentual: 73,
      producao_total: 21_000,
      metas_cumpridas: 1,
      metas_total: 2,
    },
  ],
}

export const mockRagFinanceiro: RAGFinanceiroItem[] = mockRagResumo.itens.map((item) => ({
  territorio_id: item.territorio_id,
  territorio_nome: item.territorio_nome,
  periodo: item.periodo,
  dotacao_atualizada: item.dotacao_atualizada,
  receita_realizada: item.receita_realizada,
  empenhado: item.empenhado,
  liquidado: item.liquidado,
  pago: item.pago,
}))

export const mockRagProducao: RAGProducaoItem[] = [
  { territorio_id: 1, territorio_nome: 'Municipio A', periodo: '2024', tipo: 'Consultas ESF', quantidade: 18_500 },
  { territorio_id: 1, territorio_nome: 'Municipio A', periodo: '2024', tipo: 'Visitas domiciliares', quantidade: 9_400 },
  { territorio_id: 2, territorio_nome: 'Municipio B', periodo: '2024', tipo: 'Consultas ESF', quantidade: 11_200 },
  { territorio_id: 2, territorio_nome: 'Municipio B', periodo: '2024', tipo: 'Procedimentos odontologicos', quantidade: 4_300 },
]

export const mockRagMetas: RAGMetaItem[] = [
  { territorio_id: 1, territorio_nome: 'Municipio A', periodo: '2024', indicador: 'cobertura_aps', meta_planejada: 85, meta_executada: 81.2, cumprida: false },
  { territorio_id: 1, territorio_nome: 'Municipio A', periodo: '2024', indicador: 'visitas_domiciliares', meta_planejada: 9_000, meta_executada: 9_400, cumprida: true },
  { territorio_id: 2, territorio_nome: 'Municipio B', periodo: '2024', indicador: 'cobertura_aps', meta_planejada: 78, meta_executada: 74.5, cumprida: false },
  { territorio_id: 2, territorio_nome: 'Municipio B', periodo: '2024', indicador: 'consultas_esf', meta_planejada: 11_000, meta_executada: 11_200, cumprida: true },
]
