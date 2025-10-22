import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

import { getRAGProducao } from '../../lib/api'
import { mockRagProducao } from '../../lib/mocks/rag'
import type { RAGProducaoItem } from '../../lib/types'

export default function RagProducao() {
  const [territorioId, setTerritorioId] = useState('')
  const [periodo, setPeriodo] = useState('2024')
  const [dados, setDados] = useState<RAGProducaoItem[]>([])
  const [carregando, setCarregando] = useState(false)

  const carregar = async () => {
    setCarregando(true)
    try {
      const territorio = territorioId ? Number(territorioId) : undefined
      const resposta = await getRAGProducao(periodo || undefined, territorio)
      setDados(resposta)
    } catch (err) {
      console.warn('[rag/producao] fallback para mocks', err)
      setDados(mockRagProducao)
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
        <h2>RAG - Producao assistencial</h2>
        <p className="text-sm text-muted-foreground">Quantidades consolidadas por tipo de servico e territorio.</p>
      </div>

      <div className="no-print grid grid-cols-1 sm:grid-cols-3 gap-3 items-end">
        <div className="space-y-1">
          <Label htmlFor="rag-prod-territorio">Territorio ID</Label>
          <Input id="rag-prod-territorio" value={territorioId} onChange={(e) => setTerritorioId(e.target.value)} placeholder="ex.: 1" />
        </div>
        <div className="space-y-1">
          <Label htmlFor="rag-prod-periodo">Periodo</Label>
          <Input id="rag-prod-periodo" value={periodo} onChange={(e) => setPeriodo(e.target.value)} placeholder="ex.: 2024" />
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
              <TableHead>Tipo</TableHead>
              <TableHead>Quantidade</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {dados.map((row, index) => (
              <TableRow key={`${row.territorio_id}-${row.periodo}-${index}`}>
                <TableCell>{row.territorio_nome || `Territorio ${row.territorio_id}`}</TableCell>
                <TableCell>{row.periodo}</TableCell>
                <TableCell>{row.tipo}</TableCell>
                <TableCell>{row.quantidade?.toLocaleString('pt-BR') ?? '-'}</TableCell>
              </TableRow>
            ))}
            {!dados.length && (
              <TableRow>
                <TableCell colSpan={4} className="text-center text-sm text-muted-foreground py-6">Nenhum registro.</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </section>
  )
}
