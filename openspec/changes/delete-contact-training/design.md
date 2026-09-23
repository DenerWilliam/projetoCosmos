## Context

O projeto Cosmos Advisors (Odoo 16 devel em `localhost:16069`, banco `devel`, usuário
admin/admin) gera treinamentos para o módulo Knowledge via pipeline de Playwright:

```
cosmos_<modulo>.py  ->  output_<modulo>/*.png + videos/*.gif  ->  tutoriais/0X-<modulo>.md  ->  import_tutorials_to_knowledge.py (XML-RPC)
```

Os scripts usam `cosmos_helpers.py` (sessão persistente em `session_state.json`, helpers
`navigate_to`, `get_logged_in_context`, `convert_all_videos`). O tutorial de Contatos
existente é `tutoriais/04-contatos.md`, com screenshots em `output_contato/`.

Motivação: ver `proposal.md - Why`. Requisitos: ver `specs/tutorials/spec.md`.

## Goals / Non-Goals

**Goals:**

- Novo script Playwright que demonstra a exclusão de contato de forma segura (contato
  demo autocontido)
- Tutorial markdown `06-excluir-contato.md` no mesmo padrão dos demais
- Publicação no Knowledge via import_script

**Non-Goals:**

- Não alterar a UI do Odoo nem criar módulos Odoo
- Não excluir contatos reais do banco de desenvolvimento
- Não refatorar `import_tutorials_to_knowledge.py`, apenas adicionar entrada

## Decisions

### 1. Contato demo autocontido (em vez de excluir registro real)

O script cria um contato único "Contato Demo - Excluir", salva, exclui — o banco termina
sem resíduos e o fluxo é re-rodável. Alternativas rejeitadas: excluir contato existente
(destrutivo, pode ser bloqueado por vínculos em outras app), e excluir um contato criado
em execuções anteriores (complexidade desnecessária).

- Busca pelo nome na lista filtrando antes de abrir, garantindo robustez a duplicatas em
  bancos que já rodaram o fluxo de cadastro.

### 2. Reuso de `cosmos_helpers.py`

O script segue a mesma assinatura dos pares (`get_logged_in_context`, `navigate_to` com
menu_id 111 de Contatos, `convert_all_videos`). Nenhum novo helper é necessário.

### 3. Fluxo de UI para exclusão (Odoo 16)

```
Contatos (menu 111) -> busca pelo nome -> abrir form
  -> engrenagem Ações -> Excluir -> diálogo de confirmação -> Confirmar
  -> volta pra lista sem o contato
```

Screenshots previstas em `output_contato_delete/`: `01_contatos_lista.png`,
`02_busca_contato.png`, `03_form_contato.png`, `04_menu_acoes.png`,
`05_confirmacao_excluir.png`, `06_contato_excluido.png`.

### 4. Tutorial follow o template de `04-contatos.md`

Seções: O que é / Por que / Fluxo passo-a-passo / Fluxo Visual / Screenshots / Boas
práticas / Uso em outros módulos / mermaid.

## Risks / Trade-offs

- [Script depende de estado de helpers (`session_state.json`/login)] → seguir fluxo
  padrão `get_logged_in_context`, com login automático se necessário
- [Diálogo de exclusão pode ter textos diferentes por locale/versão] → usar seletores
  robustos com fallback (`has-text("Excluir")` / `has-text("Delete")`)
- [Contato demo pode conflitar com execuções anteriores] → busca por nome +
  `create_or_update`-like: excluir o que existir antes de recriar, ou usar nome único
