import { useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import DataTable from '../components/DataTable'
import ProvenanceBadges from '../components/Provenance'
import { listUnidades } from '../lib/api'
import type { DimUnidade } from '../lib/types'

export default function Unidades() {
  const [cnes, setCnes] = useState<string>('')
  const [territorio, setTerritorio] = useState<string>('')
  const [limit, setLimit] = useState<number>(10)
  const [offset, setOffset] = useState<number>(0)

  const { data, isLoading, error } = useQuery({
    queryKey: ['unidades', { cnes, territorio, limit, offset }],
    queryFn: () =>
      listUnidades({
        cnes: cnes || undefined,
        territorio_id: territorio ? Number(territorio) : undefined,
        limit,
        offset,
      }),
  })

  const columns = useMemo<ColumnDef<DimUnidade>[]>(
    () => [
      { header: 'ID', accessorKey: 'id' },
      { header: 'CNES', accessorKey: 'cnes' },
      { header: 'Nome', accessorKey: 'nome' },
      { header: 'Tipo', accessorKey: 'tipo_estabelecimento' },
      { header: 'Bairro', accessorKey: 'bairro' },
      { header: 'Território', accessorKey: 'territorio_id' },
      { header: 'Gestão', accessorKey: 'gestao' },
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
        <h2>Dimensão: Unidades</h2>
      </div>

      <div className="no-print flex flex-wrap items-end gap-3">
        <label className="text-sm">
          <span className="block text-muted-foreground">CNES</span>
          <input
            className="w-40 rounded-md border bg-background px-2 py-1"
            value={cnes}
            onChange={(e) => {
              setCnes(e.target.value)
              setOffset(0)
            }}
            placeholder="1234567"
          />
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">Território ID</span>
          <input
            type="number"
            className="w-32 rounded-md border bg-background px-2 py-1"
            value={territorio}
            onChange={(e) => {
              setTerritorio(e.target.value)
              setOffset(0)
            }}
            placeholder="1"
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

      <DataTable<DimUnidade>
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
