import clsx from 'clsx'
import { Badge } from '@/components/ui/badge'

export type ProvenanceBadgesProps = {
  fonte?: string
  periodo?: string
  versao?: string
  className?: string
}

export function ProvenanceBadges({ fonte, periodo, versao, className }: ProvenanceBadgesProps) {
  const hasAny = !!(fonte || periodo || versao)
  if (!hasAny) return <span className="text-xs text-muted-foreground">—</span>
  return (
    <span
      className={clsx('flex flex-wrap gap-1.5', className)}
      aria-label={`Proveniência${fonte ? `, fonte ${fonte}` : ''}${periodo ? `, período ${periodo}` : ''}${versao ? `, versão ${versao}` : ''}`}
    >
      {fonte ? <Badge><span className="text-muted-foreground">fonte</span>&nbsp;<strong>{fonte}</strong></Badge> : null}
      {periodo ? <Badge><span className="text-muted-foreground">período</span>&nbsp;<strong>{periodo}</strong></Badge> : null}
      {versao ? <Badge><span className="text-muted-foreground">versão</span>&nbsp;<strong>{versao}</strong></Badge> : null}
    </span>
  )
}

export default ProvenanceBadges
