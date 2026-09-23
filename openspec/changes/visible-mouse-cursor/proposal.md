## Why

Os vídeos/GIFs gravados pelos scripts Playwright (headless) não mostram o cursor do
mouse, porque o Chromium headless não renderiza o ponteiro do SO. Isso dificulta o
acompanhamento dos fluxos nos tutoriais, especialmente para indicar **onde** o usuário
clicou — essencial em passo-a-passo.

## What Changes

- **Injetar overlay de cursor via JS** em `playwright-screenshots/cosmos_helpers.py`: um
  cursor estilo "seta" que segue o `mousemove` real do Playwright dentro da página,
  visível na gravação.
- **Halo de clique**: animação circular no ponto do `mousedown`, destacando exatamente
  onde o usuário clicou.
- **Aplicado via `page.add_init_script`** no `get_logged_in_context` — ponto único que
  afeta **todos** os scripts de tutorial (novos e re-gerações), sem tocar em cada script
  individualmente.
- **Zero dependências novas**: mesmo Playwright + ffmpeg já usados; o cursor é DOM
  injetado, capturado nativamente na gravação (vídeo e GIF).

## Capabilities

### New Capabilities

- `mouse-cursor-overlay`: Overlay de cursor (seta + halo de clique) injetado nas
  gravações de vídeo dos tutoriais, tornando o ponteiro e o ponto de clique visíveis no
  conteúdo gravado.

### Modified Capabilities

- Nenhuma — a spec `tutorials` do outro change ainda está em trânsito (não arquivada),
  então não há spec em `openspec/specs/` a modificar.

## Impact

- **Código afetado**:
  - `playwright-screenshots/cosmos_helpers.py` — adicionar `CURSOR_OVERLAY_JS` +
    `add_init_script` em `get_logged_in_context`
- **Dependências**: nenhuma nova (Playwright, ffmpeg, Odoo devel existentes).
- **Compatibilidade**:
  - Sem mudança de comportamento dos scripts — só o visual dos vídeos passa a ter cursor
  - `pointer-events: none` no overlay garante que o cursor não intercepte cliques do
    Playwright
  - Persiste nas navegações SPA do Odoo (mudança de view via hash não recarrega a
    página)
- **Verificação**: rodar um script existente (ex. `cosmos_contato_delete.py`) e
  confirmar que o overlay está no DOM / aparece no GIF gerado.
