# Plano de Implementação do MVP (Frontend)

Objetivo: interface web para cadastrar e consultar dimensões analíticas (Tempo, Território, População por Faixa/Sexo, Unidade, Equipe, Fonte). Consumir a API do backend (VITE_API_BASE) e exigir X-API-Key apenas para escrita quando configurado.

## 1) Fundações e Ambiente
- [ ] Definir `VITE_API_BASE` em `.env` (ex.: `http://localhost:8000`).
- [ ] Instalar deps: `npm i` (adicionar se faltar: `react-router-dom`, `axios`, `zod`, `@tanstack/react-query`, `@tanstack/react-table`).
- [ ] Estrutura base `src/`: `app/` (rotas/layout), `components/` (UI), `features/` (cada dimensão), `lib/` (api, utils), `styles/`.

## 2) Estilos e Layout
- [ ] Garantir Tailwind ativo (global.css com `@tailwind base; @tailwind components; @tailwind utilities;`).
- [ ] Criar layout padrão: header (título, campo X-API-Key opcional), navbar (links), container.

## 3) Cliente de API e Tipos
- [ ] `src/lib/api.ts`: axios com `baseURL`=`import.meta.env.VITE_API_BASE`, interceptor para `X-API-Key` (se presente no storage).
- [ ] Tipos TS alinhados aos DTOs do backend (Out/Create/Update) por dimensão.

## 4) Roteamento
- [ ] `react-router-dom` com rotas:
  - `/` (dashboard simples), `/tempo`, `/territorios`, `/pop-faixa`, `/unidades`, `/equipes`, `/fontes`.

## 5) Listas (GET)
- [ ] Para cada rota, página com:
  - Tabela (React Table) com paginação (`limit/offset`) e filtros (ex.: ano/mês em Tempo; UF/IBGE em Território; território/ano em Pop-Faixa).
  - Botões: “Novo”, “Editar”, “Excluir”.
  - Estados de carregando/erro (React Query: `useQuery`).

## 6) Formulários (POST/PUT)
- [ ] Modal/Form por dimensão (Zod + React Hook Form): validações (UF 2 chars, IBGE 6–7 dígitos, datas ISO, população ≥ 0…).
- [ ] Enviar `X-API-Key` no cabeçalho quando definido (ler de um campo no header e salvar em `localStorage`).
- [ ] Após sucesso, invalidar queries (React Query) e fechar modal.

## 7) Exclusão (DELETE)
- [ ] Diálogo de confirmação → DELETE → refetch da lista.

## 8) UX e A11y
- [ ] Focus management nos modais, labels/aria, toasts de feedback (sucesso/erro) simples.
- [ ] Máscaras/helps para datas e IBGE.

## 9) Testes
- [ ] Vitest + Testing Library: testes de páginas de lista (render, loading, empty), e formulários (validação, submit feliz/erro).
- [ ] Mocks de API com MSW (opcional) ou axios-mock-adapter.

## 10) Build & Entrega
- [ ] `npm run build` (garantir `VITE_API_BASE` em `.env` de prod).
- [ ] Dockerfile: servir build com `vite preview` ou nginx (se contêinerizar).
- [ ] Documentar no README do frontend: variáveis, comandos, rotas e exemplos.
