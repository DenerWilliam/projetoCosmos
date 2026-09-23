## Context

A pipeline de vídeos usa Chromium headless (`cosmos_helpers.py:74`) com
`record_video_dir`. O headless não desenha o cursor do SO. Todos os scripts de tutorial
chamam `get_logged_in_context()` (cosmos_helpers.py:69), que é o ponto único de criação
de página. Requisitos: `specs/mouse-cursor-overlay/spec.md`, motivação em `proposal.md`.

## Goals / Non-Goals

**Goals:**

- Cursor visível (seta) em todos os vídeos/GIFs de tutorial
- Halo animado no ponto de clique
- Uma única mudança em `cosmos_helpers.py`, sem tocar nos scripts individuais
- Zero dependências novas

**Non-Goals:**

- Não alterar o conteúdo/servidor Odoo
- Não criar novo pipeline de gravação (ffmpeg atual permanece)
- Não refatorar script a script (apenas re-geração futura dos vídeos)

## Decisions

### 1. Overlay DOM injetado via `add_init_script` (em vez de pós-processamento ffmpeg)

Injetar um `<div>` de cursor + halo na página via `page.add_init_script()`. O Playwright
dispara eventos `mousemove`/`mousedown` reais no DOM nas ações de clique, então o
overlay acompanha. O vídeo é gravado pela própria tela da página, então captura o cursor
naturalmente.

Alternativas rejeitadas:

- Overlay via ffmpeg pós-gravação: exigiria registrar coordenadas por timestamp —
  complexo e frágil.
- Screenshot compositing: não afeta vídeo.
- Cursor do SO: impossível em headless.

### 2. Aplicação no `get_logged_in_context`

Depois de `page = await context.new_page()` (cosmos*helpers.py:86), registrar o init
script. Assim todos os fluxos herdam o overlay sem alteração em cada `cosmos*\*.py`.

### 3. Design do overlay (estilo A)

- Cursor: div estilizada como seta (ponteiro), `position: fixed`,
  `pointer-events: none`, `z-index` alto. SVG de 52px (antes 24px) com viewBox 24x24
  escalado via `width`/`height` do SVG; a ponta da seta e deslocada para o ponto exato
  via `translate(x - TIP_X, y - TIP_Y)`.
- Halo: div circular que surge e anima (fade/scale) a cada `mousedown`.
- Movimento com interpolacao (lerp): o `mousemove` so atualiza o alvo `{tx, ty}`; um
  loop `requestAnimationFrame` persegue o alvo com fator `EASE = 0.15`. Como o `click()`
  do Playwright dispara um unico `mousemove` no destino final, o lerp e o que transforma
  o aparencia de "teletransporte" em um deslize visivel.
- Halo sincronizado com a chegada: o `mousedown` apenas agenda `pendingHalo`; o loop
  `render` dispara o halo quando a seta chega (dist > 0.5), evitando o anel aparecendo
  antes da seta.
- O init script e pequeno e re-executa a cada `goto` (SPA mantem o elemento pois nao ha
  reload — conforme requisito "Persistencia em navegacao SPA").

### 4. Validação

Rodar `cosmos_contato_delete.py` e verificar no DOM que o overlay existe durante a
execução; conferir visualmente o GIF gerado. Como o modelo não lê imagens, a confirmação
visual final fica com o usuário, mas o DOM check garante injeção correta.

## Risks / Trade-offs

- [Init script pode ser executado antes do DOM do overlay estar acessível no SPA] → usar
  `document`-level listeners; o overlay é criado no `documentElement`, independente da
  view atual
- [Cursor pode permanecer "parado" se navegação SPA não disparar mousemove] → aceitável;
  o próximo clique reposiciona
- [Precisão da seta em alvos distantes] → o lerp com EASE 0.15 leva ~700ms para alvos
  distantes; o halo confirmando a chegada mitiga a percepção de latência
- [Overlay visível em capturas de logotipo/frames iniciais] → menor impacto; pode ser
  aceito como padrão dos tutoriais
- [Mínimo overhead por clique] → animação curta (CSS transition) sem afetar a latência
  de ações subsequentes

## Migration Plan

- Adicionar o snippet e o `add_init_script` em `cosmos_helpers.py`; re-gerar vídeos dos
  tutoriais desejados com os scripts existentes. Rollback: remover o init script
  (reverter o helper).
