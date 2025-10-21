import { useMemo, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import DataTable from '../components/DataTable'
import ProvenanceBadges from '../components/Provenance'
import { listTerritorios, deleteTerritorio } from '../lib/api'
import type { DimTerritorio } from '../lib/types'
import Modal from '../components/Modal'
import TerritorioForm from '../components/forms/TerritorioForm'
import { Button } from '@/components/ui/button'

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
      { header: 'ID', accessorKey: 'id' },
      { header: 'Município (IBGE)', accessorKey: 'cod_ibge_municipio' },
      { header: 'Nome', accessorKey: 'nome' },
      { header: 'UF', accessorKey: 'uf' },
      { header: 'Área km²', accessorKey: 'area_km2' },
      { header: 'Pop. Censo 2022', accessorKey: 'pop_censo_2022' },
      { header: 'Pop. Estim. 2024', accessorKey: 'pop_estim_2024' },
      {
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

      <div className="no-print flex flex-wrap items-end gap-3">
        <label className="text-sm">
          <span className="block text-muted-foreground">UF</span>
          <input
            className="w-20 uppercase rounded-md border bg-background px-2 py-1"
            maxLength={2}
            value={uf}
            onChange={(e) => {
              setUf(e.target.value.toUpperCase())
              setOffset(0)
            }}
            placeholder="RS"
            aria-describedby="ajuda-uf"
            aria-label="Filtro por UF"
          />
          <span id="ajuda-uf" className="block text-xs text-muted-foreground">2 letras, ex.: RS</span>
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">IBGE</span>
          <input
            className="w-32 rounded-md border bg-background px-2 py-1"
            value={ibge}
            onChange={(e) => {
              setIbge(e.target.value)
              setOffset(0)
            }}
            placeholder="4300000"
            inputMode="numeric"
            aria-label="Filtro por código IBGE"
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
      <Modal open={showCreate} onClose={() => setShowCreate(false)} title="Novo Território">
        <TerritorioForm onSuccess={() => setShowCreate(false)} />
      </Modal>
      <Modal open={!!editing} onClose={() => setEditing(null)} title="Editar Território">
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
      </Modal>
    </section>
  )
}

