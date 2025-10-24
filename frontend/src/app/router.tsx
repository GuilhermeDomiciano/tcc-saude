import { createBrowserRouter } from 'react-router-dom'
import Layout from './Layout'
import ErrorPage from './ErrorPage'
import Dashboard from '../pages/Dashboard'
import Tempo from '../pages/Tempo'
import Territorios from '../pages/Territorios'
import PopFaixa from '../pages/PopFaixa'
import Unidades from '../pages/Unidades'
import Equipes from '../pages/Equipes'
import Fontes from '../pages/Fontes'
import Ingestao from '../pages/Ingestao'
import Pipeline from '../pages/Pipeline'
import ExecAudit from '../pages/ExecAudit'
import RdqaIndex from '../pages/rdqa/Index'
import RdqaConsistencia from '../pages/rdqa/Consistencia'
import RdqaCobertura from '../pages/rdqa/Cobertura'
import RagIndex from '../pages/rag/Index'
import RagResumo from '../pages/rag/Resumo'
import RagFinanceiro from '../pages/rag/Financeiro'
import RagProducao from '../pages/rag/Producao'
import RagMetas from '../pages/rag/Metas'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    errorElement: <ErrorPage />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'tempo', element: <Tempo /> },
      { path: 'territorios', element: <Territorios /> },
      { path: 'pop-faixa', element: <PopFaixa /> },
      { path: 'unidades', element: <Unidades /> },
      { path: 'equipes', element: <Equipes /> },
      { path: 'fontes', element: <Fontes /> },
      { path: 'ingestao', element: <Ingestao /> },
      { path: 'pipeline', element: <Pipeline /> },
      { path: 'auditoria', element: <ExecAudit /> },
      {
        path: 'rdqa',
        children: [
          { index: true, element: <RdqaIndex /> },
          { path: 'consistencia', element: <RdqaConsistencia /> },
          { path: 'cobertura', element: <RdqaCobertura /> },
        ],
      },
      {
        path: 'rag',
        children: [
          { index: true, element: <RagIndex /> },
          { path: 'resumo', element: <RagResumo /> },
          { path: 'financeiro', element: <RagFinanceiro /> },
          { path: 'producao', element: <RagProducao /> },
          { path: 'metas', element: <RagMetas /> },
        ],
      },
    ],
  },
])

export default router
