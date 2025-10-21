import { useMemo } from 'react'
import type { ColumnDef } from '@tanstack/react-table'
import { flexRender, getCoreRowModel, getPaginationRowModel, useReactTable } from '@tanstack/react-table'

export type DataTableProps<T extends object> = {
  data: T[]
  columns: ColumnDef<T, any>[]
  loading?: boolean
  error?: string | null
}

export function DataTable<T extends object>({ data, columns, loading, error }: DataTableProps<T>) {
  const table = useReactTable({
    data: useMemo(() => data ?? [], [data]) as T[],
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  })

  if (loading) return <div className="text-sm text-muted-foreground">Carregando…</div>
  if (error) return <div className="text-sm text-destructive">Erro: {error}</div>
  if (!data?.length) return <div className="text-sm text-muted-foreground">Nenhum registro encontrado.</div>

  return (
    <div className="w-full overflow-auto">
      <table className="w-full border-collapse text-sm">
        <thead className="bg-muted text-foreground/90">
          {table.getHeaderGroups().map((hg) => (
            <tr key={hg.id}>
              {hg.headers.map((h) => (
                <th key={h.id} className="px-3 py-2 text-left font-medium">
                  {h.isPlaceholder ? null : flexRender(h.column.columnDef.header, h.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((r) => (
            <tr key={r.id} className="odd:bg-background even:bg-secondary/30">
              {r.getVisibleCells().map((c) => (
                <td key={c.id} className="px-3 py-2 align-top">
                  {flexRender(c.column.columnDef.cell, c.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default DataTable
