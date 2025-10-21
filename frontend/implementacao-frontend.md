# Plano de Implementação do MVP (Frontend)

Objetivo: interface web para cadastrar e consultar dimensões analíticas (Tempo, Território, População por Faixa/Sexo, Unidade, Equipe, Fonte) e publicar Quadros RDQA com exportação em PDF e proveniência. Consumir a API do backend (`VITE_API_BASE`) e exigir `X-API-Key` apenas para escrita quando configurado.

## 1) Fundações e Ambiente
- [x] Definir `VITE_API_BASE` em `.env` (ex.: `http://localhost:8000`).
- [x] Instalar deps: `npm i` (adicionar se faltar: `react-router-dom`, `axios`, `zod`, `@tanstack/react-query`, `@tanstack/react-table`, `react-hook-form`).
- [x] UI kit: `shadcn/ui` (ou equivalente) para componentes acessíveis e consistentes.
- [x] Utilitários: `qrcode` (ou `qrcode.react`) para QR Code nos PDFs; `date-fns` para datas.
- [x] Estrutura base `src/`: `app/` (rotas/layout), `components/` (UI), `features/` (cada dimensão), `lib/` (api, utils), `styles/`, `pages/rdqa/` (quadros e exportação).

## 2) Estilos e Layout
- [x] Garantir Tailwind ativo (global.css com `@tailwind base; @tailwind components; @tailwind utilities;`).
- [x] Criar layout padrão: header (título, campo `X-API-Key` opcional), navbar (links), container.
- [x] Estilos de impressão para PDF: layout A4, margens, classes utilitárias `print:*`, ocultar elementos não imprimíveis.

## 3) Cliente de API e Tipos
- [x] `src/lib/api.ts`: axios com `baseURL`=`import.meta.env.VITE_API_BASE`, interceptor para `X-API-Key` (se presente em `localStorage`).
- [x] Tipos TS alinhados aos DTOs do backend (Out/Create/Update) por dimensão.
- [x] Metadados de proveniência: estender tipos para exibir `fonte`, `periodo`, `versao` e, se disponível, `hash`/`exec_id`.
 - [x] Exportador RDQA: helper para `POST /rdqa/export/pdf` aceitando `{ html?: string, url?: string, format?: 'A4', margin_mm?: number }`, retornando `Blob` e lendo headers `X-Exec-Id`/`X-Hash` para o QR.

## 4) Roteamento
- [x] `react-router-dom` com rotas:
  - `/` (dashboard simples), `/tempo`, `/territorios`, `/pop-faixa`, `/unidades`, `/equipes`, `/fontes`.
  - `/rdqa` (hub dos quadros) e sub-rotas por quadro (ex.: `/rdqa/consistencia`, `/rdqa/cobertura`).

## 5) Listas (GET)
- [x] Para cada rota, página com:
  - Tabela (React Table) com paginação (`limit/offset`) e filtros (ex.: ano/mês em Tempo; UF/IBGE em Território; território/ano em Pop-Faixa).
  - Estados de carregando/erro (React Query: `useQuery`).
- [x] Badges de proveniência nos cards/tabelas (exibir `fonte/periodo/versao`).

## 6) Formulários (POST/PUT)
- [x] Modal/Form por dimensão (Zod + React Hook Form): validações (UF 2 chars, IBGE 6–7 dígitos, datas ISO, população ≥ 0). (Implementado para Tempo e Territórios)
- [x] Enviar `X-API-Key` no cabeçalho quando definido (ler de um campo no header e salvar em `localStorage`).
- [x] Após sucesso, invalidar queries (React Query) e fechar modal.

## 7) Exclusão (DELETE)
- [x] Diálogo de confirmação → DELETE → refetch da lista. (Implementado com botão de exclusão por ID nas listas)

## 8) RDQA: Páginas e Exportação
- [x] Criar páginas dos Quadros RDQA com layout de impressão (A4) e variações por período/município.
- [x] Exportação em PDF com QR Code de verificação:
  - Opção A (recomendada): chamar endpoint do backend `POST /rdqa/export/pdf` (Pyppeteer) a partir do HTML da página; usar headers `X-Exec-Id`/`X-Hash` no QR.
  - Opção B (fallback): `window.print()` com estilos de impressão ou lib client-side, garantindo fidelidade mínima.
- [x] QR Code aponta para URL verificável do backend: `/public/verificar?exec_id=...&hash=...`.
- [x] Inserir metadados no rodapé (fonte/periodicidade/versão, data/hora da geração).

## 9) UX, A11y e Qualidade
- [ ] Focus management nos modais; labels/aria; navegação por teclado.
- [ ] Máscaras/ajuda para datas e IBGE.
- [ ] Estados vazios e mensagens de erro claras.
- [ ] Consistência visual com `shadcn/ui` (ou design system escolhido).

## 10) Testes
- [ ] Vitest + Testing Library: listas (render, loading, empty), formulários (validação, submit sucesso/erro).
- [ ] Testes das páginas RDQA: renderização e presença de metadados de proveniência.
- [ ] Teste de exportação PDF: mock do `POST /rdqa/export/pdf`, garantir leitura de headers `X-Exec-Id`/`X-Hash` e montagem correta do QR.
- [ ] Mocks de API com MSW (ou axios-mock-adapter).

## 11) Build & Entrega
- [ ] `npm run build` (garantir `VITE_API_BASE` em `.env` de prod).
- [ ] Dockerfile: servir build com `vite preview` ou nginx; opcionalmente integrar em `docker-compose` com backend.
- [ ] Documentar no README do frontend: variáveis, comandos, rotas e exemplos, incluindo fluxo de exportação RDQA.

## 12) Observações de alinhamento com o artigo (JIC)
- [ ] Badges de proveniência visíveis nas telas e embutidas nos PDFs (fonte/período/versão e, quando houver, `hash/exec_id`).
- [ ] QR Code nos PDFs para verificação pública do conteúdo (rastreabilidade ponta a ponta).
- [ ] Páginas RDQA compõem as figuras/tabelas do paper (prints podem ser usados como anexos).
- [ ] Estilos de impressão garantem legibilidade e aderência a A4.


