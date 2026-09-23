## Purpose

Capacidade de gerar e publicar treinamentos no Odoo Knowledge a partir de fluxos de UI
gravados via Playwright, incluindo screenshots, GIFs, markdown e importação por XML-RPC.

## ADDED Requirements

### Requirement: Geração de treinamento de exclusão de contato

O sistema SHALL permitir gerar um treinamento de "Excluir Contato" na mesma pipeline dos
demais (`cosmos_contato.py` → `tutoriais/*.md` → `import_tutorials_to_knowledge.py`).

O script SHALL criar um contato demo descartável, registrar o fluxo de exclusão
(screenshots numeradas + vídeo/GIF) e terminar com o banco sem o contato demo.

#### Scenario: Fluxo completo de exclusão gravado

- **WHEN** o script `cosmos_contato_delete.py` é executado contra o Odoo devel
- **THEN** ele cria um contato demo "Contato Demo - Excluir"
- **AND** grava screenshots numeradas de lista, formulário, menu de ações, diálogo de
  confirmação e lista final
- **AND** grava vídeo que é convertido em GIF
- **AND** exclui o contato demo no final

#### Scenario: Banco termina limpo

- **WHEN** o script termina
- **THEN** nenhum registro de contato demo permanece no banco `devel`

#### Scenario: Re-rodável

- **WHEN** o script é executado novamente com o banco no estado padrão
- **THEN** ele funciona sem conflitos nem duplicatas

### Requirement: Publicação do treinamento no Knowledge

O tutorial gerado SHALL ser publicado no módulo Knowledge sob a categoria "Tutoriais",
via `import_tutorials_to_knowledge.py`.

#### Scenario: Importação do novo tutorial

- **WHEN** `import_tutorials_to_knowledge.py` é executado
- **THEN** a página "Tutorial: Contatos - Exclusao de Contato" existe sob a categoria
  "Tutoriais"
- **AND** contém o conteúdo markdown do arquivo `06-excluir-contato.md`
