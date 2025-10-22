import { useEffect, useRef, useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import { Button } from '@/components/ui/button'

export function Layout() {
  return (
    <div className="min-h-svh bg-background text-foreground">
      <a href="#conteudo" className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2 focus:z-50 focus:rounded-md focus:bg-primary focus:px-3 focus:py-1.5 focus:text-primary-foreground">Pular para o conteúdo</a>
      <Header />
      <NavBar />
      <main id="conteudo" className="mx-auto max-w-6xl p-4 print:p-0">
        <div className="print-container rounded-lg bg-card p-4 shadow-sm print:shadow-none print:bg-white">
          <Outlet />
        </div>
      </main>
    </div>
  )
}

function Header() {
  return (
    <header className="no-print sticky top-0 z-10 border-b bg-background/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 p-3">
        <div className="flex items-center gap-3">
          <div aria-hidden className="size-8 rounded-md bg-primary/10 text-primary flex items-center justify-center font-bold">RD</div>
          <h1 className="text-base sm:text-lg font-semibold tracking-tight">Plataforma RDQA/RAG</h1>
        </div>
        <ApiKeyField />
      </div>
    </header>
  )
}

function NavBar() {
  const linkBase = 'text-sm transition-colors px-2.5 py-1.5 rounded-md focus:outline-none focus-visible:ring-2 focus-visible:ring-ring'
  const linkInactive = 'text-muted-foreground hover:text-foreground hover:bg-accent'
  const linkActive = 'bg-primary text-primary-foreground hover:bg-primary/90'
  return (
    <nav className="no-print border-b">
      <div className="mx-auto max-w-6xl p-2 flex flex-wrap gap-2">
        {[
          { to: '/', label: 'Dashboard' },
          { to: '/tempo', label: 'Tempo' },
          { to: '/territorios', label: 'Territórios' },
          { to: '/pop-faixa', label: 'Pop. Faixa' },
          { to: '/unidades', label: 'Unidades' },
          { to: '/equipes', label: 'Equipes' },
          { to: '/fontes', label: 'Fontes' },
          { to: '/rdqa', label: 'RDQA' },
          { to: '/rag', label: 'RAG' },
        ].map((i) => (
          <NavLink
            key={i.to}
            to={i.to}
            className={({ isActive }: { isActive: boolean }) => [linkBase, isActive ? linkActive : linkInactive].join(' ')}
          >
            {i.label}
          </NavLink>
        ))}
      </div>
    </nav>
  )
}

function ApiKeyField() {
  const [key, setKey] = useState('')
  const inputRef = useRef<HTMLInputElement | null>(null)
  useEffect(() => {
    const k = localStorage.getItem('apiKey') || ''
    setKey(k)
  }, [])
  const onChange = (v: string) => {
    setKey(v)
    localStorage.setItem('apiKey', v)
  }
  return (
    <div className="flex items-center gap-2 text-sm">
      <label htmlFor="api-key" className="text-muted-foreground">X-API-Key</label>
      <input
        id="api-key"
        ref={inputRef}
        value={key}
        onChange={(e) => onChange(e.target.value)}
        placeholder="opcional"
        className="w-56 rounded-md border bg-background px-2 py-1 text-sm outline-none focus:ring-2 focus:ring-ring"
      />
      {key && (
        <Button variant="ghost" size="sm" aria-label="Limpar API Key" onClick={() => { onChange(''); inputRef.current?.focus() }}>Limpar</Button>
      )}
    </div>
  )
}

export default Layout
