import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

const summaryCards = [
  { label: 'Mortalidade geral', value: '7,3 por mil', trend: '+0,4 vs. ultimo quadrimestre' },
  { label: 'Incidencia de agravos', value: '218 por 100 mil', trend: '-12% em relacao a 2024.Q2' },
  { label: 'Despesa executada', value: 'R$ 18,6 mi', trend: 'Cobertura 94% do orcado' },
  { label: 'Cobertura APS', value: '88,5%', trend: '+1,2 p.p. em 12 meses' },
]

const evolucaoSerie = [
  { label: '2024.Q3', value: 6.8 },
  { label: '2024.Q4', value: 7.1 },
  { label: '2025.Q1', value: 7.4 },
  { label: '2025.Q2', value: 7.0 },
  { label: '2025.Q3', value: 7.3 },
]

const heatmapSeries = [
  { label: 'Setor Norte', value: 0.82 },
  { label: 'Setor Sul', value: 0.65 },
  { label: 'Centro', value: 0.91 },
  { label: 'Zona Rural', value: 0.56 },
  { label: 'Distrito A', value: 0.74 },
  { label: 'Distrito B', value: 0.68 },
]

const financeiroSeries = [
  { label: 'Autorizado', value: 19.8 },
  { label: 'Empenhado', value: 18.9 },
  { label: 'Pago', value: 18.6 },
]

const sections = [
  {
    title: 'Evolucao quadrimestral',
    description: 'Indicador de mortalidade geral com linha de tendencia e marcadores por trimestre.',
    gradient: 'from-sky-500/20 to-sky-500/5',
    chart: <MiniLineChart data={evolucaoSerie} />,
  },
  {
    title: 'Mapa de situacao',
    description: 'Heatmap por territorio destacando score combinado de mortalidade infantil, cobertura vacinal e producao.',
    gradient: 'from-emerald-500/20 to-emerald-500/5',
    chart: <MiniHeatGrid data={heatmapSeries} />,
  },
  {
    title: 'Painel financeiro',
    description: 'Comparativo de despesa autorizada, empenhada e paga no quadrimestre corrente.',
    gradient: 'from-amber-500/20 to-amber-500/5',
    chart: <MiniBarChart data={financeiroSeries} />,
  },
]

export default function Dashboard() {
  return (
    <section className="space-y-8">
      <header className="space-y-2">
        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Visao geral</p>
        <h2 className="text-2xl font-semibold tracking-tight">RDQA / RAG</h2>
      </header>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {summaryCards.map((card) => (
          <article
            key={card.label}
            className="rounded-xl border bg-card/60 p-4 shadow-sm ring-1 ring-border/40 backdrop-blur"
          >
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">{card.label}</p>
            <p className="mt-2 text-2xl font-semibold">{card.value}</p>
            <p className="mt-1 text-xs text-emerald-600 dark:text-emerald-400">{card.trend}</p>
          </article>
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        {sections.map((section) => (
          <section
            key={section.title}
            className="relative overflow-hidden rounded-2xl border bg-card shadow-sm ring-1 ring-border/40"
          >
            <div className={cn('absolute inset-0 bg-linear-to-br', section.gradient)} aria-hidden />
            <div className="relative space-y-4 p-6">
              <div className="space-y-2">
                <h3 className="text-base font-semibold">{section.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{section.description}</p>
              </div>
              <div>{section.chart}</div>
            </div>
          </section>
        ))}
      </div>

      <div className="flex flex-col items-start gap-4 rounded-2xl border bg-muted/40 p-6 shadow-inner lg:flex-row lg:items-center lg:justify-between">
        <div className="space-y-1">
          <h3 className="text-lg font-semibold">Exportacao automatica</h3>
          <p className="text-sm text-muted-foreground max-w-xl leading-relaxed">
            Gere os quadros do RDQA e RAG com registro do Exec-ID e assinatura SHA-256 para rastreabilidade.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button size="lg" variant="default">Exportar RDQA</Button>
          <Button size="lg" variant="secondary">Exportar RAG</Button>
          <Button size="lg" variant="outline">Compartilhar link</Button>
        </div>
      </div>
    </section>
  )
}

type LinePoint = { label: string; value: number }

function MiniLineChart({ data }: { data: LinePoint[] }) {
  const width = 280
  const height = 140
  const margin = 16
  const values = data.map((d) => d.value)
  const min = Math.min(...values)
  const max = Math.max(...values)
  const range = max - min || 1
  const innerWidth = width - margin * 2
  const innerHeight = height - margin * 2
  const coords = data.map((point, index) => {
    const ratio = data.length > 1 ? index / (data.length - 1) : 0
    const x = margin + ratio * innerWidth
    const y = margin + (1 - (point.value - min) / range) * innerHeight
    return { ...point, x, y }
  })
  const linePath = coords
    .map((coord, index) => `${index === 0 ? 'M' : 'L'}${coord.x.toFixed(1)},${coord.y.toFixed(1)}`)
    .join(' ')
  const areaPath = [
    `M${coords[0]?.x.toFixed(1) ?? margin},${height - margin}`,
    ...coords.map((coord) => `L${coord.x.toFixed(1)},${coord.y.toFixed(1)}`),
    `L${coords.at(-1)?.x.toFixed(1) ?? margin},${height - margin}`,
    'Z',
  ].join(' ')

  return (
    <div className="space-y-3">
      <svg viewBox={`0 0 ${width} ${height}`} className="w-full">
        <defs>
          <linearGradient id="line-area" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor="rgba(14,165,233,0.35)" />
            <stop offset="100%" stopColor="rgba(14,165,233,0)" />
          </linearGradient>
        </defs>
        <rect
          x={margin}
          y={margin}
          width={innerWidth}
          height={innerHeight}
          rx={12}
          className="fill-muted/40 stroke-border/60"
        />
        <path d={areaPath} fill="url(#line-area)" />
        <path d={linePath} fill="none" stroke="rgb(2,132,199)" strokeWidth={2.5} strokeLinecap="round" />
        {coords.map((coord) => (
          <circle key={coord.label} cx={coord.x} cy={coord.y} r={4} className="fill-sky-500 stroke-white stroke-[1.5]" />
        ))}
        <line
          x1={margin}
          y1={height - margin}
          x2={width - margin}
          y2={height - margin}
          className="stroke-border/80"
          strokeDasharray="4 4"
        />
        {coords.map((coord) => (
          <text
            key={`label-${coord.label}`}
            x={coord.x}
            y={height - margin / 2}
            textAnchor="middle"
            className="fill-muted-foreground text-[10px]"
          >
            {coord.label}
          </text>
        ))}
      </svg>
      <div className="flex items-center gap-4 text-xs text-muted-foreground">
        <span className="flex items-center gap-1">
          <span className="inline-block size-2.5 rounded-full bg-sky-500" /> Mortalidade geral
        </span>
        <span>
          Pico: {max.toFixed(1)} | Baixa: {min.toFixed(1)}
        </span>
      </div>
    </div>
  )
}

type HeatPoint = { label: string; value: number }

function MiniHeatGrid({ data }: { data: HeatPoint[] }) {
  const max = Math.max(...data.map((d) => d.value))
  const min = Math.min(...data.map((d) => d.value))
  const range = max - min || 1
  return (
    <div className="space-y-3">
      <div className="grid grid-cols-3 gap-2">
        {data.map((cell) => {
          const ratio = (cell.value - min) / range
          const lightness = 80 - ratio * 35
          return (
            <div
              key={cell.label}
              className="rounded-lg border border-emerald-500/40 p-3 shadow-sm"
              style={{ backgroundColor: `hsl(152 70% ${lightness}%)` }}
            >
              <p className="text-xs font-medium text-emerald-900/80 dark:text-emerald-50">{cell.label}</p>
              <p className="mt-2 text-lg font-semibold text-emerald-900 dark:text-emerald-100">{(cell.value * 100).toFixed(0)}%</p>
              <p className="text-[10px] text-emerald-900/70 dark:text-emerald-200">score composto</p>
            </div>
          )
        })}
      </div>
      <div className="flex items-center gap-2 text-xs text-muted-foreground">
        <span className="inline-flex h-2 w-10 rounded-full bg-emerald-200" aria-hidden />
        <span className="inline-flex h-2 w-10 rounded-full bg-emerald-500" aria-hidden />
        <span className="inline-flex h-2 w-10 rounded-full bg-emerald-700" aria-hidden />
        <span className="text-xs">Menor cobertura → Maior cobertura</span>
      </div>
    </div>
  )
}

type FinancePoint = { label: string; value: number }

function MiniBarChart({ data }: { data: FinancePoint[] }) {
  const max = Math.max(...data.map((d) => d.value))
  return (
    <div className="space-y-3">
      <div className="space-y-3">
        {data.map((item) => (
          <div key={item.label} className="flex items-center gap-3">
            <span className="w-24 text-xs font-medium text-muted-foreground">{item.label}</span>
            <div className="relative h-3 flex-1 rounded-full bg-muted">
              <div
                className="absolute inset-y-0 left-0 rounded-full bg-amber-500/80"
                style={{ width: `${(item.value / max) * 100}%` }}
              />
            </div>
            <span className="w-20 text-right text-xs font-semibold text-foreground">
              {item.value.toFixed(1)} mi
            </span>
          </div>
        ))}
      </div>
      <div className="text-xs text-muted-foreground">
        Execucao orcamentaria consolidada para o quadrimestre atual.
      </div>
    </div>
  )
}
