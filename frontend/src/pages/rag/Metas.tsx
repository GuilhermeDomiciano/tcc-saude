import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

import { getRAGMetas } from '../../lib/api'
import { mockRagMetas } from '../../lib/mocks/rag'
import type { RAGMetaItem } from '../../lib/types'

export default function RagMetas() {
  const [territorioId, setTerritorioId] = useState('')
  const [periodo, setPeriodo] = useState('2024')
  const [dados, setDados] = useState<RAGMetaItem[]>([])
  const [carregando, setCarregando] = useState(false)

  const carregar = async () => {
    setCarregando(true)
    try {
      const territorio = territorioId ? Number(territorioId) : undefined
      const resposta = await getRAGMetas(periodo || undefined, territorio)
      setDados(resposta)
    } catch (err) {
      console.warn('[rag/metas] fallback para mocks', err)
      setDados(mockRagMetas)
    } finally {
      setCarregando(false)
    }
  }

  useEffect(() => {
    carregar()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <section className="space-y-4">
      <div className="prose max-w-none dark:prose-invert">
        <h2>RAG - Metas</h2>
        <p className="text-sm text-muted-foreground">Comparativo meta planejada x executada, com status de cumprimento.</p>
      </div>

      <div className="no-print grid grid-cols-1 sm:grid-cols-3 gap-3 items-end">
        <div className="space-y-1">
          <Label htmlFor="rag-metas-territorio">Territorio ID</Label>
          <Input id="rag-metas-territorio" value={territorioId} onChange={(e) => setTerritorioId(e.target.value)} placeholder="ex.: 1" />
        </div>
        <div className="space-y-1">
          <Label htmlFor="rag-metas-periodo">Periodo</Label>
          <Input id="rag-metas-periodo" value={periodo} onChange={(e) => setPeriodo(e.target.value)} placeholder="ex.: 2024" />
        </div>
        <div className="space-y-1">
          <Label className="invisible">Acoes</Label>
          <Button variant="secondary" onClick={carregar} disabled={carregando}>{carregando ? 'Carregando...' : 'Atualizar'}</Button>
        </div>
      </div>

      <div className="rounded-lg border bg-card p-4">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Territorio</TableHead>
              <TableHead>Periodo</TableHead>
              <TableHead>Indicador</TableHead>
              <TableHead>Meta planejada</TableHead>
              <TableHead>Meta executada</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {dados.map((row) => (
              <TableRow key={`${row.territorio_id}-${row.periodo}-${row.indicador}`}>
                <TableCell>{row.territorio_nome || `Territorio ${row.territorio_id}`}</TableCell>
                <TableCell>{row.periodo}</TableCell>
                <TableCell>{row.indicador}</TableCell>
                <TableCell>{row.meta_planejada ?? '-'}</TableCell>
                <TableCell>{row.meta_executada ?? '-'}</TableCell>
                <TableCell>
                  {row.cumprida === null || row.cumprida === undefined ? (
                    <span className="text-muted-foreground">n/d</span>
                  ) : row.cumprida ? (
                    <span className="text-green-600">Cumprida</span>
                  ) : (
                    <span className="text-red-500">Nao cumprida</span>
                  )}
                </TableCell>
              </TableRow>
            ))}
            {!dados.length && (
              <TableRow>
                <TableCell colSpan={6} className="text-center text-sm text-muted-foreground py-6">Nenhum registro.</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </section>
  )
}
