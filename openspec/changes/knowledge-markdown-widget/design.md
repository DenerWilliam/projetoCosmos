## Context

O módulo `document_page` do OCA Knowledge (v16) fornece páginas de documentação com
campos `name`, `content` (HTML), `parent_id` (categoria), e metadados. O campo `content`
usa o widget `html` do Odoo (WYSIWYG editor).

O módulo `cosmos_knowledge_markdown` foi desenvolvido internamente para o projeto Cosmos
Advisors e demonstrou viabilidade técnica da conversão Markdown → HTML usando a
biblioteca Python `markdown`.

## Goals / Non-Goals

**Goals:**

- Criar módulo Odoo 16 CE auto-contido para distribuição
- Fornecer editor Markdown com preview em tempo real
- Manter compatibilidade com páginas existentes (não-Markdown)
- Seguir convenções OCA para facilitar contribuição
- Dependência mínima: apenas biblioteca Python `markdown`

**Non-Goals:**

- Suporte a outros formatos (reStructuredText, AsciiDoc)
- Editor JavaScript rich-text para Markdown
- Sincronização bidirecional Markdown ↔ HTML
- Suporte a Odoo 15 ou versões anteriores
- Integração com editores externos (VS Code, etc.)

## Decisions

### 1. Estrutura do módulo

**Decisão**: Criar módulo `knowledge_markdown` em vez de estender
`cosmos_knowledge_markdown`

**Razão**:

- `cosmos_knowledge_markdown` tem dependências do projeto Cosmos
- Módulo distribuível deve ser independente
- Nome mais genérico e descritivo

**Alternativas consideradas**:

- Publicar `cosmos_knowledge_markdown` → Rejeitado por dependências específicas
- Criar módulo genérico `markdown_widget` → Rejeitado por ser muito amplo

### 2. Conversão Markdown → HTML

**Decisão**: Usar biblioteca Python `markdown` com extensões (extra, codehilite, toc)

**Razão**:

- Biblioteca madura e bem mantida
- Extensões fornecem tabelas, código com syntax highlighting, sumário
- Conversão server-side garante consistência

**Alternativas consideradas**:

- JavaScript (marked.js) → Rejeitado: conversão client-side menos confiável
- Custom parser → Rejeitado: reinventar a roda

### 3. Interface do formulário

**Decisão**: Notebook com 3 abas (Markdown, Preview, HTML Final)

**Razão**:

- Separa claramente edição de visualização
- Preview permite verificar antes de salvar
- HTML Final mostra o que realmente é salvo
- Componente nativo do Odoo (sem JavaScript custom)

**Alternativas consideradas**:

- Split view (lado a lado) → Rejeitado: espaço insuficiente
- Modal de preview → Rejeitado: interrupção do fluxo
- Toggle Markdown/Preview → Rejeitado: menos intuitivo

### 4. Sincronização de dados

**Decisão**: Atualizar campo `content` nos métodos `create` e `write`

**Razão**:

- Garante que HTML está sempre disponível
- Compatível com relatórios e exports
- Não depende de triggers ou cron jobs

**Alternativas consideradas**:

- Compute sempre → Rejeitado: performance e complexidade
- Lazy update → Rejeitado: inconsistência potencial

## Risks / Trade-offs

**[Risco] Performance com páginas grandes** → Mitigação: Usar compute dependente de
`markdown_content` apenas

**[Risco] Conflito com outros módulos** → Mitigação: Usar herança leve (\_inherit) e
prioridade alta

**[Risco] Dependência Python não instalada** → Mitigação: Verificar no manifest e
mensagem de erro clara

**[Risco] Perda de dados HTML existentes** → Mitigação: Não sobrescrever campo `content`
se `markdown_content` estiver vazio

**[Trade-off] Flexibilidade vs Simplicidade** → Escolhemos simplicidade: conversão
automática sem opções avançadas

## Migration Plan

1. **Instalação**: `pip install markdown` no ambiente Odoo
2. **Deploy**: Instalar módulo via Apps ou linha de comando
3. **Dados**: Nenhuma migração necessária - páginas existentes funcionam normalmente
4. **Rollback**: Desinstalar módulo - campos customizados permanecem mas não são
   exibidos

## Open Questions

- Nenhuma questão aberta - todas as decisões foram tomadas
