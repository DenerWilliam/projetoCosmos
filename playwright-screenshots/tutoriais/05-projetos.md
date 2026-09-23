# Tutorial: Projetos - Gestao de Projetos

## O que e o modulo de Projetos?

O modulo de Projetos do Odoo gerencia **tarefas, prazos e recursos** de projetos da
empresa. E ideal para empresas de servicos como a **Cosmos Advisors**.

## Por que usar Projetos no Odoo?

Para uma consultoria financeira, projetos incluem:

- Processos de M&A (Fusoes e Aquisicoes)
- Due Diligence
- Reestruturacao financeira
- BPO financeiro por projeto

O modulo permite:

- Acompanhar progresso por tarefa
- Controlar prazos e responsaveis
- Medir horas trabalhadas
- Gerar relatorios de produtividade

## Visao Kanban (Principal)

A visao Kanban mostra projetos como cards organizados por estagio:

| Estagio          | Significado                           |
| ---------------- | ------------------------------------- |
| **A Fazer**      | Projeto planejado, ainda nao iniciado |
| **Em Andamento** | Trabalho em progresso                 |
| **Concluido**    | Projeto finalizado                    |

### Informacoes no Card

Cada card mostra:

- **Nome do Projeto** → Titulo
- **Responsavel** → Quem lidera
- **Prazo** → Data de inicio e fim
- **Tipo** → Externo, Interno, Experimental
- **Tarefas** → Numero de tarefas associadas
- **Tickets** → Chamados vinculados ao projeto

> **Por que o card mostra tarefas e tickets?** Para ver rapidamente o nivel de atividade
> de cada projeto.

## Fluxo: Criar um Projeto

### Passo 1: Acessar Projetos

Navegue ate o modulo pelo menu superior. A visao Kanban mostra os projetos existentes.

### Passo 2: Clicar em NOVO

O formulario de novo projeto e aberto com os campos:

| Campo          | Obrigatorio? | Descricao                      |
| -------------- | :----------: | ------------------------------ |
| Nome           |     Sim      | Titulo do projeto              |
| Responsavel    |     Nao      | Gerente do projeto             |
| Cliente        |     Nao      | Empresa beneficiada            |
| Data de Inicio |     Nao      | Quando comeca                  |
| Data de Fim    |     Nao      | Quando termina                 |
| Tipo           |     Nao      | Externo, Interno, Experimental |

> **Por que definir o tipo?** Tipo Externo e para clientes; Interno para projetos da
> propria empresa.

### Passo 3: Configurar o Projeto

Apos criar o projeto, configure:

1. **Criar tarefas** → Itens de trabalho individuais
2. **Definir responsaveis** → Quem faz cada tarefa
3. **Estimar horas** → Quanto tempo vai levar
4. **Definir marcos** → Eventos importantes

### Passo 4: Gerenciar Tarefas

Dentro do projeto, crie tarefas com:

| Campo               | Descricao                        |
| ------------------- | -------------------------------- |
| Titulo da Tarefa    | O que precisa ser feito          |
| Responsavel         | Quem vai executar                |
| Prazo               | ate quando                       |
| Estimativa de Horas | Quanto tempo estimado            |
| Estagio             | A Fazer, Em Andamento, Concluido |

> **Dica:** Tarefas muito grandes devem ser divididas em subtarefas.

### Passo 5: Acompanhar Progresso

O projeto mostra automaticamente:

- **Percentual concluido** → Baseado nas tarefas
- **Horas trabalhadas** → Lançadas pelos responsaveis
- **Atrasos** → Tarefas alem do prazo
- **Anexos** → Documentos do projeto

## Visao Gantt

A visao Gantt mostra um grafico de barras com:

- Linha do tempo do projeto
- Tarefas como barras
- Sobreposicoes e dependencias
- Marcos importantes

> **Quando usar Gantt?** Para projetos complexos com muitas tarefas interdependentes.

## Screenshots

| Etapa             | Arquivo           |
| ----------------- | ----------------- |
| Lista de projetos | `04_projects.png` |

## Boas Praticas

1. **Nome claro** — o titulo deve descrever o projeto
2. **Defina responsavel** — sempre designe um lider
3. **Crie tarefas detalhadas** — tarefas grandes confundem
4. **Use prazos reais** — prazos apertados geram atrasos
5. **Registre horas** — para medir produtividade
6. **Feche tarefas** — mantenha o kanban limpo

## Integracao com Outros Modulos

| Modulo               | Integracao                              |
| -------------------- | --------------------------------------- |
| **Helpdesk**         | Tickets podem ser vinculados a projetos |
| **Faturamento**      | Horas trabalhadas geram faturas         |
| **CRM**              | Oportunidades podem virar projetos      |
| **Recursos Humanos** | Atribuicao de equipe                    |

## Relatorios

O modulo gera:

- **Burndown Chart** — progresso vs tempo
- **Horas por Tarefa** — distribuicao de esforco
- **Atrasos** — tarefas fora do prazo
- **Produtividade por Responsavel** — quem entrega mais

---

- Tutorial gerado automaticamente a partir dos scripts de automacao Playwright\*
