import { useMemo, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import DataTable from '../components/DataTable'
import ProvenanceBadges from '../components/Provenance'
import { listFontes, deleteFonte } from '../lib/api'
import type { DimFonteRecurso } from '../lib/types'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from '@/components/ui/select'

export default function Fontes() {
  const [codigo, setCodigo] = useState<string>('')
  const [limit, setLimit] = useState<number>(10)
  const [offset, setOffset] = useState<number>(0)
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
      { header: 'Código', accessorKey: 'codigo' },
      { header: 'Descrição', accessorKey: 'descricao' },
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

      <div className="no-print grid grid-cols-1 sm:grid-cols-4 gap-3 items-end">
        <div className="space-y-1">
          <Label htmlFor="f-codigo">Código</Label>
          <Input id="f-codigo" className="w-40" value={codigo} placeholder="001" onChange={(e) => { setCodigo(e.target.value); setOffset(0) }} />
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

      <DataTable<DimFonteRecurso>
        data={items}
        columns={columns}
        loading={isLoading}
        error={(error as Error | undefined)?.message ?? null}
      />

      <div className="no-print flex items-center justify-between">
        <Button variant="outline" className="min-w-28" disabled={offset === 0} onClick={() => setOffset((o) => Math.max(0, o - limit))}>← Anterior</Button>
        <Button variant="outline" className="min-w-28" disabled={items.length < limit} onClick={() => setOffset((o) => o + limit)}>Próxima →</Button>
      </div>
    </section>
  )
}
