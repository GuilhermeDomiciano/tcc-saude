import { isRouteErrorResponse, useRouteError } from 'react-router-dom'
import { Button } from '@/components/ui/button'

export default function ErrorPage() {
  const error = useRouteError()
  const status = isRouteErrorResponse(error) ? error.status : 500
  const message = isRouteErrorResponse(error) ? error.statusText : (error as Error)?.message || 'Erro desconhecido'
  return (
    <div className="mx-auto max-w-xl p-6">
      <h1 className="text-xl font-semibold mb-2">Ocorreu um erro</h1>
      <p className="text-sm text-muted-foreground mb-4">{status} — {message}</p>
      <div className="flex gap-2">
        <Button onClick={() => location.reload()}>Recarregar</Button>
        <Button variant="outline" onClick={() => history.back()}>Voltar</Button>
      </div>
    </div>
  )
}

