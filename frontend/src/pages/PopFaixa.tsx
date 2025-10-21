import { useMemo, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import DataTable from '../components/DataTable'
import ProvenanceBadges from '../components/Provenance'
import { listPopFaixa, deletePopFaixa } from '../lib/api'
import type { DimPopFaixaEtaria } from '../lib/types'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from '@/components/ui/select'

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
      {
        id: 'acoes',
        header: 'Ações',
        cell: ({ row }) => (
          <Button className="no-print" size="sm" variant="destructive" onClick={() => { if (confirm('Excluir este registro?')) delMut.mutate(row.original.id) }}>
            Excluir
          </Button>
        ),
      },
      { header: 'ID', accessorKey: 'id' },
      { header: 'Território', accessorKey: 'territorio_id' },
      { header: 'Ano', accessorKey: 'ano' },
      { header: 'Faixa Etária', accessorKey: 'faixa_etaria' },
      { header: 'Sexo', accessorKey: 'sexo' },
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

      <div className="no-print grid grid-cols-1 sm:grid-cols-4 gap-3 items-end">
        <div className="space-y-1">
          <Label htmlFor="f-territorio">Território ID</Label>
          <Input id="f-territorio" type="number" className="w-32" value={territorioId} placeholder="1" onChange={(e) => { setTerritorioId(e.target.value); setOffset(0) }} />
        </div>
        <div className="space-y-1">
          <Label htmlFor="f-ano">Ano</Label>
          <Input id="f-ano" type="number" className="w-28" value={ano} placeholder="2025" onChange={(e) => { setAno(e.target.value); setOffset(0) }} />
        </div>
        <div className="space-y-1">
          <Label>Linhas por página</Label>
          <Select value={String(limit)} onValueChange={(v) => { setLimit(Number(v)); setOffset(0) }}>
            <SelectTrigger className="w-28"><SelectValue /></SelectTrigger>
            <SelectContent>
              {[10, 20, 50].map((n) => (
                <SelectItem key={n} value={String(n)}>{n}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <DataTable<DimPopFaixaEtaria>
        data={items}
        columns={columns}
        loading={isLoading}
        error={(error as Error | undefined)?.message ?? null}
      />

      <div className="no-print grid grid-cols-1 sm:grid-cols-3 gap-2 items-end">
        <div className="space-y-1">
          <Label htmlFor="del-id">Excluir por ID</Label>
          <Input id="del-id" type="number" className="w-28" value={deleteId} placeholder="id" onChange={(e) => setDeleteId(e.target.value)} />
        </div>
        <div>
          <Button disabled={!deleteId || delMut.isPending} onClick={() => {
            const id = Number(deleteId)
            if (!Number.isFinite(id)) return
            if (confirm('Confirmar exclusão?')) {
              delMut.mutate(id, { onSuccess: () => setDeleteId('') })
            }
          }}>Excluir</Button>
        </div>
      </div>

      <div className="no-print flex items-center justify-between">
        <Button variant="outline" className="min-w-28" disabled={offset === 0} onClick={() => setOffset((o) => Math.max(0, o - limit))}>← Anterior</Button>
        <Button variant="outline" className="min-w-28" disabled={items.length < limit} onClick={() => setOffset((o) => o + limit)}>Próxima →</Button>
      </div>
    </section>
  )
}
