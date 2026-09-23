# Tutorial: Contatos - Cadastro de Cliente

## O que e o modulo de Contatos?

O modulo de Contatos e o **cadastro central** da empresa. Todos os dados de clientes,
fornecedores e parceiros sao armazenados aqui.

Na **Cosmos Advisors**, os contatos sao usados para:

- Clientes que recebem faturas
- Empresas parceiras
- Fornecedores de servicos
- Contatos para correspondencia

## Por que cadastrar Contatos?

Um **contato** no Odoo nao e apenas um nome e telefone. Ele e um registro completo que
alimenta outros modulos:

| Modulo      | Como usa o contato     |
| ----------- | ---------------------- |
| Faturamento | Para gerar faturas     |
| CRM         | Para vincular leads    |
| Helpdesk    | Para associar tickets  |
| Vendas      | Para gerar pedidos     |
| Compras     | Para pedidos de compra |

> **Contato bem cadastrado = menos retrabalho em todos os modulos.**

## Fluxo: Criar um Contato

### Passo 1: Acessar Contatos

Navegue ate o modulo pelo menu superior. A grade mostra os contatos ja cadastrados com
foto e nome.

> **Por que comecar pela grade?** Ver contatos existentes evita duplicatas.

### Passo 2: Clicar em NOVO

O formulario de novo contato e aberto. Primeiro, selecione o tipo:

| Tipo                | Quando usar                     |
| ------------------- | ------------------------------- |
| **Pessoa Fisica**   | Cliente individual, funcionario |
| **Pessoa Juridica** | Empresa, organizacao            |

> **Dica:** Para clientes da Cosmos Advisors (consultoria), o mais comum e Pessoa
> Juridica.

### Passo 3: Preencher Dados Principais

| Campo    |       Importancia       | Exemplo            |
| -------- | :---------------------: | ------------------ |
| Nome     |      Identificacao      | Joao Silva         |
| Empresa  | Vinculo com organizacao | Cosmos Advisors    |
| Cargo    |    Funcao do contato    | Diretor Financeiro |
| Email    |       Comunicacao       | joao@cosmos.com.br |
| Telefone |     Contato direto      | +55 11 99999-1234  |

> **Por que o email e importante?** Ele e usado para enviar faturas, propostas e
> notificacoes automaticas.

### Passo 4: Preencher Endereco

| Campo          | Descricao          |
| -------------- | ------------------ |
| Endereco (Rua) | Logradouro         |
| Complemento    | Andar, sala, bloco |
| Cidade         | Municipio          |
| CEP            | Codigo postal      |
| Pais           | Brasil             |

> **Por que preencher endereco?** E obrigatorio para notas fiscais (NFe) e para
> correspondencia fisica.

### Passo 5: Preencher Dados Fiscais

| Campo              | Descricao         | Exemplo            |
| ------------------ | ----------------- | ------------------ |
| CNPJ/CPF           | Documento fiscal  | 12.345.678/0001-99 |
| Inscricao Estadual | IE (se aplicavel) | Isento             |

> **Por que o CNPJ e crucial?** Sem CNPJ, nao e possivel emitir nota fiscal para a
> empresa.

### Passo 6: Preencher Contatos Adicionais

| Campo   | Descricao            |
| ------- | -------------------- |
| Celular | Telefone alternativo |
| Website | Site da empresa      |

### Passo 7: Salvar

Clique em **Salvar** ou pressione **Ctrl+S**.

O contato fica disponivel em todos os modulos do Odoo.

## Fluxo Visual

```
Contatos → NOVO → Selecionar tipo → Preencher dados → Preencher endereco → Preencher CNPJ → Salvar
```

## Screenshots

| Etapa                 | Arquivo                 |
| --------------------- | ----------------------- |
| Lista de contatos     | `01_contatos_lista.png` |
| Formulario preenchido | `02_form_contato.png`   |
| Contato salvo         | `03_contato_salvo.png`  |

## Campos Importantes

### Dados de Identificacao

- **Nome** → Identificador principal
- **Tipo** → Fisica ou Juridica
- **CNPJ/CPF** → Documento fiscal

### Dados de Contato

- **Email** → Comunicacao e notificacoes
- **Telefone** → Contato direto
- **Website** → Presenca online

### Dados de Endereco

- **Endereco** → Correspondencia e fiscal
- **Cidade/CEP** → Localizacao
- **Pais** → Para impostos internacionais

## Boas Praticas

1. **Nao duplique contatos** — busque antes de criar novo
2. **Preencha o CNPJ** — obrigatorio para faturamento
3. **Use email corporativo** — facilita identificacao
4. **Atualize dados** — movimentacoes de endereco/telefone
5. **Vincule a empresa** — usando o campo "Empresa" (commercial_partner_id)
6. **Adicione foto** — para identificacao visual na grade

## Uso em Outros Modulos

### Faturamento

Ao criar uma fatura, busque o contato pelo nome. O Odoo puxa automaticamente:

- CNPJ
- Endereco
- Condicoes de pagamento

### CRM

Ao criar um lead, vincule o contato para historico completo.

### Helpdesk

## Ao criar um ticket, associe ao contato para saber quem esta pedindo suporte.

```mermaid
swimlane-beta LR
  subgraph Customer
    Browse[Browse catalogue]
    Pay[Pay]
  end
  subgraph Warehouse
    Pick[Pick items]
    Ship[Ship order]
  end
  subgraph Finance
    Invoice[Raise invoice]
  end
  Browse --> Pay
  Pay --> Pick
  Pick --> Ship
  Pay --> Invoice
```

---

- Tutorial gerado automaticamente a partir dos scripts de automacao Playwright\*
