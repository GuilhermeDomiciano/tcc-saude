import { useMemo, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import DataTable from '../components/DataTable'
import ProvenanceBadges from '../components/Provenance'
import { listTerritorios, deleteTerritorio } from '../lib/api'
import type { DimTerritorio } from '../lib/types'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import TerritorioForm from '../components/forms/TerritorioForm'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from '@/components/ui/select'

export default function Territorios() {
  const [uf, setUf] = useState<string>('')
  const [ibge, setIbge] = useState<string>('')
  const [limit, setLimit] = useState<number>(10)
  const [offset, setOffset] = useState<number>(0)
  const queryClient = useQueryClient()
  const delMut = useMutation({
    mutationFn: (id: number) => deleteTerritorio(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['territorios'] }),
  })
  const [showCreate, setShowCreate] = useState(false)
  const [editing, setEditing] = useState<DimTerritorio | null>(null)

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
      {
        id: 'acoes',
        header: 'Ações',
        cell: ({ row }) => (
          <div className="no-print flex gap-2">
            <Button size="sm" variant="outline" aria-label={`Editar ${row.original.nome}`} onClick={() => setEditing(row.original)}>
              Editar
            </Button>
            <Button
              size="sm"
              variant="destructive"
              aria-label={`Excluir ${row.original.nome}`}
              onClick={() => {
                if (confirm('Excluir este registro?')) delMut.mutate(row.original.id)
              }}
            >
              Excluir
            </Button>
          </div>
        ),
      },
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
        <h2>Dimensão: Territórios</h2>
      </div>

      <div className="no-print grid grid-cols-1 sm:grid-cols-4 gap-3 items-end">
        <div className="space-y-1">
          <Label htmlFor="f-uf">UF</Label>
          <Input id="f-uf" className="w-20 uppercase" maxLength={2} value={uf} placeholder="RS"
            aria-describedby="ajuda-uf"
            onChange={(e) => { setUf(e.target.value.toUpperCase()); setOffset(0) }} />
          <span id="ajuda-uf" className="block text-xs text-muted-foreground">2 letras, ex.: RS</span>
        </div>
        <div className="space-y-1">
          <Label htmlFor="f-ibge">IBGE</Label>
          <Input id="f-ibge" className="w-32" value={ibge} placeholder="4300000" inputMode="numeric"
            onChange={(e) => { setIbge(e.target.value); setOffset(0) }} />
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
        <Button onClick={() => setShowCreate(true)} aria-label="Novo território">Novo</Button>
      </div>

      <DataTable<DimTerritorio>
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
            <DialogTitle>Novo Território</DialogTitle>
          </DialogHeader>
          <TerritorioForm onSuccess={() => setShowCreate(false)} />
        </DialogContent>
      </Dialog>
      <Dialog open={!!editing} onOpenChange={(o) => !o && setEditing(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Editar Território</DialogTitle>
          </DialogHeader>
          {editing && (
            <TerritorioForm
              initial={{
                id: editing.id,
                cod_ibge_municipio: editing.cod_ibge_municipio,
                nome: editing.nome,
                uf: editing.uf,
                area_km2: editing.area_km2 ?? undefined,
                pop_censo_2022: editing.pop_censo_2022 ?? undefined,
                pop_estim_2024: editing.pop_estim_2024 ?? undefined,
              }}
              onSuccess={() => setEditing(null)}
            />
          )}
        </DialogContent>
      </Dialog>
    </section>
  )
}
