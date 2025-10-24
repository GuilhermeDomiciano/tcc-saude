const steps = [
  {
    numero: '1',
    titulo: 'Ingestão',
    detalhe: 'Upload dos arquivos CSV ou planilhas com registro de fonte, período e versão.',
    rota: '/ingestao',
  },
  {
    numero: '2',
    titulo: 'Validação',
    detalhe: 'Regras de consistência (domínios IBGE, chaves, datas) e logs de conferências.',
    rota: '/logs',
  },
  {
    numero: '3',
    titulo: 'Materialização',
    detalhe: 'Views SQL declarativas com metadados de numerador, denominador e período de referência.',
    rota: '/materializacao',
  },
  {
    numero: '4',
    titulo: 'Publicação API',
    detalhe: 'Endpoints REST com exec-id e hash para cada pacote de exportacao gerado.',
    rota: '/swagger',
  },
  {
    numero: '5',
    titulo: 'Visualização',
    detalhe: 'Dashboards interativos e exportação automática do RDQA e do RAG.',
    rota: '/',
  },
]

export default function Pipeline() {
  return (
    <section className="space-y-8">
      <header className="space-y-2">
        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Fluxo completo</p>
        <h2 className="text-2xl font-semibold tracking-tight">Do dado bruto aos paineis</h2>
        <p className="text-sm text-muted-foreground leading-relaxed">
          Figura 5 deve ser capturada aqui (<code className="rounded bg-muted px-1.5 py-0.5">/pipeline</code>).
          As etapas estao numeradas para montar um print sequencial que ilustra todo o pipeline.
        </p>
      </header>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
        {steps.map((step) => (
          <article
            key={step.numero}
            className="relative flex flex-col gap-3 rounded-2xl border bg-card p-5 shadow-sm ring-1 ring-border/40"
          >
            <span className="absolute -top-4 left-5 flex size-9 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground shadow-md">
              {step.numero}
            </span>
            <div className="pt-3">
              <h3 className="text-base font-semibold">{step.titulo}</h3>
              <p className="mt-1 text-sm text-muted-foreground leading-relaxed">{step.detalhe}</p>
            </div>
            {/* <div className="mt-auto text-xs text-muted-foreground">
              Rota ilustrativa: <code className="rounded bg-muted px-1 py-0.5">{step.rota}</code>
            </div> */}
          </article>
        ))}
      </div>

      <div className="rounded-xl border border-dashed border-primary/40 bg-primary/5 p-5 text-sm leading-relaxed text-primary-foreground/80 shadow-inner">
        Dica de composicao da Figura 5: capture esta tela em formato paisagem, com as cinco cartas alinhadas e as rotas
        destacadas. Opcionalmente, inclua setas ou numeracao adicional na edicao do artigo para reforcar o fluxo.
      </div>
    </section>
  )
}
