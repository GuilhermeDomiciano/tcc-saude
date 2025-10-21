import { useRef, useState } from 'react'
import { exportRDQAPdf } from '../../lib/api'
import { buildRDQAHtml } from '../../lib/rdqa'
import QRCode from 'qrcode'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

export default function RdqaConsistencia() {
  const contentRef = useRef<HTMLDivElement | null>(null)
  const [municipio, setMunicipio] = useState('')
  const [periodo, setPeriodo] = useState('')
  const [loading, setLoading] = useState(false)

  const onExport = async () => {
    if (!contentRef.current) return
    setLoading(true)
    try {
      const contentHtml = contentRef.current.innerHTML
      const title = 'Quadro RDQA — Consistência'
      const initialHtml = buildRDQAHtml({ title, contentHtml, meta: { municipio, periodo } })
      let { blob, execId, hash } = await exportRDQAPdf({ html: initialHtml, format: 'A4', margin_mm: 12 })
      if (execId && hash) {
        const verifyUrl = `${import.meta.env.VITE_API_BASE}/public/verificar?exec_id=${encodeURIComponent(execId)}&hash=${encodeURIComponent(hash)}`
        const qrDataUrl = await QRCode.toDataURL(verifyUrl)
        const withQrHtml = buildRDQAHtml({ title, contentHtml, meta: { municipio, periodo }, qrDataUrl })
        const second = await exportRDQAPdf({ html: withQrHtml, format: 'A4', margin_mm: 12 })
        blob = second.blob
      }
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'rdqa-consistencia.pdf'
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
        <h2>RDQA — Consistência</h2>
        <p className="text-sm text-muted-foreground">Compare totais por indicador entre fontes oficiais para identificar divergências.</p>
      </div>

      <div className="no-print grid grid-cols-1 sm:grid-cols-3 gap-3 items-end">
        <div className="space-y-1">
          <Label htmlFor="f-municipio">Município</Label>
          <Input id="f-municipio" className="w-64" value={municipio} onChange={(e) => setMunicipio(e.target.value)} placeholder="Ex.: Município A" />
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
          <h3 className="text-base font-semibold">Quadro de Consistência</h3>
          <p className="text-xs text-muted-foreground">{municipio || '—'} • {periodo || '—'}</p>
        </div>
        <div ref={contentRef} id="rdqa-print">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Indicador</TableHead>
                <TableHead>Fonte A</TableHead>
                <TableHead>Fonte B</TableHead>
                <TableHead>Diferença %</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell>Nascidos vivos</TableCell>
                <TableCell>1020</TableCell>
                <TableCell>1000</TableCell>
                <TableCell>+2,0%</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>Óbitos gerais</TableCell>
                <TableCell>520</TableCell>
                <TableCell>515</TableCell>
                <TableCell>+1,0%</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </div>
    </section>
  )
}

