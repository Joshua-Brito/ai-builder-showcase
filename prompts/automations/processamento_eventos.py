"""
Pipeline de Tratamento e Higienização de Notificações Operacionais (Webhooks)
Autor: Joshua Miguel Brito
Objetivo: Sanitizar payloads recebidos da esteira logística, classificar criticidade
          e padronizar os dados para ingestão em filas operacionais e dashboards.
"""

import json
from typing import Dict, Any
from datetime import datetime


def validar_payload_operacional(payload: Dict[str, Any]) -> bool:
    """
    Valida se os campos obrigatórios para o roteamento do evento existem no payload.
    """
    campos_obrigatorios = {"id", "tipo_evento", "status", "detalhes"}
    return campos_obrigatorios.issubset(payload.keys())


def processar_evento_logistico(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Higieniza, normaliza e aplica regras de negócio para roteamento de pedidos críticos.
    """
    if not validar_payload_operacional(payload):
        raise ValueError("Payload operacional inválido: campos obrigatórios ausentes.")

    evento_id = str(payload["id"]).strip().upper()
    tipo_evento = str(payload["tipo_evento"]).strip().upper()
    status_bruto = str(payload["status"]).strip().upper()
    detalhes = payload.get("detalhes", {})

    # Mapeamento e normalização de criticidade
    status_criticos = {"FALHA_ENTREGA", "CANCELADO_SISTEMA", "EXTRAVIO", "TIMEOUT_CLIENTE"}
    e_critico = status_bruto in status_criticos

    # Tratamento seguro de valores monetários
    try:
        valor_pedido = float(detalhes.get("valor", 0.0))
    except (ValueError, TypeError):
        valor_pedido = 0.0

    # Construção do payload padronizado para as squads operacionais
    registro_processado = {
        "transacao_id": evento_id,
        "tipo_evento": tipo_evento,
        "status_normalizado": status_bruto,
        "is_critico": e_critico,
        "valor_pedido": round(valor_pedido, 2),
        "regiao_operacional": detalhes.get("regiao", "NAO_INFORMADA").strip().title(),
        "tempo_em_espera_minutos": int(detalhes.get("tempo_espera_minutos", 0)),
        "rota_acao": "FILA_PRIORITARIA" if e_critico else "FLUXO_REGULAR",
        "timestamp_processamento": datetime.utcnow().isoformat() + "Z"
    }

    return registro_processado


if __name__ == "__main__":
    # Simulação de evento recebido de webhook operacional (ex: pedido com entrega travada)
    evento_simulado = {
        "id": "IFOOD-REC-2026-8841",
        "tipo_evento": "LOGISTICA_LOCAL",
        "status": "falha_entrega",
        "detalhes": {
            "valor": "94.80",
            "regiao": "recife-centro",
            "tempo_espera_minutos": 12,
            "motivo": "cliente_nao_localizado"
        }
    }

    print("--- Processando Evento Operacional ---")
    resultado = processar_evento_logistico(evento_simulado)
    
    # Exibe o resultado formatado em JSON identado
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
