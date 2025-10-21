import clsx from 'clsx'

export type ProvenanceBadgesProps = {
  fonte?: string
  periodo?: string
  versao?: string
  className?: string
}

export function ProvenanceBadges({ fonte, periodo, versao, className }: ProvenanceBadgesProps) {
  const hasAny = !!(fonte || periodo || versao)
  if (!hasAny) return <span className="text-xs text-muted-foreground">—</span>
  const badge = 'inline-flex items-center gap-1 rounded border px-1.5 py-0.5 text-[11px] text-foreground/80 bg-secondary/40'
  return (
    <span className={clsx('flex flex-wrap gap-1.5', className)}>
      {fonte ? <span className={badge}><span className="text-muted-foreground">fonte</span><strong>{fonte}</strong></span> : null}
      {periodo ? <span className={badge}><span className="text-muted-foreground">período</span><strong>{periodo}</strong></span> : null}
      {versao ? <span className={badge}><span className="text-muted-foreground">versão</span><strong>{versao}</strong></span> : null}
    </span>
  )
}

export default ProvenanceBadges

