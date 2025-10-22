import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'

export default function RagIndex() {
  const cards = [
    {
      title: 'Resumo executivo',
      description: 'Indicadores consolidados de execucao financeira, producao e metas.',
      to: '/rag/resumo',
    },
    {
      title: 'Financeiro',
      description: 'Detalhes de dotacao, receita, empenho, liquidacao e pagamento.',
      to: '/rag/financeiro',
    },
    {
      title: 'Producao assistencial',
      description: 'Volumes consolidados por tipo de servico e territorio.',
      to: '/rag/producao',
    },
    {
      title: 'Metas e resultados',
      description: 'Comparativo meta planejada x executada com status de cumprimento.',
      to: '/rag/metas',
    },
  ]

  return (
    <section className="space-y-4">
      <div className="prose max-w-none dark:prose-invert">
        <h2>RAG</h2>
        <p>Selecione um quadro para visualizar os indicadores do Relatorio Anual de Gestao e exportar os PDFs com QR Code.</p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {cards.map((card) => (
          <div key={card.to} className="rounded-lg border bg-card p-4">
            <h3 className="text-base font-semibold mb-1">{card.title}</h3>
            <p className="text-sm text-muted-foreground mb-3">{card.description}</p>
            <Button asChild>
              <Link to={card.to}>Abrir</Link>
            </Button>
          </div>
        ))}
      </div>
    </section>
  )
}
