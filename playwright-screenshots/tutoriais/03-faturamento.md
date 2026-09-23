# Tutorial: Faturamento - Emissao de Nota Fiscal

## O que e o modulo de Faturamento?

O modulo de Faturamento (Accounting/Invoicing) e responsavel pela **emissao de notas
fiscais**, gestao de recebimentos e controle financeiro da empresa.

Na **Cosmos Advisors**, ele e usado para:

- Emitir faturas de consultoria
- Controlar recebimentos de clientes
- Gerar relatorios de faturamento
- Conciliacao bancaria

## Por que emitir Faturas no Odoo?

Uma **fatura** e o documento oficial que cobra o cliente por um servico prestado. No
Odoo, ela:

- Gera lancamentos contabeis automaticamente
- Controla o vencimento e pagamento
- Alimenta os relatorios financeiros
- Permite conciliacao bancaria

## Fluxo: Criar uma Fatura

### Passo 1: Acessar o Faturamento

Navegue ate o modulo pelo menu superior. A lista de faturas mostra:

| Coluna             | Descricao                              |
| ------------------ | -------------------------------------- |
| Numero             | Sequencial automatico (INV/2026/00006) |
| Cliente            | Quem esta sendo cobrado                |
| Data da Fatura     | Data de emissao                        |
| Data de Vencimento | Quando o pagamento e devido            |
| Total              | Valor total da fatura                  |
| Situacao           | Rascunho, Lançado, Pago                |

> **Por que comecar pela lista?** Ver faturas anteriores ajuda a manter o padrao de
> numeracao e formatacao.

### Passo 2: Clicar em NOVO

O formulario de nova fatura e aberto com os campos principais:

| Campo                  | Obrigatorio? | Descricao                       |
| ---------------------- | :----------: | ------------------------------- |
| Cliente (partner_id)   |     Sim      | Quem sera cobrado               |
| Data da Fatura         |     Sim      | Data de emissao                 |
| Referencia             |     Nao      | Numero de referencia do cliente |
| Condicoes de Pagamento |     Nao      | Prazo de pagamento              |

> **Por que o cliente e obrigatorio?** A fatura precisa ter um destinatario para gerar o
> lancamento contabil correto.

### Passo 3: Preencher o Cliente

O campo **Cliente** e um many2one que busca no cadastro de contatos.

- Digite o nome do cliente
- Selecione na lista suspensa
- O Odoo preenche automaticamente dados fiscais (CNPJ, endereco)

> **Dica:** Se o cliente nao existe, cadastre primeiro em Contatos.

### Passo 4: Preencher Data e Referencia

- **Data da Fatura** → Data de emissao (padrao: hoje)
- **Referencia** → Numero do contrato ou pedido do cliente

> **Por que usar referencia?** Ela ajuda o cliente a identificar a fatura no extrato
> bancario.

### Passo 5: Adicionar Linhas de Produto

Cada linha representa um item/servico faturado:

| Campo          | Descricao          | Exemplo                      |
| -------------- | ------------------ | ---------------------------- |
| Descricao      | Nome do servico    | Consultoria Financeira - M&A |
| Quantidade     | Unidades           | 10 (horas)                   |
| Preco Unitario | Valor por unidade  | R$ 5.000,00                  |
| Total          | Calculo automatico | R$ 50.000,00                 |

Para adicionar:

1. Clique em **"Adicionar uma linha"**
2. Preencha a descricao
3. Defina quantidade e preco
4. Repita para cada item

> **Por que linhas separadas?** Cada linha gera um lancamento contabil diferente. Isso
> facilita a analise de receita por servico.

### Passo 6: Salvar e Confirmar

1. **Ctrl+S** → Salva como Rascunho
2. **Confirmar** → Muda para "Lancado" (status fiscal)
3. **Registrar Pagamento** → Registra o recebimento

> **Diferenca entre Rascunho e Lancado:**
>
> - **Rascunho** → Pode editar livremente, nao gera lancamento contabil
> - **Lancado** → Documento fiscal emitido, gera lancamento automatico

### Passo 7: Registrar Pagamento

Apos a confirmacao, o botao **"Registrar Pagamento"** aparece:

1. Clique no botao
2. Selecione a forma de pagamento (Dinheiro, Transferencia, Cartao)
3. Confirme

A fatura muda para **"Pago"** e o lancamento bancario e criado.

## Fluxo Visual

```
Faturamento → NOVO → Preencher cliente → Adicionar linhas → Ctrl+S → Confirmar → Registrar Pagamento
```

## Screenshots

| Etapa                | Arquivo                    |
| -------------------- | -------------------------- |
| Lista de faturas     | `01_faturas_lista.png`     |
| Formulario vazio     | `02_form_fatura.png`       |
| Linhas adicionadas   | `03_linhas_fatura.png`     |
| Fatura salva         | `04_fatura_salva.png`      |
| Fatura confirmada    | `05_fatura_confirmada.png` |
| Pagamento registrado | `06_pagamento.png`         |

## Status da Fatura

| Status        | Significado       | Acao disponivel             |
| ------------- | ----------------- | --------------------------- |
| **Rascunho**  | Em edicao         | Editar, Excluir             |
| **Lancado**   | Documento emitido | Registrar Pagamento, Enviar |
| **Pago**      | Recebido          | Imprimir, Enviar            |
| **Cancelado** | Anulado           | Nenhuma                     |

## Boas Praticas

1. **Preencha a referencia** — facilita a identificacao pelo cliente
2. **Use linhas separadas** — cada servico deve ter sua linha
3. **Confirme rapidamente** — rascunhosc nao geram relatorio
4. **Registre o pagamento** — para manter o fluxo de caixa atualizado
5. **Revise antes de confirmar** — depois de Lancado, nao pode editar

## Relatorios

O modulo gera automaticamente:

- **Demonstracao de Resultados (DRE)** — receita vs despesas
- **Fluxo de Caixa** — entradas e saidas
- **Inadimplencia** — faturas vencidas nao pagas
- **Analise por Cliente** — quem mais fatura

---

- Tutorial gerado automaticamente a partir dos scripts de automacao Playwright\*
