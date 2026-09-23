## 1. Overlay de cursor

- [x] 1.1 Adicionar em `cosmos_helpers.py` o construtor do overlay (constante
      `CURSOR_OVERLAY_JS` com cursor-seta + halo de clique, `pointer-events:none`,
      escutando `mousemove` e `mousedown`) e verificar que o arquivo importa sem erros
- [x] 1.2 Chamar `page.add_init_script(CURSOR_OVERLAY_JS)` no `get_logged_in_context`
      após criar a página e verificar que o snippet é registrado (log/inspections sem
      falha)
- [x] 1.3 Confirmar que o overlay não bloqueia cliques: rodar um script simples de
      navegação com o cursor ativo e verificar que ações `click()` completam normalmente

## 2. Validação em vídeo

- [ ] 2.1 Executar `cosmos_contato_delete.py` (que gera screenshots + GIF) e verificar
      que o overlay está presente no DOM durante a execução
- [ ] 2.2 Gerar/atualizar o GIF e conferir visualmente que a seta acompanha o mouse e o
      halo aparece nos cliques (validação visual com o usuário)
- [ ] 2.3 Confirmar que a seta desliza (interpolação) até o destino em vez de
      "teletransportar" — verificar frames intermediários no GIF/MP4
- [ ] 2.4 Confirmar que a seta ficou maior (52px vs 24px) e permanece nítida após a
      redução da resolução para GIF
