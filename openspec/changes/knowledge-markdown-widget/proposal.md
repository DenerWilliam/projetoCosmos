## Why

O módulo `document_page` do OCA Knowledge não oferece suporte nativo a Markdown.
Usuários que preferem escrever em Markdown precisam de uma solução que permita:

1. Editar conteúdo em formato Markdown dentro do Odoo
2. Visualizar o preview renderizado em tempo real
3. Armazenar o HTML resultante para compatibilidade com o sistema

Atualmente, a única opção é usar o editor HTML WYSIWYG, que não é ideal para
documentação técnica ou conteúdo estruturado.

## What Changes

- **Novo módulo `knowledge_markdown`**: Módulo Odoo 16 CE que estende `document_page`
  com suporte a Markdown
- **Campo `markdown_content`**: Campo Text para edição em Markdown com fonte monospace
- **Campo `html_preview`**: Campo computado que mostra o HTML renderizado
- **Conversão automática**: Markdown é convertido para HTML ao salvar (create/write)
- **Formulário com abas**: Notebook com 3 abas (Markdown, Preview, HTML Final)
- **Dependência Python**: Biblioteca `markdown` com extensões extra, codehilite, toc

## Capabilities

### New Capabilities

- `markdown-editor`: Editor de Markdown para o módulo Knowledge do Odoo, incluindo
  campos, conversão automática e interface com abas

### Modified Capabilities

- Nenhuma capacidade existente é modificada - o módulo é independente

## Impact

- **Código afetado**: Novo módulo em `odoo/custom/src/private/knowledge_markdown/`
- **Dependências**:
  - Odoo 16 CE
  - OCA `document_page` (módulo base)
  - Python `markdown` library
- **Compatibilidade**:
  - Não quebra funcionalidade existente
  - Compatível com páginas Markdown e não-Markdown
  - HTML gerado é compatível com o widget `html` do Odoo
- **Instalação**: Módulo auto-contido, pode ser distribuído independentemente
