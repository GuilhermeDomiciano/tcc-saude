import { useRef, useState } from 'react'
import { exportRDQAPdf } from '../../lib/api'
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
          <Label className="invisible">Exportar</Label>
          <Button onClick={onExport} disabled={loading}>{loading ? 'Gerando…' : 'Exportar PDF'}</Button>
        </div>
      </div>

      <div className="rounded-lg border bg-card p-4">
        <div className="flex items-baseline justify-between mb-3">
          <h3 className="text-base font-semibold">Quadro de Cobertura</h3>
          <p className="text-xs text-muted-foreground">{territorioId || '—'} • {periodo || '—'}</p>
        </div>
        <div ref={contentRef} id="rdqa-print">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Tempo</TableHead>
                <TableHead>Equipe</TableHead>
                <TableHead>Cobertura %</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell>2024-01</TableCell>
                <TableCell>ESF 01</TableCell>
                <TableCell>72,3%</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>2024-02</TableCell>
                <TableCell>ESF 01</TableCell>
                <TableCell>73,1%</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </div>
    </section>
  )
}

