import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

type RegistroIngestao = {
  id: string
  fonte: string
  periodo: string
  versao: string
  status: 'Validado' | 'Pendente' | 'Erro'
  registros: string
  execId: string
  checksum: string
}

const registros: RegistroIngestao[] = [
  {
    id: 'IBGE_POP_2025',
    fonte: 'IBGE - Populacao',
    periodo: '2014-2025',
    versao: 'v2025-09',
    status: 'Validado',
    registros: '3 planilhas normalizadas',
    execId: '2025.Q3-042',
    checksum: '7d61:9fb0:fa21',
  },
  {
    id: 'SINASC_NASCIDOS',
    fonte: 'SINASC',
    periodo: '2022.Q1-2025.Q3',
    versao: '2025-09-10',
    status: 'Pendente',
    registros: 'Upload aguardando validacao',
    execId: 'pendente',
    checksum: 'pendente',
  },
  {
    id: 'SIOPS_FIN',
    fonte: 'SIOPS / SIAF',
    periodo: '2024.Q1-2025.Q2',
    versao: 'liberado em 02/09',
    status: 'Validado',
    registros: 'ETL finalizada, 48.231 linhas',
    execId: '2025.Q3-041',
    checksum: 'c28f:21b0:ad77',
  },
  {
    id: 'PNI_IMUNIZACOES',
    fonte: 'PNI / LocalizaSUS',
    periodo: '2025.Q1-Q3',
    versao: 'snapshot 18/09',
    status: 'Erro',
    registros: 'Falha no schema: coluna dose_ref ausente',
    execId: 'erro',
    checksum: 'erro',
  },
]

const statusStyles: Record<RegistroIngestao['status'], { variant: 'default' | 'outline'; className?: string }> = {
  Validado: { variant: 'default', className: 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border-emerald-500/40' },
  Pendente: { variant: 'outline', className: 'border-amber-500/60 text-amber-600 dark:text-amber-300' },
  Erro: { variant: 'outline', className: 'border-red-500/60 text-red-600 dark:text-red-400' },
}

export default function Ingestao() {
  return (
    <section className="space-y-6">
      <header className="space-y-2">
        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Pipeline etapa 1</p>
        <h2 className="text-2xl font-semibold tracking-tight">Ingestão e integração das fontes</h2>
      </header>

      <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border bg-card/60 p-4 shadow-sm">
        <div>
          <p className="text-sm text-muted-foreground">Ultima execução concluída</p>
          <p className="font-semibold">Exec-ID 2025.Q3-042 - hash 7d61:9fb0:fa21</p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline">Carregar nova base</Button>
          <Button variant="secondary">Validar lote</Button>
        </div>
      </div>

      <div className="rounded-2xl border bg-card shadow-sm ring-1 ring-border/40">
        <Table>
          <TableCaption>
            Dados meramente ilustrativos para compor o print da ingestao.
          </TableCaption>
          <TableHeader>
            <TableRow className="bg-muted">
              <TableHead className="w-40">Fonte</TableHead>
              <TableHead>Periodo</TableHead>
              <TableHead>Versao</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Registros</TableHead>
              <TableHead className="w-[180px]">Exec-ID</TableHead>
              <TableHead>Checksum</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {registros.map((registro) => (
              <TableRow
                key={registro.id}
                className={registro.status === 'Validado' ? 'border-l-4 border-l-emerald-500/70 bg-emerald-500/5' : undefined}
              >
                <TableCell className="font-medium">{registro.fonte}</TableCell>
                <TableCell>{registro.periodo}</TableCell>
                <TableCell>{registro.versao}</TableCell>
                <TableCell>
                  <Badge variant={statusStyles[registro.status].variant} className={statusStyles[registro.status].className}>
                    {registro.status}
                  </Badge>
                </TableCell>
                <TableCell>{registro.registros}</TableCell>
                <TableCell>{registro.execId}</TableCell>
                <TableCell>{registro.checksum}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </section>
  )
}
