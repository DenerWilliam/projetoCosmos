## Purpose

Torna o ponteiro do mouse visível nas gravações de vídeo dos tutoriais do Cosmos
(gravadas via Playwright headless), com uma seta que segue o mouse e um halo que destaca
o ponto de cada clique.

## ADDED Requirements

### Requirement: Cursor visivel nas gravacoes

O sistema de captura de video dos tutoriais SHALL exibir um cursor (seta) visivel nos
videos e GIFs gravados, que acompanha os movimentos do mouse realizados durante o fluxo
automatizado.

O cursor SHALL nao interferir nas acoes do Playwright (nao interceptar cliques) e SHALL
permanecer visivel ao trocar de tela dentro da navegacao SPA do Odoo.

#### Scenario: Seta segue o mouse durante a gravacao

- **WHEN** o script Playwright executa movimentos de mouse (ex. `click`) e grava video
- **THEN** a seta aparece no video gerado
- **AND** posiciona-se no ponto do cursor a cada movimento
- **AND** desliza suavemente (interpolacao) do local anterior ate o destino, sem
  "teletransporte"
- **AND** a seta e grande o suficiente para ser nitida quando o video e reduzido para
  GIF (~52px, o dobro do tamanho original de 24px)

#### Scenario: Overlay nao bloqueia interacoes

- **WHEN** o automatizador clica em um elemento da pagina
- **THEN** o clique atinge o elemento, sem ser interceptado pelo cursor

#### Scenario: Persistencia em navegacao SPA

- **WHEN** o fluxo navega entre telas via mudanca de hash (sem recarregar a pagina)
- **THEN** o overlay de cursor permanece ativo nas telas seguintes

### Requirement: Halo de clique

O sistema SHALL destacar visualmente o ponto de cada clique em um anel (halo) que
aparece e anima quando o clique ocorre, para orientar o espectador sobre onde a acao
aconteceu.

#### Scenario: Halo no clique

- **WHEN** o automatizador dispara um `mousedown`
- **THEN** um anel visual e exibido no ponto do clique no video gravado
- **AND** o anel surge quando a seta chega ao destino (sincronizado com a chegada, nao
  imediatamente no disparo)
