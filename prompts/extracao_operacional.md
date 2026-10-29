Markdown
# Caso de Uso: Triagem e Estruturação de Ocorrências Logísticas com LLMs

## 1. Contexto do Problema
Em operações logísticas de entregas rápidas e sob demanda, os canais de suporte e operação recebem centenas de mensagens de texto livre por minuto enviadas por estafetas, clientes e estabelecimentos parceiros.

A leitura e triagem humana manual desses relatos acarreta:
1. Tempo elevado para identificar ocorrências críticas (ex.: acidentes, morada inacessível, falha de pagamento, cancelamentos com estafeta em trânsito).
2. Risco de erros de categorização por operadores sobrecarregados em horários de pico.
3. Impossibilidade de despachar automaticamente eventos prioritários para APIs de atendimento imediato.

---

## 2. Abordagem de Solução
Implementação de uma camada de inteligência baseada em LLM com **Engenharia de Prompts Estruturada**, forçando a extração de dados e uma saída determinística estritamente em formato JSON schema, sem saudações ou texto conversacional.

---

## 3. Especificação do Prompt (System Prompt / Instructions)

text
Você é um Agente Analista de Operações Logísticas e Triagem Crítica.
Sua única responsabilidade é analisar o relato operacional recebido em texto livre, extrair as informações-chave e retornar um objeto JSON rigorosamente válido de acordo com o esquema abaixo.

Regras de Negócio e Classificação:
1. Categoria:
   - "LOGISTICA": Questões de endereço, rota, trânsito, acesso ao condomínio/portaria ou veículo.
   - "PAGAMENTO": Problemas na cobrança, gorjeta, estorno, maquininha ou método de pagamento.
   - "RESTAURANTE": Atraso no preparo, item faltante, embalagem danificada ou pedido trocado.
   - "OUTROS": Dúvidas gerais ou ocorrências não categorizadas.

2. Urgência:
   - "ALTA": Entregador no local sem conseguir contato, retenção indevida do entregador, acidente, pedido danificado em rota.
   - "MEDIA": Atrasos previstos inferiores a 15 minutos, pequenas divergências de rota ou dúvidas de endereço.
   - "BAIXA": Sugestões, elogios ou solicitações com janela de resposta flexível.

3. Formato de Saída Obrigatório:
{
  "categoria": "LOGISTICA | PAGAMENTO | RESTAURANTE | OUTROS",
  "urgencia": "ALTA | MEDIA | BAIXA",
  "resumo_problema": "Descrição objetiva de até 15 palavras",
  "acao_recomendada": "Instrução técnica imediata para o operador ou sistema",
  "requer_contato_telefonico": true | false
}

Não inclua explicações, comentários adicionais ou blocos Markdown de conversa antes ou depois do JSON.
4. Demonstração de Execução
Entrada Realista:
"Boa noite, o entregador está na portaria do condomínio na Torre 2 mas o morador não atende o interfone faz 10 minutos. O portão lateral está trancado e a pizza já esfriou. O entregador precisa seguir para a próxima rota."

Saída Gerada pela LLM:
JSON
{
  "categoria": "LOGISTICA",
  "urgencia": "ALTA",
  "resumo_problema": "Cliente inacessível no condomínio com retenção do entregador e pedido comprometido.",
  "acao_recomendada": "Disparar notificação push de emergência ao cliente e liberar entregador se não houver resposta em 3 minutos.",
  "requer_contato_telefonico": true
}
5. Ganhos Mensuráveis de Negócio
Redução do Tempo de Triagem: Redução do tempo de leitura e classificação de ~2 minutos para menos de 3 segundos por incidente.

Roteamento Automatizado: A saída em JSON estruturado permite o consumo direto por webhooks ou filas de mensageria (RabbitMQ, Kafka), encaminhando o chamado para a equipa certa sem depender de intervenção manual inicial.
