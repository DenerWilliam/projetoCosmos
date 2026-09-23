# Changelog

## [Unreleased]

### Added

- Overlay de cursor animado (seta + halo de clique) nas gravações de vídeo dos tutoriais
  Playwright (Cosmos)
- Suporte a interpolação (lerp) no movimento do cursor: a seta desliza suavemente até o
  destino em vez de "teletransportar"
- Halo de clique sincronizado com a chegada da seta ao ponto alvo

### Changed

- Tamanho do cursor aumentado de 24px para 52px para nitidez nos GIFs reduzidos
- Qualidade da conversão MP4 → GIF melhorada: dithering `sierra2_4a` (substitui
  `bayer`), paleta de 192 cores com `lanczos`
