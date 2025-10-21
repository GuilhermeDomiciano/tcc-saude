import { createBrowserRouter } from 'react-router-dom'
import Layout from './Layout'
import Dashboard from '../pages/Dashboard'
import Tempo from '../pages/Tempo'
import Territorios from '../pages/Territorios'
import PopFaixa from '../pages/PopFaixa'
import Unidades from '../pages/Unidades'
import Equipes from '../pages/Equipes'
import Fontes from '../pages/Fontes'
import RdqaIndex from '../pages/rdqa/Index'
import RdqaConsistencia from '../pages/rdqa/Consistencia'
import RdqaCobertura from '../pages/rdqa/Cobertura'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'tempo', element: <Tempo /> },
      { path: 'territorios', element: <Territorios /> },
      { path: 'pop-faixa', element: <PopFaixa /> },
      { path: 'unidades', element: <Unidades /> },
      { path: 'equipes', element: <Equipes /> },
      { path: 'fontes', element: <Fontes /> },
      {
        path: 'rdqa',
        children: [
          { index: true, element: <RdqaIndex /> },
          { path: 'consistencia', element: <RdqaConsistencia /> },
          { path: 'cobertura', element: <RdqaCobertura /> },
        ],
      },
    ],
  },
])

export default router

