import { useEffect, useRef, useState } from 'react'
import QRCode from 'qrcode'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

import { buildRDQAHtml } from '../../lib/rdqa'
import { exportRAGPdf, getRAGResumo } from '../../lib/api'
import { mockRagResumo } from '../../lib/mocks/rag'
import type { RAGResumo } from '../../lib/types'

export default function RagResumo() {
  const contentRef = useRef<HTMLDivElement | null>(null)
  const [territorioId, setTerritorioId] = useState('')
  const [periodo, setPeriodo] = useState('2024')
  const [dados, setDados] = useState<RAGResumo | null>(null)
  const [carregando, setCarregando] = useState(false)
  const [exportando, setExportando] = useState(false)

  const carregar = async () => {
    setCarregando(true)
    try {
      const territorio = territorioId ? Number(territorioId) : undefined
      const resposta = await getRAGResumo(periodo || undefined, territorio)
      setDados(resposta)
    } catch (err) {
      console.warn('[rag/resumo] fallback para mocks', err)
      setDados(mockRagResumo)
    } finally {
      setCarregando(false)
    }
  }

  useEffect(() => {
    carregar()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const onExportar = async () => {
    if (!contentRef.current) return
    setExportando(true)
    try {
      const title = 'RAG - Resumo Executivo'
      const contentHtml = contentRef.current.innerHTML
      const meta = { periodo: periodo || dados?.periodos?.join(', ') || 'n/d', territorioId: territorioId || 'todos' }
      const initialHtml = buildRDQAHtml({ title, contentHtml, meta })
      let { blob, execId, hash } = await exportRAGPdf({ html: initialHtml, format: 'A4', margin_mm: 12 })
      if (execId && hash) {
        const verifyUrl = `${import.meta.env.VITE_API_BASE}/public/verificar?exec_id=${encodeURIComponent(execId)}&hash=${encodeURIComponent(hash)}`
        const qrDataUrl = await QRCode.toDataURL(verifyUrl)
        const withQrHtml = buildRDQAHtml({ title, contentHtml, meta, qrDataUrl })
        const second = await exportRAGPdf({ html: withQrHtml, format: 'A4', margin_mm: 12 })
        blob = second.blob
      }
      const url = URL.createObjectURL(blob)
      const anchor = document.createElement('a')
      anchor.href = url
      anchor.download = 'rag-resumo.pdf'
      anchor.click()
      URL.revokeObjectURL(url)
    } catch (err) {
      alert(err instanceof Error ? err.message : String(err))
    } finally {
      setExportando(false)
    }
  }

  return (
    <section className="space-y-4">
      <div className="prose max-w-none dark:prose-invert">
        <h2>RAG - Resumo</h2>
        <p className="text-sm text-muted-foreground">
          Consolidado de execucao financeira, producao e metas. Carregue os dados reais via API; em caso de indisponibilidade, o frontend exibe mocks.
        </p>
      </div>

      <div className="no-print grid grid-cols-1 sm:grid-cols-3 gap-3 items-end">
        <div className="space-y-1">
          <Label htmlFor="rag-resumo-territorio">Territorio ID</Label>
          <Input id="rag-resumo-territorio" value={territorioId} onChange={(e) => setTerritorioId(e.target.value)} placeholder="ex.: 1" />
        </div>
        <div className="space-y-1">
          <Label htmlFor="rag-resumo-periodo">Periodo</Label>
          <Input id="rag-resumo-periodo" value={periodo} onChange={(e) => setPeriodo(e.target.value)} placeholder="ex.: 2024" />
        </div>
        <div className="space-y-1">
          <Label className="invisible">Acoes</Label>
          <div className="flex gap-2">
            <Button variant="secondary" onClick={carregar} disabled={carregando}>{carregando ? 'Carregando...' : 'Atualizar'}</Button>
            <Button onClick={onExportar} disabled={exportando || !dados}>{exportando ? 'Gerando...' : 'Exportar PDF'}</Button>
          </div>
        </div>
      </div>

      <div className="rounded-lg border bg-card p-4">
        <div className="flex items-baseline justify-between mb-3">
          <h3 className="text-base font-semibold">Resumo por territorio</h3>
          <p className="text-xs text-muted-foreground">{dados?.periodos?.join(', ') || 'n/d'}</p>
        </div>
        <div ref={contentRef}>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Territorio</TableHead>
                <TableHead>Dotacao</TableHead>
                <TableHead>Pago</TableHead>
                <TableHead>Execucao %</TableHead>
                <TableHead>Producao total</TableHead>
                <TableHead>Metas</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {dados?.itens?.map((item) => (
                <TableRow key={`${item.territorio_id}-${item.periodo}`}>
                  <TableCell>{item.territorio_nome || `Territorio ${item.territorio_id}`}</TableCell>
                  <TableCell>{item.dotacao_atualizada?.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }) ?? '-'}</TableCell>
                  <TableCell>{item.pago?.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }) ?? '-'}</TableCell>
                  <TableCell>{item.execucao_percentual !== undefined && item.execucao_percentual !== null ? `${item.execucao_percentual.toFixed(1)}%` : '-'}</TableCell>
                  <TableCell>{item.producao_total?.toLocaleString('pt-BR') ?? '-'}</TableCell>
                  <TableCell>{item.metas_cumpridas}/{item.metas_total}</TableCell>
                </TableRow>
              ))}
              {!dados?.itens?.length && (
                <TableRow>
                  <TableCell colSpan={6} className="text-center text-sm text-muted-foreground py-6">Nenhum dado encontrado.</TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </div>
    </section>
  )
}
