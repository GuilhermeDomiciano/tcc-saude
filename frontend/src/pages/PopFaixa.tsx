import { useMemo, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import DataTable from '../components/DataTable'
import ProvenanceBadges from '../components/Provenance'
import { listPopFaixa, deletePopFaixa } from '../lib/api'
import type { DimPopFaixaEtaria } from '../lib/types'

export default function PopFaixa() {
  const [territorioId, setTerritorioId] = useState<string>('')
  const [ano, setAno] = useState<string>('')
  const [limit, setLimit] = useState<number>(10)
  const [offset, setOffset] = useState<number>(0)
  const [deleteId, setDeleteId] = useState<string>('')
  const queryClient = useQueryClient()
  const delMut = useMutation({
    mutationFn: (id: number) => deletePopFaixa(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['pop-faixa'] }),
  })

  const { data, isLoading, error } = useQuery({
    queryKey: ['pop-faixa', { territorioId, ano, limit, offset }],
    queryFn: () =>
      listPopFaixa({
        territorio_id: territorioId ? Number(territorioId) : undefined,
        ano: ano ? Number(ano) : undefined,
        limit,
        offset,
      }),
  })

  const columns = useMemo<ColumnDef<DimPopFaixaEtaria>[]>(
    () => [
      { header: 'ID', accessorKey: 'id' },
      { header: 'Território', accessorKey: 'territorio_id' },
      { header: 'Ano', accessorKey: 'ano' },
      { header: 'Faixa Etária', accessorKey: 'faixa_etaria' },
      { header: 'Sexo', accessorKey: 'sexo' },
      {
        header: 'Ações',
        cell: ({ row }) => (
          <button className="no-print rounded-md border px-2 py-0.5 text-xs" onClick={() => { if (confirm('Excluir este registro?')) delMut.mutate(row.original.id) }}>
            Excluir
          </button>
        ),
      },
      { header: 'População', accessorKey: 'populacao' },
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
        <h2>Dimensão: População por Faixa Etária</h2>
      </div>

      <div className="no-print flex flex-wrap items-end gap-3">
        <label className="text-sm">
          <span className="block text-muted-foreground">Território ID</span>
          <input
            type="number"
            className="w-32 rounded-md border bg-background px-2 py-1"
            value={territorioId}
            onChange={(e) => {
              setTerritorioId(e.target.value)
              setOffset(0)
            }}
            placeholder="1"
          />
        </label>
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

      <DataTable<DimPopFaixaEtaria>
        data={items}
        columns={columns}
        loading={isLoading}
        error={(error as Error | undefined)?.message ?? null}
      />

      <div className="no-print flex items-end gap-2">
        <label className="text-sm">
          <span className="block text-muted-foreground">Excluir por ID</span>
          <input
            type="number"
            className="w-28 rounded-md border bg-background px-2 py-1"
            value={deleteId}
            onChange={(e) => setDeleteId(e.target.value)}
            placeholder="id"
          />
        </label>
        <button
          className="rounded-md border px-3 py-1 text-sm disabled:opacity-50"
          disabled={!deleteId || delMut.isPending}
          onClick={() => {
            const id = Number(deleteId)
            if (!Number.isFinite(id)) return
            if (confirm('Confirmar exclusão?')) {
              delMut.mutate(id, { onSuccess: () => setDeleteId('') })
            }
          }}
        >
          Excluir
        </button>
      </div>

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

