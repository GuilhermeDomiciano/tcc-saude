import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

const exemploResposta = `{
  "exec_id": "2025.Q3-042",
  "status": "concluido",
  "gerado_em": "2025-10-02T10:32:14Z",
  "hash_sha256": "4d3f8a12f47c6c109b3a912c2f78b66a4a9aa7d9c2a3e940b87c90df6109a812",
  "arquivos": [
    {
      "tipo": "rdqa_pdf",
      "url": "https://api.rdqa.gov.br/execucoes/2025.Q3-042/rdqa.pdf"
    },
    {
      "tipo": "rag_planilha",
      "url": "https://api.rdqa.gov.br/execucoes/2025.Q3-042/rag.xlsx"
    }
  ]
}`

export default function ExecAudit() {
  return (
    <section className="space-y-6">
      <header className="space-y-2">
        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Audit trail</p>
        <h2 className="text-2xl font-semibold tracking-tight">Consulta publica de Exec-ID</h2>
      </header>

      <div className="rounded-2xl border bg-card shadow-sm ring-1 ring-border/40">
        <div className="border-b px-5 py-4">
          <div className="flex items-center gap-3">
            <Badge variant="outline" className="font-mono text-xs uppercase border-primary/60 text-primary">
              get
            </Badge>
            <code className="text-sm font-mono">/execucoes/&lt;exec-id&gt;</code>
          </div>
          <p className="mt-2 text-sm text-muted-foreground">
            Endpoint publico para verificar hash, status e artefatos de uma execucao registrada.
          </p>
        </div>

        <div className="grid gap-6 p-5 lg:grid-cols-[320px_1fr]">
          <div className="space-y-4 rounded-xl border bg-muted/40 p-4">
            <h3 className="text-sm font-semibold tracking-tight">Parametros</h3>
            <div className="space-y-2 text-sm">
              <label className="flex flex-col gap-1">
                <span className="font-medium text-muted-foreground">Exec-ID</span>
                <Input value="2025.Q3-042" readOnly />
              </label>
              <p className="text-xs text-muted-foreground">
                Use este valor sintese para o print. Dados sao ficticios, apenas para ilustrar a auditoria.
              </p>
            </div>
            <Button className="w-full" variant="default">Consultar</Button>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold tracking-tight">Resposta 200 OK</h3>
              <Badge variant="outline" className="border-sky-500/60 text-sky-600 dark:text-sky-300">
                JSON
              </Badge>
            </div>
            <pre className="overflow-auto rounded-xl border bg-muted/30 p-4 text-xs leading-relaxed shadow-inner">
              {exemploResposta}
            </pre>
          </div>
        </div>
      </div>
    </section>
  )
}
