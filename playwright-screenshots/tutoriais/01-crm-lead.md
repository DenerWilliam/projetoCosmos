# Tutorial: CRM - Criacao de Lead

## O que e o CRM no Odoo?

O CRM (Customer Relationship Management) e o modulo responsavel pelo **funil de vendas**
da empresa. E onde voce gerencia oportunidades de negocio, desde o primeiro contato ate
o fechamento do contrato.

## Por que criar Leads?

Um **lead** e uma oportunidade potencial de venda. No contexto da **Cosmos Advisors**
(consultoria financeira), um lead representa um cliente que demonstrou interesse em
servicos como:

- Fusoes e aquisicoes (M&A)
- Corporate Finance
- Due Diligence
- BPO Financeiro

## Fluxo: Criar um Lead no Pipeline

### Passo 1: Acessar o CRM

Navegue ate o modulo CRM pelo menu superior. O funil de vendas aparece com as colunas:

- **Novo** → Leads recem-criados
- **Qualificado** → Leads que passaram no primeiro filtro
- **Proposta** → Proposta enviada ao cliente
- **Ganhamos** → Negocio fechado

> **Por que comecar pelo funil?** O funil e a visao principal do vendedor. E onde ele
> passa a maior parte do tempo trabalhando.

### Passo 2: Clicar em NOVO

O botao NOVO abre um formulario rapido (quick-add) onde voce preenche:

- **Organizacao/Cliente** → Nome da empresa ou pessoa
- **Oportunidade** → Descricao curta do negocio

> **Dica:** Nao precisa preencher tudo de uma vez. O Odoo permite salvar e completar
> depois.

### Passo 3: Preencher os Dados

No formulario completo, adicione informacoes mais detalhadas:

| Campo            | Exemplo               | Por que importa?                     |
| ---------------- | --------------------- | ------------------------------------ |
| Email            | contato@cosmos.com.br | Para enviar propostas e follow-ups   |
| Telefone         | +55 11 3000-1234      | Para contato direto                  |
| Receita Esperada | $150.000              | Para calcular o pipeline financeiro  |
| Empresa          | Cosmos Advisors       | Para vincular ao cadastro do cliente |

> **Por que preencher a receita esperada?** Ela alimenta os relatorios de forecast
> (previsao de vendas). O gestor consegue ver quanto faturar no mes.

### Passo 4: Salvar com Ctrl+S

O Odoo 16 usa **Ctrl+S** para salvar (nao tem botao visivel). Apos salvar:

- O lead aparece no funil na coluna "Novo"
- Um numero e atribuido automaticamente (ex: LEAD/0042)
- O sistema registra a data e o responsavel

### Passo 5: Verificar no Pipeline

Volte ao funil para confirmar que o lead aparece corretamente com:

- Titulo da oportunidade
- Valor da receita esperada
- Nome do cliente

## Fluxo Visual

```
CRM → NOVO → Preencher dados → Ctrl+S → Ver no funil
```

## Screenshots

| Etapa               | Arquivo                     |
| ------------------- | --------------------------- |
| Pipeline vazio      | `01_crm_pipeline.png`       |
| Formulario rapido   | `02_form_quick.png`         |
| Formulario completo | `03_form_full.png`          |
| Dados preenchidos   | `04_form_filled.png`        |
| Lead salvo          | `05_lead_saved.png`         |
| Lead no funil       | `06_pipeline_with_lead.png` |

## GIF do Fluxo

O video/GIF mostra o fluxo completo de criacao de um lead, desde a navegacao ate o
resultado final no funil.

## Boas Praticas

1. **Sempre preencha o email** — sem email, nao e possivel enviar propostas automaticas
2. **Use a receita esperada** — ela e usada nos relatorios de dashboard
3. **Mova o lead no funil** — arraste o card para a coluna certa conforme o progresso
4. **Adicione notas** — use o campo de descricao para historico do contato
5. **Atribua um responsavel** — sempre designe quem esta cuidando da oportunidade

## Comandos Uteis

| Acao           | Atalho/Metodo  |
| -------------- | -------------- |
| Salvar         | `Ctrl+S`       |
| Criar novo     | Botao NOVO     |
| Editar         | Botao EDITAR   |
| Mover no funil | Arrastar card  |
| Excluir        | Acao > Excluir |

---

- Tutorial gerado automaticamente a partir dos scripts de automacao Playwright\*
