# Guia Rápido: Tutoriais Odoo - Cosmos Advisors

## Visao Geral

Esta pasta contem tutoriais para os modulos do Odoo 16 configurados para a **Cosmos
Advisors**.

## Modulos Disponiveis

| #   | Modulo          | Tutorial                                     | Script                     |
| --- | --------------- | -------------------------------------------- | -------------------------- |
| 1   | **CRM**         | [Criacao de Lead](01-crm-lead.md)            | `cosmos_lead.py`           |
| 2   | **Helpdesk**    | [Criacao de Ticket](02-helpdesk-ticket.md)   | `cosmos_helpdesk.py`       |
| 3   | **Faturamento** | [Emissao de Nota Fiscal](03-faturamento.md)  | `cosmos_nota.py`           |
| 4   | **Contatos**    | [Cadastro de Cliente](04-contatos.md)        | `cosmos_contato.py`        |
| 5   | **Projetos**    | [Gestao de Projetos](05-projetos.md)         | `cosmos_all.py`            |
| 6   | **Contatos**    | [Exclusao de Contato](06-excluir-contato.md) | `cosmos_contato_delete.py` |

## Como Usar

### 1. Preparar o Ambiente

```bash
# Salvar sessao (primeira vez)
cd playwright-screenshots
python cosmos_session.py
```

### 2. Rodar os Scripts

```bash
# Gerar screenshots e videos de cada modulo
python cosmos_lead.py       # CRM
python cosmos_helpdesk.py   # Helpdesk
python cosmos_nota.py       # Faturamento
python cosmos_contato.py    # Contatos
python cosmos_all.py        # Todos os modulos
python cosmos_contato_delete.py  # Contatos - Exclusao
```

### 3. Resultados

Cada script gera:

- **Screenshots** → Pasta `output_*/`
- **Videos** → Pasta `output_*/videos/`
- **GIFs** → Pasta `output_*/videos/` (convertidos automaticamente)

## Fluxo dos Tutoriais

Cada tutorial segue a estrutura:

1. **O que e** → Explicacao do modulo
2. **Por que usar** → Beneficios praticos
3. **Passo a passo** → Fluxo detalhado com "por que" de cada acao
4. **Screenshots** → Referencia visual
5. **Boas Praticas** → Dicas de uso
6. **Comandos Uteis** → Atalhos e acoes comuns

## Dicas Gerais

### Atalhos do Odoo 16

| Acao    | Atalho            |
| ------- | ----------------- |
| Salvar  | `Ctrl+S`          |
| Editar  | Botao EDITAR      |
| Excluir | Acao > Excluir    |
| Buscar  | Barra de pesquisa |
| Filtrar | Filtros           |

### Navegacao

- **Menu superior** → Troca de modulos
- **Breadcrumb** → Navegacao hierarquica
- **Voltar** → Botao do navegador ou ESC

### Formularios

- **Campos com \* sao obrigatorios**
- **Campos many2one** → Busca com digitar
- **Campos data** → Calendario popup
- **Campos monetarios** → Formato R$ X.XXX,XX

## Arquivos

```
playwright-screenshots/
├── cosmos_session.py          # Login e salva sessao
├── cosmos_helpers.py          # Modulo compartilhado
├── cosmos_all.py              # Screenshots de todos os modulos
├── cosmos_lead.py             # Fluxo CRM
├── cosmos_helpdesk.py         # Fluxo Helpdesk
├── cosmos_nota.py             # Fluxo Faturamento
├── cosmos_contato.py          # Fluxo Contatos
├── cosmos_contato_delete.py   # Fluxo Exclusao de Contato
├── session_state.json         # Sessao salva (nao committar!)
├── tutoriais/
│   ├── README.md              # Este arquivo
│   ├── 01-crm-lead.md
│   ├── 02-helpdesk-ticket.md
│   ├── 03-faturamento.md
│   ├── 04-contatos.md
│   ├── 05-projetos.md
│   └── 06-excluir-contato.md
├── output_modules/            # Screenshots gerais
├── output_lead/               # Screenshots CRM
├── output_helpdesk/           # Screenshots Helpdesk
├── output_nota/               # Screenshots Faturamento
└── output_contato/            # Screenshots Contatos
```

---

- Gerado para o projeto Cosmos Advisors - Escodoo\*
