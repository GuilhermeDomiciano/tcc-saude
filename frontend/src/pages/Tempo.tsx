import { useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import DataTable from '../components/DataTable'
import { listTempo } from '../lib/api'
import type { DimTempo } from '../lib/types'

export default function Tempo() {
  const [ano, setAno] = useState<string>('')
  const [mes, setMes] = useState<string>('')
  const [limit, setLimit] = useState<number>(10)
  const [offset, setOffset] = useState<number>(0)

  const { data, isLoading, error } = useQuery({
    queryKey: ['tempo', { ano, mes, limit, offset }],
    queryFn: () =>
      listTempo({
        ano: ano ? Number(ano) : undefined,
        mes: mes ? Number(mes) : undefined,
        limit,
        offset,
      }),
  })

  const columns = useMemo<ColumnDef<DimTempo>[]>(
    () => [
      { header: 'ID', accessorKey: 'id' },
      { header: 'Data', accessorKey: 'data' },
      { header: 'Ano', accessorKey: 'ano' },
      { header: 'Mês', accessorKey: 'mes' },
      { header: 'Trimestre', accessorKey: 'trimestre' },
      { header: 'Quadrimestre', accessorKey: 'quadrimestre' },
      { header: 'Mês (nome)', accessorKey: 'mes_nome' },
    ],
    [],
  )

  const items = data ?? []

  return (
    <section className="space-y-4">
      <div className="prose max-w-none dark:prose-invert">
        <h2>Dimensão: Tempo</h2>
      </div>

      <div className="no-print flex flex-wrap items-end gap-3">
        <label className="text-sm">
          <span className="block text-muted-foreground">Ano</span>
          <input
            type="number"
            className="w-28 rounded-md border bg-background px-2 py-1"
            value={ano}
            onChange={(e) => {
              setAno(e.target.value)
              setOffset(0)
            }}
            placeholder="2025"
          />
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">Mês</span>
          <input
            type="number"
            min={1}
            max={12}
            className="w-24 rounded-md border bg-background px-2 py-1"
            value={mes}
            onChange={(e) => {
              setMes(e.target.value)
              setOffset(0)
            }}
            placeholder="1..12"
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

      <DataTable<DimTempo>
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
