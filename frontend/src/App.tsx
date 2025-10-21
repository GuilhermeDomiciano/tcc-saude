import './App.css'
import Layout from './app/Layout'

function App() {
  return (
    <Layout>
      <div className="prose max-w-none dark:prose-invert">
        <h2>Bem-vindo</h2>
        <p>Estrutura de layout pronta. Use a navbar para navegar.</p>
        <p className="no-print text-xs text-muted-foreground">
          Dica: defina sua <span className="font-semibold">X-API-Key</span> no topo se o backend exigir escrita.
        </p>
      </div>
    </Layout>
  )
}

export default App
