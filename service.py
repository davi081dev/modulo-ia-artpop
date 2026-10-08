import bentoml
from typing import List, Dict, Any, Optional

CATALOGO_ARTESANATO = [
    {
        "product_id": "prod_caruaru_barro_01",
        "nome": "Casal de Lampião e Maria Bonita em Barro",
        "typology": "cerâmica_de_barro",
        "creative_pole": "Caruaru",
        "mestre_id": "mestre_vitalino",
        "artisan_name": "Família Vitalino",
        "score_base": 0.95,
        "avaliacao": 4.9
    },
    {
        "product_id": "prod_tracunhaem_barro_04",
        "nome": "Leão Alado em Cerâmica",
        "typology": "cerâmica_de_barro",
        "creative_pole": "Tracunhaém",
        "mestre_id": "mestre_nuca",
        "artisan_name": "Mestre Nuca",
        "score_base": 0.94,
        "avaliacao": 5.0
    },
    {
        "product_id": "prod_caruaru_vitalino_09",
        "nome": "Retirantes em Barro",
        "typology": "cerâmica_de_barro",
        "creative_pole": "Caruaru",
        "mestre_id": "mestre_vitalino",
        "artisan_name": "Família Vitalino",
        "score_base": 0.89,
        "avaliacao": 4.8
    },
    {
        "product_id": "prod_petrolina_carranca_02",
        "nome": "Carranca Esculpida em Madeira 50cm",
        "typology": "esculpida_em_madeira",
        "creative_pole": "Petrolina",
        "mestre_id": "mestre_ana_carrancas",
        "artisan_name": "Mestre Ana das Carrancas",
        "score_base": 0.92,
        "avaliacao": 4.9
    },
    {
        "product_id": "prod_pesqueira_renda_05",
        "nome": "Toalha de Mesa em Renda Renascença",
        "typology": "renda_renascença",
        "creative_pole": "Pesqueira",
        "mestre_id": "cooperativa_pesqueira",
        "artisan_name": "Cooperativa das Rendeiras",
        "score_base": 0.88,
        "avaliacao": 4.7
    },
    {
        "product_id": "prod_bezerros_papangu_03",
        "nome": "Máscara Tradicional de Papangu",
        "typology": "papelagem_e_mascaras",
        "creative_pole": "Bezerros",
        "mestre_id": "mestre_lula",
        "artisan_name": "Mestre Lula Vassourinha",
        "score_base": 0.91,
        "avaliacao": 4.8
    },
    {
        "product_id": "prod_ibimirim_madeira_07",
        "nome": "Santo São Francisco em Madeira",
        "typology": "esculpida_em_madeira",
        "creative_pole": "Ibimirim",
        "mestre_id": "mestre_sauba",
        "artisan_name": "Mestre Saúba",
        "score_base": 0.87,
        "avaliacao": 4.6
    },
    {
        "product_id": "prod_gloria_mamulengo_08",
        "nome": "Boneco de Mamulengo",
        "typology": "teatro_de_bonecos",
        "creative_pole": "Glória do Goitá",
        "mestre_id": "mestre_ze_vina",
        "artisan_name": "Mestre Zé de Vina",
        "score_base": 0.90,
        "avaliacao": 4.9
    }
]

@bentoml.service(name="modulo_ia_artpop")
class ModuloArtPopService:

    @bentoml.api
    def recomendar_tipologia_regiao(
        self,
        user_id: str,
        current_product_id: str,
        context: Dict[str, str],
        limit: int = 4
    ) -> Dict[str, Any]:
        """RF-01 e Endpoint do Design spec: Retorna produtos por tipologia ou polo criativo."""
        typology = context.get("typology", "").lower()
        creative_pole = context.get("creative_pole", "").lower()

        recomendados = []
        for p in CATALOGO_ARTESANATO:
            if p["product_id"] == current_product_id:
                continue
            if (p["typology"].lower() == typology) or (p["creative_pole"].lower() == creative_pole):
                recomendados.append({
                    "product_id": p["product_id"],
                    "artisan_name": p["artisan_name"],
                    "score": p["score_base"]
                })

        if not recomendados:
            for p in CATALOGO_ARTESANATO:
                if p["product_id"] != current_product_id:
                    recomendados.append({
                        "product_id": p["product_id"],
                        "artisan_name": p["artisan_name"],
                        "score": 0.75
                    })

        return {
            "status": "success",
            "strategy_applied": "cultural_typology_matching",
            "recommended_products": recomendados[:limit]
        }

    @bentoml.api
    def recomendar_mestre_artesao(self, mestre_id: str, limit: int = 4) -> Dict[str, Any]:
        """RF-02: Sugere prioritariamente obras do mesmo Mestre Artesão."""
        obras = [p for p in CATALOGO_ARTESANATO if p["mestre_id"] == mestre_id]
        
        recomendados = []
        for p in obras[:limit]:
            recomendados.append({
                "product_id": p["product_id"],
                "artisan_name": p["artisan_name"],
                "score": 0.98
            })

        return {
            "status": "success",
            "strategy_applied": "master_artisan_focus",
            "mestre_id": mestre_id,
            "recommended_products": recomendados
        }

    @bentoml.api
    def cold_start_populares(self, user_id: str, limit: int = 6) -> Dict[str, Any]:
        """RF-03: Estratégia de Cold Start para novos visitantes (6 peças mais populares)."""
        populares = sorted(CATALOGO_ARTESANATO, key=lambda x: x["avaliacao"], reverse=True)

        recomendados = []
        for p in populares[:limit]:
            recomendados.append({
                "product_id": p["product_id"],
                "artisan_name": p["artisan_name"],
                "score": round(p["avaliacao"] / 5.0, 2)
            })

        return {
            "status": "success",
            "strategy_applied": "cold_start_popular_items",
            "user_id": user_id,
            "recommended_products": recomendados
        }

    @bentoml.api
    def fallback_cache(self) -> Dict[str, Any]:
        """RF-04: Estratégia de Fallback estática em cache com 1 peça por polo criativo."""
        polos_vistos = set()
        cache = []

        for p in CATALOGO_ARTESANATO:
            if p["creative_pole"] not in polos_vistos:
                polos_vistos.add(p["creative_pole"])
                cache.append({
                    "product_id": p["product_id"],
                    "creative_pole": p["creative_pole"],
                    "artisan_name": p["artisan_name"]
                })

        return {
            "status": "fallback_ativo",
            "message": "Serviço principal de IA indisponível. Retornando cache por polo criativo.",
            "recommended_products": cache
        }
