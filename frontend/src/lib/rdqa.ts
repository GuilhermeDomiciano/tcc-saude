export function buildRDQAHtml(options: {
  title: string
  contentHtml: string
  meta?: Record<string, string | number | undefined>
  qrDataUrl?: string
}) {
  const { title, contentHtml, meta = {}, qrDataUrl } = options
  const metaRows = Object.entries(meta)
    .filter(([, v]) => v !== undefined && v !== null && String(v).length > 0)
    .map(([k, v]) => `<tr><td style="padding:2px 6px;color:#555">${escapeHtml(k)}</td><td style="padding:2px 6px;"><strong>${escapeHtml(String(v))}</strong></td></tr>`) 
    .join('')
  return `<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>${escapeHtml(title)}</title>
  <style>
    @page { size: A4; margin: 12mm; }
    body { font-family: ui-sans-serif,system-ui; color: #111; }
    h1 { font-size: 18px; margin: 0 0 8px; }
    .muted { color: #666; font-size: 12px; }
    .card { border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; }
    .row { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
    table.meta { border-collapse: collapse; font-size: 12px; }
    table.meta td { border-bottom: 1px solid #eee; }
  </style>
</head>
<body>
  <div class="row">
    <div>
      <h1>${escapeHtml(title)}</h1>
      <div class="muted">Gerado via RDQA Export</div>
      ${metaRows ? `<table class="meta">${metaRows}</table>` : ''}
    </div>
    ${qrDataUrl ? `<img alt="QR" src="${qrDataUrl}" width="96" height="96" />` : ''}
  </div>
  <div style="height:8px"></div>
  <div class="card">
    ${contentHtml}
  </div>
</body>
</html>`
}

function escapeHtml(s: string) {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

