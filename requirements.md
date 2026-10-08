# Requisitos do Módulo de Recomendação (SDD)

## Requisitos Funcionais

### RF-01: Recomendação por Tipologia e Região
- **História de Usuário:** Como comprador, quero ver artesanatos similares ao visualizar uma peça, para conhecer outros itens da mesma tipologia ou polo criativo.
- **Critério de Aceitação:** QUANDO o comprador visualizar a página de uma peça artesanal, O MÓDULO DE RECOMENDAÇÃO DEVERÁ retornar até 4 produtos da mesma tipologia (ex: barro, madeira, tecido) ou do mesmo polo criativo.

### RF-02: Recomendação do Mestre Artesão
- **História de Usuário:** Como apreciador de arte, quero ver outras obras do mesmo autor ao visitar um produto, para prestigiar o trabalho do mestre.
- **Critério de Aceitação:** QUANDO o comprador acessar o detalhe de uma peça criada por um Mestre Artesão reconhecido, O MÓDULO DE RECOMENDAÇÃO DEVERÁ sugerir prioritariamente outras obras disponíveis do mesmo autor.

### RF-03: Estratégia de Cold Start para Novos Visitantes
- **História de Usuário:** Como novo visitante, quero ver as peças culturais mais populares de Pernambuco, para começar minha navegação.
- **Critério de Aceitação:** SE o comprador não possuir histórico de navegação ou compras anteriores, ENTÃO O MÓDULO DE RECOMENDAÇÃO DEVERÁ retornar uma lista das 6 peças mais bem avaliadas da cultura pernambucana.

### RF-04: Fallback por Falha do Serviço
- **História de Usuário:** Como sistema, quero garantir a exibição de produtos mesmo em caso de falha no modelo de IA, para não quebrar a experiência da loja.
- **Critério de Aceitação:** SE o serviço de IA estiver indisponível ou retornar erro, ENTÃO O MÓDULO DE RECOMENDAÇÃO DEVERÁ retornar uma seleção estática em cache contendo uma peça de cada polo criativo principal.

## Requisitos Não Funcionais

### RNF-01: Desempenho de Resposta
- **História de Usuário:** Como sistema, preciso de respostas ágeis da API de recomendação para não travar o carregamento das páginas da loja.
- **Critério de Aceitação:** O MÓDULO DE RECOMENDAÇÃO DEVERÁ responder às requisições de sugestão de produtos em tempo de latência inferior a 300 milissegundos no percentil 95.

### RNF-02: Privacidade e Anonimização
- **História de Usuário:** Como usuário, quero que meus dados pessoais sejam protegidos durante a navegação.
- **Critério de Aceitação:** O MÓDULO DE RECOMENDAÇÃO DEVERÁ utilizar estritamente identificadores anonimizados (`user_id`), sem manipular ou armazenar dados pessoais (PII) nas requisições.

### RNF-03: Ambiente de Execução
- **História de Usuário:** Como engenheiro de infraestrutura (or DevOps), quero que o módulo de IA seja empacotado em contêineres e rode em ambiente Linux, para garantir a portabilidade e facilitar a implantação na mesma nuvem do sistema principal.
- **Critério de Aceitação:** O MÓDULO DE RECOMENDAÇÃO DEVERÁ ser fornecido como uma imagem de contêiner (ex: Docker) nativamente executável em sistemas operacionais baseados em Linux.
