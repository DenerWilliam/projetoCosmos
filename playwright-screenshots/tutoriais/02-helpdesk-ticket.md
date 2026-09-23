# Tutorial: Helpdesk - Criacao de Ticket

## O que e o Helpdesk no Odoo?

O Helpdesk e o modulo de **gestao de chamados** (tickets). Ele permite registrar,
acompanhar e resolver solicitacoes de clientes ou usuarios internos.

Na **Cosmos Advisors**, o Helpdesk e util para:

- Duvidas sobre servicos prestados
- Solicitacoes de integracao ERP
- Suporte tecnico
- Reclamacoes e sugestoes

## Por que criar Tickets?

Um **ticket** e um registro formal de uma solicitacao. Ele permite:

- Acompanhar o tempo de resposta
- Designar responsaveis
- Histrico de atendimentos
- Metricas de satisfacao

## Fluxo: Criar um Ticket no Helpdesk

### Passo 1: Acessar o Helpdesk

Navegue ate o modulo pelo menu superior. A lista de tickets aparece com as colunas:

- **Prioridade** → Estrelas (1 a 3)
- **Numero do Chamado** → Identificador unico (HT00010)
- **Situacao** → Status visual
- **Titulo** → Descricao curta
- **Estagio** → Novo, Em Andamento, Aguardando, Concluido

> **Por que usar o Helpdesk em vez de email?** Tickets tem historico, prazos e
> responsaveis. Email e informal e facil de perder.

### Passo 2: Clicar em NOVO

O formulario de novo ticket e aberto com os campos:

| Campo                   | Obrigatorio? | Descricao                   |
| ----------------------- | :----------: | --------------------------- |
| Titulo (name)           |     Sim      | Descricao curta do problema |
| Descricao (description) |     Sim      | Detalhes completos          |
| Contato (partner_id)    |     Nao      | Cliente associado           |
| Equipe (team_id)        |     Nao      | Time responsavel            |
| Usuario (user_id)       |     Nao      | Pessoa designada            |
| Prioridade              |     Nao      | 1-3 estrelas                |
| Categoria               |     Nao      | Tipo do chamado             |
| Marcadores              |     Nao      | Tags para filtragem         |

> **Por que o titulo e obrigatorio?** Ele e o campo principal que aparece na lista e nos
> relatorios. Um titulo claro facilita o gerenciamento.

### Passo 3: Preencher o Titulo

O titulo e o campo de texto grande no topo do formulario (abaixo do numero "/" que sera
atribuido).

Exemplo: **"Duvida sobre Integracao ERP"**

> **Dica:** Seja especifico. Em vez de "Problema", escreva "Erro ao gerar relatorio
> financeiro".

### Passo 4: Preencher o Contato

O campo **Contato** (partner_id) e um campo many2one que busca no cadastro de contatos.

- Digite o nome do cliente
- O Odoo mostra sugestoes
- Selecione o cliente correto

> **Por que vincular ao contato?** Assim o ticket fica associado ao historico completo
> do cliente.

### Passo 5: Preencher a Descricao

Abaixo dos campos principais, ha uma aba **Descricao** com um campo de texto livre.

Use para detalhar:

- O que o cliente solicitou
- Passos para reproduzir o problema
- Informacoes tecnicas relevantes

### Passo 6: Salvar com Ctrl+S

Apos salvar:

- O ticket recebe um numero (HT00010)
- O estagio e definido como "Novo"
- O responsavel e atribuido automaticamente (se configurado)

### Passo 7: Verificar na Lista

Volte a lista de tickets para confirmar que o ticket aparece com:

- Numero do chamado
- Titulo correto
- Estagio "Novo"
- Data de criacao

## Fluxo Visual

```
Helpdesk → Tickets → NOVO → Preencher titulo/descricao → Ctrl+S → Ver na lista
```

## Screenshots

| Etapa             | Arquivo                   |
| ----------------- | ------------------------- |
| Lista de tickets  | `01_tickets_list.png`     |
| Formulario vazio  | `02_ticket_form.png`      |
| Dados preenchidos | `03_ticket_filled.png`    |
| Ticket salvo      | `04_ticket_saved.png`     |
| Ticket na lista   | `05_tickets_with_new.png` |

## Gerenciamento de Tickets

### Mover entre Estagios

| Estagio          | Significado                      |
| ---------------- | -------------------------------- |
| **Novo**         | Recem-criado, aguardando analise |
| **Em Andamento** | Sendo atendido                   |
| **Aguardando**   | Esperando resposta do cliente    |
| **Concluido**    | Resolvido e fechado              |
| **Cancelado**    | Descartado                       |

### Acoes Comuns

| Acao                 | Como fazer                          |
| -------------------- | ----------------------------------- |
| Designar responsavel | Editar campo "Usuario atribuido"    |
| Mudar prioridade     | Clicar nas estrelas                 |
| Adicionar categoria  | Selecionar no campo "Categoria"     |
| Adicionar marcadores | Selecionar no campo "Marcadores"    |
| Enviar mensagem      | Aba "Enviar mensagem" no formulario |

## Boas Praticas

1. **Titulo descritivo** — sempre descreva o problema em uma linha
2. **Descricao detalhada** — inclua passos para reproduzir
3. **Vincule ao contato** — para historico completo
4. **Defina prioridade** — tickets criticos ficam em 3 estrelas
5. **Mova o estagio** — mantenha o ticket sempre no estagio correto
6. **Use marcadores** — para filtrar por tipo (bug, duvida, solicitacao)

## Metricas Importantes

O Helpdesk gera relatorios de:

- **Tempo medio de resposta** — tempo entre criacao e primeira acao
- **Tickets por equipe** — distribuicao de trabalho
- **Satisfacao do cliente** — pos-atendimento
- **Volume por categoria** — quais problemas sao mais comuns

---

- Tutorial gerado automaticamente a partir dos scripts de automacao Playwright\*
