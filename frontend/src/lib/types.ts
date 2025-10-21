export type Proveniencia = {
  fonte?: string
  periodo?: string
  versao?: string
  hash?: string
  exec_id?: string
}

export interface DimTerritorioCreate {
  cod_ibge_municipio: string
  nome: string
  uf: string
  area_km2?: number | null
  pop_censo_2022?: number | null
  pop_estim_2024?: number | null
}
export type DimTerritorioUpdate = Partial<DimTerritorioCreate>
export interface DimTerritorioOut {
  id: number
  cod_ibge_municipio: string
  nome: string
  uf: string
  area_km2?: number | null
  pop_censo_2022?: number | null
  pop_estim_2024?: number | null
}
export type DimTerritorio = DimTerritorioOut & Proveniencia

export interface DimTempoCreate {
  data: string // YYYY-MM-DD
  ano: number
  mes: number
  trimestre: number
  quadrimestre: number
  mes_nome?: string | null
}
export type DimTempoUpdate = Partial<DimTempoCreate>
export interface DimTempoOut {
  id: number
  data: string
  ano: number
  mes: number
  trimestre: number
  quadrimestre: number
  mes_nome?: string | null
}
export type DimTempo = DimTempoOut & Proveniencia

export type Sexo = 'M' | 'F'
export interface DimPopFaixaEtariaCreate {
  territorio_id: number
  ano: number
  faixa_etaria: string
  sexo: Sexo
  populacao: number
}
export type DimPopFaixaEtariaUpdate = Partial<DimPopFaixaEtariaCreate>
export interface DimPopFaixaEtariaOut {
  id: number
  territorio_id: number
  ano: number
  faixa_etaria: string
  sexo: Sexo
  populacao: number
}
export type DimPopFaixaEtaria = DimPopFaixaEtariaOut & Proveniencia

export interface DimUnidadeCreate {
  cnes: string
  nome: string
  tipo_estabelecimento?: string | null
  bairro?: string | null
  territorio_id?: number | null
  gestao?: string | null
}
export type DimUnidadeUpdate = Partial<DimUnidadeCreate>
export interface DimUnidadeOut {
  id: number
  cnes: string
  nome: string
  tipo_estabelecimento?: string | null
  bairro?: string | null
  territorio_id?: number | null
  gestao?: string | null
}
export type DimUnidade = DimUnidadeOut & Proveniencia

export type EquipeTipo = 'ESF' | 'ESB' | 'ACS' | 'OUTROS'
export interface DimEquipeCreate {
  id_equipe: string
  tipo: EquipeTipo
  unidade_id?: number | null
  territorio_id?: number | null
  ativo?: boolean
}
export type DimEquipeUpdate = Partial<DimEquipeCreate>
export interface DimEquipeOut {
  id: number
  id_equipe: string
  tipo: EquipeTipo
  unidade_id?: number | null
  territorio_id?: number | null
  ativo: boolean
}
export type DimEquipe = DimEquipeOut & Proveniencia

export interface DimFonteRecursoCreate {
  codigo: string
  descricao: string
}
export type DimFonteRecursoUpdate = Partial<DimFonteRecursoCreate>
export interface DimFonteRecursoOut {
  id: number
  codigo: string
  descricao: string
}
export type DimFonteRecurso = DimFonteRecursoOut & Proveniencia

export type FatoCoberturaAPSOut = Record<string, unknown>
