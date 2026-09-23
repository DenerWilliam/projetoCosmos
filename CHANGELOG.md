# Changelog

## [Unreleased]

### Added

- Overlay de cursor animado (seta + halo de clique) nas gravações de vídeo dos tutoriais
  Playwright (Cosmos)
- Suporte a interpolação (lerp) no movimento do cursor: a seta desliza suavemente até o
  destino em vez de "teletransportar"
- Halo de clique sincronizado com a chegada da seta ao ponto alvo
- Helper `smooth_click` em `cosmos_helpers.py`: move o mouse do Playwright de forma
  interpolada até o alvo (mousemove reais progressivos), pausa, e só então dispara
  `mouse.down/up` — nas gravações a seta chega ao destino **antes** do clique,
  eliminando o efeito "clique primeiro, seta depois"
- Movimento do cursor com Ease-In-Out (começa devagar, acelera e desacelera) e delay
  aleatório de 0.01–0.02s entre passos, simulando movimento humano em vez de varredura
  linear robótica
- Helper `human_type` em `cosmos_helpers.py`: move a seta até o campo, clica e digita o
  texto caractere por caractere com delay por tecla (padrão 80ms), substituindo o
  `.fill()` instantâneo — opção `clear=True` limpa o campo antes de digitar

### Fixed

- Seta do cursor ficava invisível nas gravações: a visibilidade era controlada por
  `element.style.opacity`, que retorna `''` (não `'0'`) para estilos vindos da
  `<style>`, mantendo o `opacity: 0` do CSS. Agora é usada uma flag `shown` no loop de
  renderização.
- Seta se movia depois/saltava no clique: `click()` do Playwright é instantâneo.
  Substituído nos tutoriais por `smooth_click`, que interpola o movimento com
  `page.mouse.move` e aguarda a chegada antes de clicar.

### Changed

- Tamanho do cursor aumentado de 24px para 52px para nitidez nos GIFs reduzidos
- Qualidade da conversão MP4 → GIF melhorada: dithering `sierra2_4a` (substitui
  `bayer`), paleta de 192 cores com `lanczos`
- Todos os tutoriais de vídeo (`cosmos_contato`, `cosmos_contato_delete`, `cosmos_lead`,
  `cosmos_nota`, `cosmos_helpdesk`, `cosmos_all`) agora preenchem formulários com
  `human_type` e clicam com `smooth_click`, uniformizando o visual humano do cursor em
  todas as gravações
