Figura 3 – Painel principal e interface de exportação automática
🎯 Objetivo da figura:

Demonstrar o resultado visual do pipeline no frontend — a interface onde os dados já processados aparecem em painéis e relatórios.

📌 Deve mostrar:

A tela inicial ou dashboard principal do sistema.

Um painel de indicadores (ex.: mortalidade, incidência, despesas).

Um botão ou link de “Exportar RDQA/RAG” (se houver).

Gráficos, tabelas ou widgets visuais que representem os resultados calculados.

💡 Dica:
Se o dashboard tiver filtros (por período, município, grupo populacional), capture a parte superior da tela, mostrando esses filtros visivelmente.

⚠️ Evite:

Prints com dados sensíveis ou municipais reais (se possível, use dados sintéticos).

Print de código.

🏷️ Legenda ABNT:

Figura 3 – Painel principal e interface de exportação automática do sistema.
Fonte: Elaboração própria.

🖼️ Figura 4 – Tela de ingestão e integração das fontes de dados do SUS
🎯 Objetivo da figura:

Comprovar visualmente o processo de ingestão e integração de dados de múltiplas fontes (a etapa 1 do pipeline).

📌 Deve mostrar:

A tela do backend (ou interface administrativa) onde são carregados os datasets.

Colunas ou campos como:

“Fonte” (ex.: SINASC, CNES, SIAF),

“Período” ou “Competência”,

“Versão dos dados”,

“Status da validação” (OK, erro, pendente).

Se o sistema gerar logs de execução, capture um trecho que mostre a validação de arquivos ou mensagens de importação bem-sucedida.

💡 Dica:
Coloque uma borda vermelha ou destaque visual (seta, círculo) sobre um registro validado com sucesso — isso ajuda o leitor a entender rapidamente o que está vendo.

⚠️ Evite:

Logs extensos ou códigos SQL.

Mensagens de erro técnico irrelevantes (só use se ilustram a validação).

🏷️ Legenda ABNT:

Figura 4 – Tela de ingestão e integração das fontes de dados do SUS utilizadas no pipeline.
Fonte: Elaboração própria.

🖼️ Figura 5 – Etapas do pipeline “da planilha aos painéis e relatórios”
🎯 Objetivo da figura:

Evidenciar o fluxo operacional completo, conectando todas as etapas descritas (ingestão → validação → materialização → publicação → visualização).

📌 Opção 1 – Diagrama (recomendado):

Monte um fluxograma horizontal mostrando as cinco etapas, com ícones simples e cores neutras.

📌 Opção 2 – Sequência de prints (se preferir usar telas reais):

Monte uma imagem composta (com 5 mini-telas lado a lado ou empilhadas), mostrando:

Upload do arquivo bruto (etapa de ingestão).

Log de validação (etapa de consistência).

Consulta a uma view SQL (etapa de materialização).

Chamada API (página Swagger ou resposta JSON).

Dashboard (etapa de visualização).

💡 Dica:
Use setas ou numeração (1 a 5) entre os prints, para indicar que é um processo contínuo.

⚠️ Evite:

Prints sem ordem lógica.

Dados irrelevantes (foco é no fluxo, não no conteúdo numérico).

🏷️ Legenda ABNT:

Figura 5 – Etapas do pipeline “da planilha aos painéis e relatórios”.
Fonte: Elaboração própria.

🖼️ Figura 6 – Endpoint público para consulta de Exec-ID e verificação de integridade
🎯 Objetivo da figura:

Mostrar a funcionalidade de verificação de integridade e reprodutibilidade das execuções — como o sistema permite auditar resultados.

📌 Deve mostrar:

A tela da documentação da API (Swagger ou ReDoc), exibindo o endpoint público (ex.: /execs/ ou /results/verify/).

Um exemplo de consulta real:

Campo “Exec-ID” preenchido.

Resultado JSON contendo informações como data, status, hash SHA-256 e link para download/exportação.

Se houver um botão de “Consultar” ou “Ver resultado”, capture o antes e o depois da execução.

💡 Dica:
Use dados sintéticos e destaque o Exec-ID e o hash com uma caixa colorida para chamar atenção.

⚠️ Evite:

Exibir tokens, senhas, chaves de API.

Prints de terminal/console — priorize a interface web.

🏷️ Legenda ABNT:

Figura 6 – Endpoint público para consulta de Exec-ID e verificação de integridade das execuções.
Fonte: Elaboração própria.