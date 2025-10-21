import { useMemo, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import DataTable from '../components/DataTable'
import ProvenanceBadges from '../components/Provenance'
import { listEquipes } from '../lib/api'
import type { DimEquipe } from '../lib/types'

export default function Equipes() {
  const [tipo, setTipo] = useState<string>('')
  const [ativo, setAtivo] = useState<string>('')
  const [limit, setLimit] = useState<number>(10)
  const [offset, setOffset] = useState<number>(0)

  const { data, isLoading, error } = useQuery({
    queryKey: ['equipes', { tipo, ativo, limit, offset }],
    queryFn: () =>
      listEquipes({
        tipo: tipo || undefined,
        ativo: ativo ? ativo === 'true' : undefined,
        limit,
        offset,
      }),
  })

  const columns = useMemo<ColumnDef<DimEquipe>[]>(
    () => [
      { header: 'ID', accessorKey: 'id' },
      { header: 'ID Equipe', accessorKey: 'id_equipe' },
      { header: 'Tipo', accessorKey: 'tipo' },
      { header: 'Unidade', accessorKey: 'unidade_id' },
      { header: 'Território', accessorKey: 'territorio_id' },
      { header: 'Ativo', accessorKey: 'ativo' },
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
        <h2>Dimensão: Equipes</h2>
      </div>

      <div className="no-print flex flex-wrap items-end gap-3">
        <label className="text-sm">
          <span className="block text-muted-foreground">Tipo</span>
          <select
            className="w-40 rounded-md border bg-background px-2 py-1"
            value={tipo}
            onChange={(e) => {
              setTipo(e.target.value)
              setOffset(0)
            }}
          >
            <option value="">Todos</option>
            {['ESF', 'ESB', 'ACS', 'OUTROS'].map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">Ativo</span>
          <select
            className="w-32 rounded-md border bg-background px-2 py-1"
            value={ativo}
            onChange={(e) => {
              setAtivo(e.target.value)
              setOffset(0)
            }}
          >
            <option value="">Todos</option>
            <option value="true">Sim</option>
            <option value="false">Não</option>
          </select>
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

      <DataTable<DimEquipe>
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
