import { useMemo, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import DataTable from '../components/DataTable'
import ProvenanceBadges from '../components/Provenance'
import { listTempo, deleteTempo } from '../lib/api'
import type { DimTempo } from '../lib/types'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import TempoForm from '../components/forms/TempoForm'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from '@/components/ui/select'

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
      {
        id: 'acoes',
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
    ],
    [],
  )

  const items = data ?? []

  return (
    <section className="space-y-4">
      <div className="prose max-w-none dark:prose-invert">
        <h2>Dimensão: Tempo</h2>
      </div>

      <div className="no-print grid grid-cols-1 sm:grid-cols-4 gap-3 items-end">
        <div className="space-y-1">
          <Label htmlFor="f-ano">Ano</Label>
          <Input id="f-ano" type="number" className="w-28" value={ano} placeholder="2025" aria-label="Filtro por ano"
            onChange={(e) => { setAno(e.target.value); setOffset(0) }} />
        </div>
        <div className="space-y-1">
          <Label htmlFor="f-mes">Mês</Label>
          <Input id="f-mes" type="number" min={1} max={12} className="w-24" value={mes} placeholder="1..12" aria-label="Filtro por mês"
            onChange={(e) => { setMes(e.target.value); setOffset(0) }} />
        </div>
        <div className="space-y-1">
          <Label>Linhas por página</Label>
          <Select value={String(limit)} onValueChange={(v) => { setLimit(Number(v)); setOffset(0) }}>
            <SelectTrigger className="w-28"><SelectValue /></SelectTrigger>
            <SelectContent>
              {[10,20,50].map(n => (
                <SelectItem key={n} value={String(n)}>{n}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
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
      <Dialog open={showCreate} onOpenChange={setShowCreate}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Tempo</DialogTitle>
          </DialogHeader>
          <TempoForm onSuccess={() => setShowCreate(false)} />
        </DialogContent>
      </Dialog>
    </section>
  )
}
