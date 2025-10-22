import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

import { getRAGFinanceiro } from '../../lib/api'
import { mockRagFinanceiro } from '../../lib/mocks/rag'
import type { RAGFinanceiroItem } from '../../lib/types'

export default function RagFinanceiro() {
  const [territorioId, setTerritorioId] = useState('')
  const [periodo, setPeriodo] = useState('2024')
  const [dados, setDados] = useState<RAGFinanceiroItem[]>([])
  const [carregando, setCarregando] = useState(false)

  const carregar = async () => {
    setCarregando(true)
    try {
      const territorio = territorioId ? Number(territorioId) : undefined
      const resposta = await getRAGFinanceiro(periodo || undefined, territorio)
      setDados(resposta)
    } catch (err) {
      console.warn('[rag/financeiro] fallback para mocks', err)
      setDados(mockRagFinanceiro)
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
        <h2>RAG - Financeiro</h2>
        <p className="text-sm text-muted-foreground">Detalhes de dotacao, receita, empenho, liquidacao e pagamento por territorio.</p>
      </div>

      <div className="no-print grid grid-cols-1 sm:grid-cols-3 gap-3 items-end">
        <div className="space-y-1">
          <Label htmlFor="rag-fin-territorio">Territorio ID</Label>
          <Input id="rag-fin-territorio" value={territorioId} onChange={(e) => setTerritorioId(e.target.value)} placeholder="ex.: 1" />
        </div>
        <div className="space-y-1">
          <Label htmlFor="rag-fin-periodo">Periodo</Label>
          <Input id="rag-fin-periodo" value={periodo} onChange={(e) => setPeriodo(e.target.value)} placeholder="ex.: 2024" />
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
              <TableHead>Dotacao</TableHead>
              <TableHead>Receita</TableHead>
              <TableHead>Empenhado</TableHead>
              <TableHead>Liquidado</TableHead>
              <TableHead>Pago</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {dados.map((row) => (
              <TableRow key={`${row.territorio_id}-${row.periodo}`}>
                <TableCell>{row.territorio_nome || `Territorio ${row.territorio_id}`}</TableCell>
                <TableCell>{row.periodo}</TableCell>
                <TableCell>{row.dotacao_atualizada?.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }) ?? '-'}</TableCell>
                <TableCell>{row.receita_realizada?.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }) ?? '-'}</TableCell>
                <TableCell>{row.empenhado?.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }) ?? '-'}</TableCell>
                <TableCell>{row.liquidado?.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }) ?? '-'}</TableCell>
                <TableCell>{row.pago?.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }) ?? '-'}</TableCell>
              </TableRow>
            ))}
            {!dados.length && (
              <TableRow>
                <TableCell colSpan={7} className="text-center text-sm text-muted-foreground py-6">Nenhum registro.</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </section>
  )
}
