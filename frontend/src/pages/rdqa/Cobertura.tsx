import { useRef, useState } from 'react'
import { exportRDQAPdf } from '../../lib/api'
import { buildRDQAHtml } from '../../lib/rdqa'
import QRCode from 'qrcode'

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
      const initialHtml = buildRDQAHtml({ title: 'Quadro RDQA — Cobertura', contentHtml, meta: { territorioId, periodo } })
      let { blob, execId, hash } = await exportRDQAPdf({ html: initialHtml, format: 'A4', margin_mm: 12 })
      if (execId && hash) {
        const verifyUrl = `${import.meta.env.VITE_API_BASE}/public/verificar?exec_id=${encodeURIComponent(execId)}&hash=${encodeURIComponent(hash)}`
        const qrDataUrl = await QRCode.toDataURL(verifyUrl)
        const withQrHtml = buildRDQAHtml({ title: 'Quadro RDQA — Cobertura', contentHtml, meta: { territorioId, periodo }, qrDataUrl })
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
      </div>

      <div className="no-print flex flex-wrap items-end gap-3">
        <label className="text-sm">
          <span className="block text-muted-foreground">Território ID</span>
          <input className="w-40 rounded-md border bg-background px-2 py-1" value={territorioId} onChange={(e) => setTerritorioId(e.target.value)} placeholder="Ex.: 1" />
        </label>
        <label className="text-sm">
          <span className="block text-muted-foreground">Período</span>
          <input className="w-64 rounded-md border bg-background px-2 py-1" value={periodo} onChange={(e) => setPeriodo(e.target.value)} placeholder="Ex.: 2024-01 a 2024-12" />
        </label>
        <button onClick={onExport} disabled={loading} className="rounded-md border bg-primary px-3 py-1 text-sm text-primary-foreground">
          {loading ? 'Gerando...' : 'Exportar PDF'}
        </button>
      </div>

      <div ref={contentRef} id="rdqa-print" className="prose max-w-none dark:prose-invert">
        <h3>Quadro de Cobertura (exemplo)</h3>
        <table>
          <thead>
            <tr>
              <th>Tempo</th>
              <th>Equipe</th>
              <th>Cobertura %</th>
            </tr>
          </thead>
        <tbody>
          <tr>
            <td>2024-01</td>
            <td>ESF 01</td>
            <td>72,3%</td>
          </tr>
          <tr>
            <td>2024-02</td>
            <td>ESF 01</td>
            <td>73,1%</td>
          </tr>
        </tbody>
        </table>
      </div>
    </section>
  )
}
