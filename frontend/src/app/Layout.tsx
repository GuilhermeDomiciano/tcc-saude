import { PropsWithChildren, useEffect, useState } from 'react'

export function Layout({ children }: PropsWithChildren) {
  return (
    <div className="min-h-svh bg-background text-foreground">
      <Header />
      <NavBar />
      <main className="mx-auto max-w-6xl p-4 print:p-0">
        <div className="print-container rounded-lg bg-card p-4 shadow-sm print:shadow-none print:bg-white">
          {children}
        </div>
      </main>
    </div>
  )
}

function Header() {
  return (
    <header className="no-print sticky top-0 z-10 border-b bg-background/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 p-4">
        <h1 className="text-lg font-semibold">Saúde RDQA/RAG</h1>
        <ApiKeyField />
      </div>
    </header>
  )
}

function NavBar() {
  const linkCls =
    'text-sm text-muted-foreground hover:text-foreground transition-colors'
  return (
    <nav className="no-print border-b">
      <div className="mx-auto max-w-6xl p-3 flex flex-wrap gap-4">
        <a className={linkCls} href="/">Dashboard</a>
        <a className={linkCls} href="/tempo">Tempo</a>
        <a className={linkCls} href="/territorios">Territórios</a>
        <a className={linkCls} href="/pop-faixa">Pop. Faixa</a>
        <a className={linkCls} href="/unidades">Unidades</a>
        <a className={linkCls} href="/equipes">Equipes</a>
        <a className={linkCls} href="/fontes">Fontes</a>
        <a className={linkCls} href="/rdqa">RDQA</a>
      </div>
    </nav>
  )
}

function ApiKeyField() {
  const [key, setKey] = useState('')
  useEffect(() => {
    const k = localStorage.getItem('apiKey') || ''
    setKey(k)
  }, [])
  const onChange = (v: string) => {
    setKey(v)
    localStorage.setItem('apiKey', v)
  }
  return (
    <label className="flex items-center gap-2 text-sm">
      <span className="text-muted-foreground">X-API-Key</span>
      <input
        aria-label="X-API-Key"
        value={key}
        onChange={(e) => onChange(e.target.value)}
        placeholder="opcional"
        className="w-56 rounded-md border bg-background px-2 py-1 text-sm outline-none focus:ring-2 focus:ring-ring"
      />
    </label>
  )
}

export default Layout

