import { useEffect, useRef, useState } from 'react'
import { exportRDQAPdf, getRDQACobertura } from '../../lib/api'
import { buildRDQAHtml } from '../../lib/rdqa'
import QRCode from 'qrcode'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

export default function RdqaCobertura() {
  const contentRef = useRef<HTMLDivElement | null>(null)
  const [territorioId, setTerritorioId] = useState('')
  const [periodo, setPeriodo] = useState('')
  const [loading, setLoading] = useState(false)
  const [dados, setDados] = useState<{ percent: number; total: number; gerados: number; faltantes: Array<{ quadro: string; periodo: string; motivo: string }> } | null>(null)
  const [loadingData, setLoadingData] = useState(false)

  const carregar = async () => {
    setLoadingData(true)
    try {
      const d = await getRDQACobertura(periodo || undefined)
      setDados(d)
    } catch (e) {
      alert(e instanceof Error ? e.message : String(e))
    } finally {
      setLoadingData(false)
    }
  }
  
  useEffect(() => {
    carregar()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const onExport = async () => {
    if (!contentRef.current) return
    setLoading(true)
    try {
      const contentHtml = contentRef.current.innerHTML
      const title = 'Quadro RDQA — Cobertura'
      const initialHtml = buildRDQAHtml({ title, contentHtml, meta: { territorioId, periodo } })
      let { blob, execId, hash } = await exportRDQAPdf({ html: initialHtml, format: 'A4', margin_mm: 12 })
      if (execId && hash) {
        const verifyUrl = `${import.meta.env.VITE_API_BASE}/public/verificar?exec_id=${encodeURIComponent(execId)}&hash=${encodeURIComponent(hash)}`
        const qrDataUrl = await QRCode.toDataURL(verifyUrl)
        const withQrHtml = buildRDQAHtml({ title, contentHtml, meta: { territorioId, periodo }, qrDataUrl })
        const second = await exportRDQAPdf({ html: withQrHtml, format: 'A4', margin_mm: 12 })
        blob = second.blob
      }
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'rdqa-cobertura.pdf'
      a.click()
      URL.revokeObjectURL(url)
    } catch (e) {
      alert(e instanceof Error ? e.message : String(e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="space-y-4">
      <div className="prose max-w-none dark:prose-invert">
        <h2>RDQA — Cobertura</h2>
        <p className="text-sm text-muted-foreground">Evolução de cobertura por equipe e período com base no denominador populacional.</p>
      </div>

      <div className="no-print grid grid-cols-1 sm:grid-cols-3 gap-3 items-end">
        <div className="space-y-1">
          <Label htmlFor="f-territorio">Território ID</Label>
          <Input id="f-territorio" className="w-40" value={territorioId} onChange={(e) => setTerritorioId(e.target.value)} placeholder="Ex.: 1" />
        </div>
        <div className="space-y-1">
          <Label htmlFor="f-periodo">Período</Label>
          <Input id="f-periodo" className="w-64" value={periodo} onChange={(e) => setPeriodo(e.target.value)} placeholder="Ex.: 2024-01 a 2024-12" />
        </div>
        <div className="space-y-1">
          <Label className="invisible">Ações</Label>
          <div className="flex gap-2">
            <Button variant="secondary" onClick={carregar} disabled={loadingData}>{loadingData ? 'Carregando…' : 'Carregar'}</Button>
            <Button onClick={onExport} disabled={loading}>{loading ? 'Gerando…' : 'Exportar PDF'}</Button>
          </div>
        </div>
      </div>

      <div className="rounded-lg border bg-card p-4">
        <div className="flex items-baseline justify-between mb-3">
          <h3 className="text-base font-semibold">Quadro de Cobertura</h3>
          <p className="text-xs text-muted-foreground">{territorioId || '—'} • {periodo || '—'}</p>
        </div>
        <div ref={contentRef} id="rdqa-print">
          <div className="mb-3 text-sm text-muted-foreground">
            {dados ? (
              <span>Cobertura: {dados.percent.toFixed(2)}% ({dados.gerados}/{dados.total})</span>
            ) : (
              <span>Informe período e clique em Carregar.</span>
            )}
          </div>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Ações</TableHead>
                <TableHead>Quadro</TableHead>
                <TableHead>Período</TableHead>
                <TableHead>Motivo</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {dados?.faltantes?.map((f) => (
                <TableRow key={`${f.quadro}-${f.periodo}`}>
                  <TableCell>—</TableCell>
                  <TableCell>{f.quadro}</TableCell>
                  <TableCell>{f.periodo}</TableCell>
                  <TableCell>{f.motivo}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </div>
    </section>
  )
}
