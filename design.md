# Design Técnico e Arquitetura

## 1. Diagrama de Componentes e Fluxo de Dados
1. **Frontend (Marketplace):** Envia uma requisição HTTP REST para o Backend com o `user_id` e o `product_id` atual.
2. **Backend (API Principal):** Encaminha os dados do contexto para o Módulo de Recomendação.
3. **Módulo de Recomendação (IA):**
    * Consulta o Banco de Dados Vetorial para buscar similaridade de tipologia/polo criativo.
    * Gera a lista de IDs recomendados.
4. **Retorno:** A API Principal enriquece os IDs com foto/preço e devolve ao Frontend.

## 2. Modelo de Dados e Estratégia
- **Estratégia Principal:** Filtragem Baseada em Conteúdo (Content-Based Filtering) focada em metadados culturais (Tipologia, Mestre, Polo Criativo).
- **Baseline (Cold Start):** Produtos mais vendidos e com melhor avaliação geral no marketplace, categorizados por polo criativo.
- **Modelo de Dados Necessário (Entrada):** Histórico de cliques do usuário, metadados dos produtos (tags, região, material).

## 3. Interface de Integração (API)
A integração será feita via API RESTful.

- **Endpoint:** `POST /api/v1/recommendations/handicrafts`
- **Requisição (Entrada):**
    ```json
    {
      "user_id": "usr_recife_8841",
      "current_product_id": "prod_caruaru_barro_01",
      "context": {
        "typology": "cerâmica_de_barro",
        "creative_pole": "Caruaru"
      },
      "limit": 4
    }
    ```
- **Resposta (Saída de Sucesso):**
    ```json
    {
      "status": "success",
      "strategy_applied": "cultural_typology_matching",
      "recommended_products": [
        {
          "product_id": "prod_tracunhaem_barro_04",
          "artisan_name": "Mestre Nuca",
          "score": 0.94
        },
        {
          "product_id": "prod_caruaru_vitalino_09",
          "artisan_name": "Familia Vitalino",
          "score": 0.89
        }
      ]
    }
    ```

## 4. Tratamento de Erros e Contingência
- **Timeout (>300ms) ou HTTP 500:** A interface de integração aborta a chamada e aciona a estratégia de *Fallback* (RF-04), devolvendo uma lista estática armazenada no cache do sistema principal.
- **Usuário Não Encontrado (HTTP 404):** Aplica a estratégia de *Cold Start* (RF-03).

## 5. Segurança, Privacidade e Observabilidade
- **Privacidade (LGPD):** Os payloads da API trafegam apenas UUIDs genéricos. Nomes de clientes, endereços ou CPFs nunca são enviados ao módulo de IA.
- **Segurança:** A API do módulo aceitará apenas requisições autenticadas (via token JWT ou mTLS) oriundas da rede interna do sistema principal.
- **Observabilidade:** Logs centralizados com registro do tempo de resposta de cada estratégia aplicada e contagem de acionamentos do sistema de *fallback*.
