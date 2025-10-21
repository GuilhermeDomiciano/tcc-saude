import { useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import DataTable from '../components/DataTable'
import ProvenanceBadges from '../components/Provenance'
import { listTerritorios } from '../lib/api'
import type { DimTerritorio } from '../lib/types'

export default function Territorios() {
  const [uf, setUf] = useState<string>('')
  const [ibge, setIbge] = useState<string>('')
  const [limit, setLimit] = useState<number>(10)
  const [offset, setOffset] = useState<number>(0)

  const { data, isLoading, error } = useQuery({
    queryKey: ['territorios', { uf, ibge, limit, offset }],
    queryFn: () =>
      listTerritorios({
        uf: uf || undefined,
        cod_ibge_municipio: ibge || undefined,
        limit,
        offset,
      }),
  })

  const columns = useMemo<ColumnDef<DimTerritorio>[]>(
    () => [
      { header: 'ID', accessorKey: 'id' },
      { header: 'Município (IBGE)', accessorKey: 'cod_ibge_municipio' },
      { header: 'Nome', accessorKey: 'nome' },
      { header: 'UF', accessorKey: 'uf' },
      { header: 'Área km²', accessorKey: 'area_km2' },
      { header: 'Pop. Censo 2022', accessorKey: 'pop_censo_2022' },
      { header: 'Pop. Estim. 2024', accessorKey: 'pop_estim_2024' },
      {
        header: 'Proveniência',
        cell: ({ row }) => (
          <ProvenanceBadges
            fonte={(row.original as any).fonte}
            periodo={(row.original as any).periodo}
            versao={(row.original as any).versao}
          />
        ),
      },
    ],
    [],
  )

  const items = data ?? []

  return (
    <section className="space-y-4">
      <div className="prose max-w-none dark:prose-invert">
        <h2>Dimensão: Territórios</h2>
      </div>

      <div className="no-print flex flex-wrap items-end gap-3">
        <label className="text-sm">
          <span className="block text-muted-foreground">UF</span>
          <input
            className="w-20 uppercase rounded-md border bg-background px-2 py-1"
            maxLength={2}
            value={uf}
            onChange={(e) => {
              setUf(e.target.value.toUpperCase())
              setOffset(0)
            }}
            placeholder="RS"
          />
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">IBGE</span>
          <input
            className="w-32 rounded-md border bg-background px-2 py-1"
            value={ibge}
            onChange={(e) => {
              setIbge(e.target.value)
              setOffset(0)
            }}
            placeholder="4300000"
          />
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">Linhas por página</span>
          <select
            className="w-28 rounded-md border bg-background px-2 py-1"
            value={limit}
            onChange={(e) => {
              setLimit(Number(e.target.value))
              setOffset(0)
            }}
          >
            {[10, 20, 50].map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>
        </label>
      </div>

      <DataTable<DimTerritorio>
        data={items}
        columns={columns}
        loading={isLoading}
        error={(error as Error | undefined)?.message ?? null}
      />

      <div className="no-print flex items-center justify-between">
        <button
          className="rounded-md border px-3 py-1 text-sm disabled:opacity-50"
          disabled={offset === 0}
          onClick={() => setOffset((o) => Math.max(0, o - limit))}
        >
          ← Anterior
        </button>
        <button
          className="rounded-md border px-3 py-1 text-sm disabled:opacity-50"
          disabled={items.length < limit}
          onClick={() => setOffset((o) => o + limit)}
        >
          Próxima →
        </button>
      </div>
    </section>
  )
}
