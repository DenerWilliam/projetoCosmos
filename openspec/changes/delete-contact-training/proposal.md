## Why

A equipe usa o módulo Knowledge do Odoo para treinar usuários, e o repositório já tem
uma pipeline para gerar treinamentos a partir de scripts Playwright (ver
`playwright-screenshots/cosmos_*.py`, `tutoriais/*.md` e
`import_tutorials_to_knowledge.py`). Hoje existem 5 treinamentos (CRM, Helpdesk,
Faturamento, Contatos, Projetos). Falta um treinamento de **como excluir um contato**,
que é um fluxo administrativo comum e destrutivo que os usuários precisam conhecer com
segurança.

## What Changes

- **Novo script `cosmos_contato_delete.py`**: Fluxo Playwright que cria um contato demo
  descartável, salva, e então o exclui capturando screenshots e vídeo — termina com o
  banco limpo e é re-rodável.
- **Nova pasta `output_contato_delete/`**: Screenshots numeradas (lista, formulário,
  menu de ações, diálogo de confirmação, lista sem o contato) + GIFs.
- **Nova página `tutoriais/06-excluir-contato.md`**: Tutorial no mesmo padrão dos outros
  (formato, tabelas, "por que", boas práticas, mermaid).
- **Entrada nova em `import_tutorials_to_knowledge.py`**: adicionar o tutorial à lista
  `TUTORIALS` para import na categoria "Tutoriais".
- **Atualização do `playwright-screenshots/tutoriais/README.md`**: tabela de módulos e
  árvore de arquivos.

## Capabilities

### New Capabilities

- `tutorials`: Pipeline de geração e publicação de treinamentos no Odoo Knowledge a
  partir de fluxos de UI gravados via Playwright (scripts, screenshots, GIFs, markdown e
  import via XML-RPC).

### Modified Capabilities

- Nenhuma — o projeto ainda não possui specs (`openspec list --specs` vazio).

## Impact

- **Código afetado**:
  - `playwright-screenshots/cosmos_contato_delete.py` (novo)
  - `playwright-screenshots/tutoriais/06-excluir-contato.md` (novo)
  - `playwright-screenshots/output_contato_delete/` (novo, gerado)
  - `import_tutorials_to_knowledge.py` (modificado, +1 entrada)
  - `playwright-screenshots/tutoriais/README.md` (modificado)
- **Dependências**: Playwright, ffmpeg (já usados), Odoo devel em `localhost:16069` com
  banco `devel`.
- **Compatibilidade**: Não altera módulos Odoo; é aditivo à pipeline existente.
- **Segurança**: O contato excluído é criado pelo próprio script (dados demo), evitando
  apagar registros reais do banco de desenvolvimento.
