## 1. Script Playwright

- [ ] 1.1 Criar `playwright-screenshots/cosmos_contato_delete.py` reutilizando
      `cosmos_helpers.py` (sessão persistente, `navigate_to` menu 111,
      `convert_all_videos`), com `OUTPUT_DIR = Path("output_contato_delete")` e
      verificar que o arquivo importa sem erros
- [ ] 1.2 Implementar fluxo: criar contato "Contato Demo - Excluir" (reaproveitando
      seletores do `cosmos_contato.py`), salvar, limpar pendências antigas do contato
      demo antes de recriar e verificar que o contato aparece na lista
- [ ] 1.3 Implementar fluxo de exclusão: abrir o contato, engrenagem Ações → Excluir
      (seletores com fallback `Excluir`/`Delete`), confirmar diálogo e verificar que sai
      da lista

## 2. Execução e artefatos

- [ ] 2.1 Executar `python cosmos_contato_delete.py` em `playwright-screenshots/` e
      verificar que gera screenshots numeradas em `output_contato_delete/` (06
      imagens) + GIF convertido
- [ ] 2.2 Verificar via UI/banco que o contato "Contato Demo - Excluir" não permanece no
      banco `devel` após a execução

## 3. Tutorial markdown

- [ ] 3.1 Criar `playwright-screenshots/tutoriais/06-excluir-contato.md` seguindo o
      template de `04-contatos.md` (formato, tabelas, "por que", boas práticas, fluxo
      visual, mermaid) referenciando as screenshots geradas

## 4. Publicação e inventário

- [ ] 4.1 Adicionar entrada em `import_tutorials_to_knowledge.py` (arquivo, nome
      "Tutorial: Contatos - Exclusao de Contato", categoria "Tutoriais") e atualizar
      `tutoriais/README.md` (tabela 04/05 + árvore de arquivos + 06)
- [ ] 4.2 Executar `python import_tutorials_to_knowledge.py` e verificar que a página
      existe sob "Tutoriais" no Knowledge com o conteúdo markdown correto
