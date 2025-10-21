import { useMemo } from 'react'
import type { ColumnDef } from '@tanstack/react-table'
import { flexRender, getCoreRowModel, getPaginationRowModel, useReactTable } from '@tanstack/react-table'
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

export type DataTableProps<T extends object> = {
  data: T[]
  columns: ColumnDef<T, unknown>[]
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

  if (loading) return <div className="text-sm text-muted-foreground" aria-live="polite">Carregando…</div>
  if (error) return <div className="text-sm text-destructive">Erro: {error}</div>
  if (!data?.length) return <div className="text-sm text-muted-foreground">Nenhum registro encontrado.</div>

  return (
    <Table className="rounded-md outline outline-border overflow-hidden">
      <TableCaption>Tabela de dados</TableCaption>
      <TableHeader>
        {table.getHeaderGroups().map((hg) => (
          <TableRow key={hg.id}>
            {hg.headers.map((h) => (
              <TableHead key={h.id} scope="col">
                {h.isPlaceholder ? null : flexRender(h.column.columnDef.header, h.getContext())}
              </TableHead>
            ))}
          </TableRow>
        ))}
      </TableHeader>
      <TableBody>
        {table.getRowModel().rows.map((r) => (
          <TableRow key={r.id} className="border-t border-border">
            {r.getVisibleCells().map((c) => (
              <TableCell key={c.id}>
                {flexRender(c.column.columnDef.cell, c.getContext())}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

export default DataTable
