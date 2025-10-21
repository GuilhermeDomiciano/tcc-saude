import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'

export default function RdqaIndex() {
  const cards = [
    {
      title: 'Consistência',
      description: 'Comparação entre fontes (ex.: SIM × SINASC) com deltas e MAPE.',
      to: '/rdqa/consistencia',
    },
    {
      title: 'Cobertura',
      description: 'Evolução de cobertura por equipe/tempo, com filtros por período.',
      to: '/rdqa/cobertura',
    },
  ]
  return (
    <section className="space-y-4">
      <div className="prose max-w-none dark:prose-invert">
        <h2>RDQA</h2>
        <p>Escolha um quadro para visualizar, filtrar e exportar em PDF.</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {cards.map((c) => (
          <div key={c.to} className="rounded-lg border p-4 bg-card">
            <h3 className="text-base font-semibold mb-1">{c.title}</h3>
            <p className="text-sm text-muted-foreground mb-3">{c.description}</p>
            <Button asChild>
              <Link to={c.to}>Abrir</Link>
            </Button>
          </div>
        ))}
      </div>
    </section>
  )
}

