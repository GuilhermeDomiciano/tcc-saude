import { Link } from 'react-router-dom'

export default function RdqaIndex() {
  return (
    <section className="prose max-w-none dark:prose-invert">
      <h2>RDQA</h2>
      <p>Selecione um quadro para visualização/exportação:</p>
      <ul>
        <li><Link to="/rdqa/consistencia">Consistência</Link></li>
        <li><Link to="/rdqa/cobertura">Cobertura</Link></li>
      </ul>
    </section>
  )
}

