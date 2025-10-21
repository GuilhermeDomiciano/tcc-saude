import { useMemo, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import type { ColumnDef } from '@tanstack/react-table'
import DataTable from '../components/DataTable'
import ProvenanceBadges from '../components/Provenance'
import { listTerritorios, deleteTerritorio } from '../lib/api'
import type { DimTerritorio } from '../lib/types'
import Modal from '../components/Modal'
import TerritorioForm from '../components/forms/TerritorioForm'

export default function Territorios() {
  const [uf, setUf] = useState<string>('')
  const [ibge, setIbge] = useState<string>('')
  const [limit, setLimit] = useState<number>(10)
  const [offset, setOffset] = useState<number>(0)
  // removed legacy delete-by-id control in favor of row actions
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
            <button className="rounded-md border px-2 py-0.5 text-xs" onClick={() => setEditing(row.original)}>Editar</button>
            <button className="rounded-md border px-2 py-0.5 text-xs" onClick={() => { if (confirm('Excluir este registro?')) delMut.mutate(row.original.id) }}>Excluir</button>
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
          />
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

      <div className="no-print">
        <button onClick={() => setShowCreate(true)} className="rounded-md border bg-primary px-3 py-1 text-sm text-primary-foreground">Novo</button>
      </div>

      <DataTable<DimTerritorio>
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

