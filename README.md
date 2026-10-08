# AV1 Prática — Módulo de Inteligência Artificial (ArtPop)

<p align="center">
  <b>Marketplace de Artesanato e Cultura de Pernambuco</b>
</p>

---

## 👥 1. Informações da Squad
* **Nome do Projeto:** ArtPop — Marketplace de Artesanato Pernambucano
* **Turma:** ADS - Embarque Digital
* **Grupo / Squad:** ArtPop
* **Membros do Grupo:**
  * Luiz Fernando Ramos de Toledo (Líder / Integrador) — Matrícula: 2025100598
  * Davi Lucas da Silva Pinheiro (Papel e Rastreabilidade)
  * Hugo Vinícius de Lima Mendonça (Entendimento dos dados)
  * Michel dos Santos Serpa (Entendimento do Negócio)

---

## 📌 2. Visão Geral do Módulo
Este repositório contém o **Módulo de Inteligência Artificial** desenvolvido para o ecossistema **ArtPop**. O sistema é focado na valorização dos mestres artesãos e polos criativos pernambucanos (como Caruaru, Tracunhaém e Petrolina), entregando recomendações dinâmicas, tratamento de novos usuários (*Cold Start*) e mecanismos de tolerância a falhas (*Fallback*).

---

## ⚙️ 3. Arquitetura e Requisitos Funcionais (Endpoints)

O serviço foi implementado utilizando **BentoML** e expõe 4 endpoints principais mapeados para os requisitos funcionais (RFs) da AV1:

| Requisito Funcional | Endpoint BentoML | Método | Descrição da Funcionalidade |
| :--- | :--- | :--- | :--- |
| **RF-01** | `/recomendar_tipologia_regiao` | `POST` | Recomenda peças cruzando a tipologia cultural (ex: cerâmica de barro) e o polo criativo de origem. |
| **RF-02** | `/recomendar_mestre_artesao` | `POST` | Prioriza e destaca obras exclusivas criadas por um mesmo Mestre Artesão selecionado. |
| **RF-03** | `/cold_start_populares` | `POST` | Fornece uma lista com as peças mais bem avaliadas para novos visitantes sem histórico prévio. |
| **RF-04** | `/fallback_cache` | `POST` | Retorna um cache estático estruturado por polo criativo caso o motor principal de IA fique indisponível. |

---

## 🛠️ 4. Como Instalar e Executar (Do Zero)

### Pré-requisitos
* Linux, MacOS ou WSL2 (Ubuntu).
* Gerenciador de pacotes `uv` e `Python 3.10+`.

### Passo a Passo Local:
```bash
# 1. Clonar o repositório
git clone [https://github.com/davi081dev/modulo-ia-artpop.git](https://github.com/davi081dev/modulo-ia-artpop.git)
cd modulo-ia-artpop

# 2. Criar o ambiente virtual e instalar dependências com uv
uv venv
source .venv/bin/activate
uv pip install bentoml

# 3. Subir o servidor de IA localmente na porta 3000
bentoml serve service.py:ModuloArtPopService --port 3000

## 4. Casos de Teste e Evidências de Execução (Validação)
### Para comprovar o funcionamento dos endpoints, execute os comandos curl abaixo em um segundo terminal com o servidor ativo:
### Teste 1: Recomendação por Tipologia e Região (RF-01)

curl -X 'POST' \
  'http://localhost:3000/recomendar_tipologia_regiao' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "usr_recife_8841",
    "current_product_id": "prod_caruaru_barro_01",
    "context": {
      "typology": "cerâmica_de_barro",
      "creative_pole": "Caruaru"
    },
    "limit": 4
  }'

### Teste 2: Foco em Mestre Artesão (RF-02)

curl -X 'POST' \
  'http://localhost:3000/recomendar_mestre_artesao' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"mestre_id": "mestre_vitalino", "limit": 4}'

### Teste 3: Cold Start para Novos Visitantes (RF-03)

curl -X 'POST' \
  'http://localhost:3000/cold_start_populares' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"user_id": "usr_novo_1020", "limit": 6}'

### Teste 4: Fallback por Cache (RF-04)

curl -X 'POST' \
  'http://localhost:3000/fallback_cache' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{}'
