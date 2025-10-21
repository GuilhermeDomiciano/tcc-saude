import { useMemo, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import DataTable from '../components/DataTable'
import ProvenanceBadges from '../components/Provenance'
import { listFontes, deleteFonte } from '../lib/api'
import type { DimFonteRecurso } from '../lib/types'

export default function Fontes() {
  const [codigo, setCodigo] = useState<string>('')
  const [limit, setLimit] = useState<number>(10)
  const [offset, setOffset] = useState<number>(0)
  // removed legacy delete-by-id control in favor of row actions
  const queryClient = useQueryClient()
  const delMut = useMutation({
    mutationFn: (id: number) => deleteFonte(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['fontes'] }),
  })

  const { data, isLoading, error } = useQuery({
    queryKey: ['fontes', { codigo, limit, offset }],
    queryFn: () => listFontes({ codigo: codigo || undefined, limit, offset }),
  })

  const columns = useMemo<ColumnDef<DimFonteRecurso>[]>(
    () => [
      { header: 'ID', accessorKey: 'id' },
      { header: 'Código', accessorKey: 'codigo' },
      { header: 'Descrição', accessorKey: 'descricao' },
      {
        header: 'Ações',
        cell: ({ row }) => (
          <button className="no-print rounded-md border px-2 py-0.5 text-xs" onClick={() => { if (confirm('Excluir este registro?')) delMut.mutate(row.original.id) }}>
            Excluir
          </button>
        ),
      },
      {
        header: 'Proveniência',
        cell: ({ row }) => (
          <ProvenanceBadges
            fonte={row.original.fonte}
            periodo={row.original.periodo}
            versao={row.original.versao}
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
        <h2>Dimensão: Fontes de Recurso</h2>
      </div>

      <div className="no-print flex flex-wrap items-end gap-3">
        <label className="text-sm">
          <span className="block text-muted-foreground">Código</span>
          <input
            className="w-40 rounded-md border bg-background px-2 py-1"
            value={codigo}
            onChange={(e) => {
              setCodigo(e.target.value)
              setOffset(0)
            }}
            placeholder="001"
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

      <DataTable<DimFonteRecurso>
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


