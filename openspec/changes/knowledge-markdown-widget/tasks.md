## 1. Estrutura do Módulo

- [x] 1.1 Criar estrutura de diretórios do módulo `knowledge_markdown` com arquivos
      básicos (**init**.py, **manifest**.py)
- [x] 1.2 Criar diretório models/ com **init**.py e model.py
- [x] 1.3 Criar diretório views/ com view.xml
- [x] 1.4 Criar diretório data/ com dados iniciais (se necessário)

## 2. Modelo de Dados

- [x] 2.1 Implementar modelo DocumentPage com herança (\_inherit = 'document.page')
- [x] 2.2 Adicionar campo markdown_content (Text) com help text
- [x] 2.3 Adicionar campo html_preview (Html) com compute dependente
- [x] 2.4 Implementar método \_convert_markdown_to_html() com biblioteca markdown
- [x] 2.5 Implementar método \_compute_html_preview() usando dependência de
      markdown_content
- [x] 2.6 Sobrescrever create() para converter markdown_content → content
- [x] 2.7 Sobrescrever write() para converter markdown_content → content
- [x] 2.8 Implementar onchange para preview em tempo real

## 3. Interface do Usuário

- [x] 3.1 Criar view herdada com notebook (3 abas: Markdown, Preview, HTML Final)
- [x] 3.2 Configurar campo markdown_content com widget text e placeholder
- [x] 3.3 Configurar campo html_preview com widget html e readonly
- [x] 3.4 Configurar campo content com widget html e options safe
- [x] 3.5 Testar interface em modo visualização e edição

## 4. Manifest e Dependências

- [x] 4.1 Criar **manifest**.py com metadados (name, version, author, license)
- [x] 4.2 Adicionar dependência 'document_page' no depends
- [x] 4.3 Adicionar external_dependencies para python: markdown
- [x] 4.4 Adicionar data files no data
- [x] 4.5 Configurar license AGPL-3

## 5. Documentação

- [x] 5.1 Criar README.md com instruções de instalação
- [x] 5.2 Documentar dependências Python
- [x] 5.3 Adicionar exemplos de uso
- [x] 5.4 Documentar compatibilidade (Odoo 16 CE)

## 6. Testes

- [x] 6.1 Testar instalação do módulo em ambiente limpo
- [ ] 6.2 Testar criação de página com markdown
- [ ] 6.3 Testar atualização de página existente
- [ ] 6.4 Testar conversão de markdown para HTML
- [ ] 6.5 Testar preview em tempo real
- [ ] 6.6 Testar compatibilidade com páginas não-markdown
- [ ] 6.7 Testar comportamento sem biblioteca markdown instalada

## 7. Distribuição

- [x] 7.1 Verificar estrutura segue convenções OCA
- [x] 7.2 Adicionar LICENSE file
- [ ] 7.3 Criar pacote para distribuição (zip ou git)
- [ ] 7.4 Testar instalação em ambiente externo
