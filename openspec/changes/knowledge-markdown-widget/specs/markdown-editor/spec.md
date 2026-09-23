## Purpose

O módulo knowledge_markdown fornece suporte a Markdown para o módulo Knowledge do Odoo,
permitindo que usuários editem conteúdo em formato Markdown com preview em tempo real e
conversão automática para HTML.

## ADDED Requirements

### Requirement: Markdown content field

O sistema SHALL fornecer um campo `markdown_content` do tipo Text para edição de
conteúdo em formato Markdown.

#### Scenario: User edits markdown content

- **WHEN** o usuário abre uma página Knowledge no modo de edição
- **THEN** o sistema exibe uma aba "Markdown" com um campo de texto monospace para
  edição

#### Scenario: Markdown placeholder text

- **WHEN** o campo markdown_content está vazio
- **THEN** o sistema exibe um placeholder com exemplos de sintaxe Markdown

### Requirement: HTML preview computation

O sistema SHALL compute automaticamente o campo `html_preview` quando o campo
`markdown_content` é alterado.

#### Scenario: Live preview update

- **WHEN** o usuário digita texto no campo markdown_content
- **THEN** o campo html_preview é atualizado com o HTML renderizado

#### Scenario: Markdown to HTML conversion

- **WHEN** o conteúdo markdown é convertido para HTML
- **THEN** o sistema usa a biblioteca Python `markdown` com extensões extra, codehilite
  e toc

### Requirement: Automatic content synchronization

O sistema SHALL sincronizar automaticamente o campo `content` (HTML) quando o campo
`markdown_content` é salvo.

#### Scenario: Create with markdown

- **WHEN** uma nova página é criada com markdown_content preenchido
- **THEN** o campo content é preenchido com o HTML convertido

#### Scenario: Write with markdown

- **WHEN** uma página existente é atualizada com novo markdown_content
- **THEN** o campo content é atualizado com o HTML convertido

### Requirement: Tabbed form interface

O sistema SHALL exibir o formulário de edição com 3 abas: Markdown, Preview e HTML
Final.

#### Scenario: Markdown tab

- **WHEN** o usuário clica na aba "Markdown"
- **THEN** o sistema exibe o campo markdown_content com fonte monospace

#### Scenario: Preview tab

- **WHEN** o usuário clica na aba "Preview"
- **THEN** o sistema exibe o campo html_preview com o HTML renderizado

#### Scenario: HTML Final tab

- **WHEN** o usuário clica na aba "HTML Final"
- **THEN** o sistema exibe o campo content com o HTML salvo no banco

### Requirement: Python dependency

O sistema SHALL exigir a biblioteca Python `markdown` como dependência externa.

#### Scenario: Missing markdown library

- **WHEN** a biblioteca `markdown` não está instalada
- **THEN** o módulo não pode ser instalado e exibe mensagem de erro

### Requirement: Module compatibility

O sistema SHALL ser compatível com o Odoo 16 Community Edition e o módulo
`document_page` do OCA.

#### Scenario: Install on Odoo 16 CE

- **WHEN** o módulo é instalado em um ambiente Odoo 16 CE com document_page
- **THEN** o módulo funciona corretamente sem conflitos

#### Scenario: Coexist with non-markdown pages

- **WHEN** existem páginas Knowledge sem markdown_content
- **THEN** essas páginas continuam funcionando normalmente
