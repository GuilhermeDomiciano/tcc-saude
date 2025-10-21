import { useMemo, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import DataTable from '../components/DataTable'
import ProvenanceBadges from '../components/Provenance'
import { listTempo, deleteTempo } from '../lib/api'
import type { DimTempo } from '../lib/types'
import Modal from '../components/Modal'
import TempoForm from '../components/forms/TempoForm'
import { Button } from '@/components/ui/button'

export default function Tempo() {
  const [ano, setAno] = useState<string>('')
  const [mes, setMes] = useState<string>('')
  const [limit, setLimit] = useState<number>(10)
  const [offset, setOffset] = useState<number>(0)
  const [showCreate, setShowCreate] = useState(false)
  const queryClient = useQueryClient()
  const delMut = useMutation({
    mutationFn: (id: number) => deleteTempo(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['tempo'] }),
  })

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
      {
        header: 'Ações',
        cell: ({ row }) => (
          <Button
            className="no-print"
            size="sm"
            variant="destructive"
            aria-label={`Excluir registro ${row.original.id}`}
            onClick={() => {
              if (confirm('Excluir este registro?')) delMut.mutate(row.original.id)
            }}
          >
            Excluir
          </Button>
        ),
      },
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
            aria-label="Filtro por ano"
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
            aria-label="Filtro por mês"
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
            aria-label="Linhas por página"
          >
            {[10, 20, 50].map((n) => (
              <option key={n} value={n}>
                {n}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="no-print">
        <Button onClick={() => setShowCreate(true)} aria-label="Novo período">Novo</Button>
      </div>

      <DataTable<DimTempo>
        data={items}
        columns={columns}
        loading={isLoading}
        error={(error as Error | undefined)?.message ?? null}
      />

      <div className="no-print flex items-center justify-between">
        <Button
          variant="outline"
          className="min-w-28"
          disabled={offset === 0}
          onClick={() => setOffset((o) => Math.max(0, o - limit))}
          aria-label="Página anterior"
        >
          ← Anterior
        </Button>
        <Button
          variant="outline"
          className="min-w-28"
          disabled={items.length < limit}
          onClick={() => setOffset((o) => o + limit)}
          aria-label="Próxima página"
        >
          Próxima →
        </Button>
      </div>
      <Modal open={showCreate} onClose={() => setShowCreate(false)} title="Tempo">
        <TempoForm onSuccess={() => setShowCreate(false)} />
      </Modal>
    </section>
  )
}

