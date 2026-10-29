# Fluxo de Automação Low-Code/No-Code: Resolução de Incidentes Logísticos (n8n / Make)

## 1. Visão do Fluxo
Automação construída para interceptar alertas operacionais de entregas paradas, consultar o status da rota via API e despachar notificações automáticas sem intervenção manual.

---

## 2. Diagrama Lógico da Esteira

text
[Webhook de Entrada: Alerta de Pedido Travado]
                     ↓
[Módulo 1: Validação de Payload e Limpeza de Dados]
                     ↓
[Módulo 2: Chamada LLM (Classificação de Severidade & Sentimento)]
                     ↓
         ┌───────────┴───────────┐
         ▼                       ▼
    [Urgência ALTA]         [Urgência MÉDIA/BAIXA]
         ↓                       ↓
[Disparo Slack/WhatsApp     [Atualização de Status
 Suporte Emergencial]        em Banco / Fila de Espera]

3. Especificação dos Nós do Fluxo
Gatilho (Trigger): Webhook Listener recebendo eventos HTTP POST da esteira de logística.

Camada de Decisão com IA: Integração com modelo de linguagem via API REST para validar se o cliente respondeu às tentativas de contato nos últimos 10 minutos.

Roteamento Condicional (Router):

Se status == "FALHA_ENTREGA" e tentativas >= 3: dispara notificação imediata via API para cancelamento assistido e ressarcimento de rota ao entregador.

Caso contrário: agenda nova verificação automática em 5 minutos.

4. Impacto Operacional
Tempo médio de resolução: Reduzido de 8 minutos para menos de 40 segundos por caso.

Autonomia da Operação: Redução de chamados manuais abertos para a equipe de atendimento humano.

---

### 2. Criar a pasta `cases/` com o arquivo `cases/oportuniza_vibe_coding.md`

O edital valoriza candidatos que sabem usar ferramentas de IA para gerar produtos e demos funcionais do zero. Esse arquivo documenta o **Oportuniza**:

No GitHub, vá em **Add file** > **Create new file**, digite `cases/oportuniza_vibe_coding.md` e cole:

markdown
# Case de Produto & Prototipagem com IA: Oportuniza WebApp

## 1. O Problema
Dificuldade de inclusão de jovens talentos em vagas formais de trabalho devido a currículos desestruturados e falta de alinhamento com requisitos técnicos básicos.

---

## 2. A Solução Construída
Desenvolvimento de uma aplicação *mobile-first* integrando Inteligência Artificial Generativa para apoiar jovens na formatação de perfis, simulação de entrevistas e conexão com oportunidades.

- **Metodologia:** *Product Discovery*, *Lean Canvas* e prototipagem ágil orientada por IA (*Vibe Coding*).
- **Camada de IA:** Prompts instrucionais desenhados para agir como mentor de carreira, traduzindo vivências informais em competências técnicas reconhecidas pelo mercado.
- **Ambiente:** Desenvolvido no contexto de residência tecnológica no ecossistema do Porto Digital.

---

## 3. Arquitetura da Solução

text
[Interface WebApp (Mobile-First)]
               ↓
   [Requisição API / Backend]
               ↓
[Camada de Prompt Engineering (LLM)]
               ↓
[Geração Estruturada de Diagnóstico de Carreira]
4. Aprendizados & Resultados
Demonstração prática de entrega ponta a ponta: do problema de negócio ao produto funcional deployado em poucos dias.

Validação rápida de hipóteses de negócio utilizando ferramentas de IA como acelerador de código e design.


---

### 3. Atualizar o `README.md` principal do repositório

Para amarrar tudo, abra o `README.md` na raiz do repositório, clique no lápis de editar e atualize a seção **Estrutura do Repositório** para refletir os novos arquivos:

markdown
## 📂 Estrutura do Repositório

- [`/prompts`](./prompts): Prompts estruturados para análise, classificação e extração de dados com LLMs.
- [`/automations`](./automations): Scripts em Python e arquitetura de fluxos com n8n/Make para automação de esteiras.
- [`/cases`](./cases): Demonstração de prototipagem ágil de produtos (*Vibe Coding*) co
