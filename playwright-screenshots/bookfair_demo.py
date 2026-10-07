#!/usr/bin/env python3
"""
Book Fair - Demonstracao em video da loja de colegios (e-commerce Odoo 16).

Gera tres videos em output_bookfair/videos/:
  01_loja_colegio_exemplo.mp4   senha, kit, aluno, termo, carrinho, checkout, frete, pagamento
  02_isolamento_horizonte.mp4   colegio triangular (frete gratis, so boleto e PIX) e kit de outro colegio
  03_administrativo.mp4         pedido feito no backoffice e cadastro do colegio

Pre-requisitos:
  - Odoo em ODOO_URL com o banco `devel` e os colegios de demonstracao
    (senhas exemplo2027 e horizonte2027).
  - Parte 3: session_state.json valido (rode cosmos_session.py antes). O script
    nao digita senha de administrador.

Uso:  python bookfair_demo.py            (sem janela)
      HEADED=1 python bookfair_demo.py   (com janela, para acompanhar)
"""
import asyncio
import os
import re
import sys
from pathlib import Path

from cosmos_helpers import (
    CURSOR_OVERLAY_JS,
    ODOO_URL,
    SESSION_FILE,
    DB,
    convert_webm_to_mp4,
    navigate_to,
)
from cosmos_helpers import human_type as _human_type
from cosmos_helpers import smooth_click as _smooth_click
from playwright.async_api import async_playwright

OUTPUT_DIR = Path("output_bookfair")
VIEWPORT = {"width": 1600, "height": 900}
HEADED = bool(os.environ.get("HEADED"))

SENHA_EXEMPLO = "  EXEMPLO2027 "  # maiusculas e espacos: a senha ignora os dois
SENHA_HORIZONTE = "horizonte2027"

ALUNO_1 = "Maria Souza"
ALUNO_2 = "Pedro Souza"
COMPRADOR = {
    "name": "Ana Souza",
    "email": "ana.souza@example.com",
    "phone": "11999990000",
    "street": "Avenida Brasil, 500",  # diferente do colegio, para mostrar a entrega no colegio
    "city": "Sao Paulo",
    "zip": "01430-000",
}
CPF_INVALIDO = "111.111.111-11"
CPF_VALIDO = "529.982.247-25"


async def pause(seconds=2.5):
    await asyncio.sleep(seconds)


async def _to_center(locator):
    """Rola ate o elemento: os auxiliares usam coordenadas da tela e erram fora da dobra."""
    await locator.first.evaluate("e => e.scrollIntoView({block: 'center'})")
    await asyncio.sleep(0.6)


async def smooth_click(page, locator):
    await _to_center(locator)
    await _smooth_click(page, locator)


async def human_type(page, locator, text, **kwargs):
    await _to_center(locator)
    await _human_type(page, locator, text, **kwargs)


async def new_context(p, name, storage_state=None):
    videos_dir = OUTPUT_DIR / "videos" / name
    videos_dir.mkdir(parents=True, exist_ok=True)
    browser = await p.chromium.launch(headless=not HEADED)
    kwargs = {
        "viewport": VIEWPORT,
        "record_video_dir": str(videos_dir),
        "record_video_size": VIEWPORT,
        "locale": "pt-BR",
    }
    if storage_state:
        kwargs["storage_state"] = str(storage_state)
    context = await browser.new_context(**kwargs)
    page = await context.new_page()
    await page.add_init_script(CURSOR_OVERLAY_JS)
    return browser, context, page


async def finish(browser, context, page, final_name):
    """Fecha o contexto (grava o video) e converte para mp4."""
    video = page.video
    await context.close()
    webm = Path(await video.path())
    target = webm.with_name(final_name + ".webm")
    webm.rename(target)
    mp4 = convert_webm_to_mp4(target)
    await browser.close()
    print(f"  Video: {mp4}")


async def shot(page, name):
    """Captura de apoio; uma falha aqui nao pode derrubar a gravacao."""
    for _ in range(3):
        try:
            await page.wait_for_load_state("load")
            await page.screenshot(path=str(OUTPUT_DIR / f"{name}.png"))
            return
        except Exception:
            await asyncio.sleep(1.5)
    print(f"  Aviso: sem captura {name}")


async def open_store(page, senha, wrong_first=False):
    await page.goto(f"{ODOO_URL}/web/login?db={DB}", wait_until="domcontentloaded")
    await page.goto(f"{ODOO_URL}/", wait_until="networkidle")
    await pause(3)
    campo = page.locator('.bf-access-form input[name="codigo"]')
    botao = page.locator('.bf-access-form button[type="submit"]')
    if wrong_first:
        await human_type(page, campo, "senhaerrada", delay=70)
        await smooth_click(page, botao)
        await page.wait_for_load_state("networkidle")
        await pause(3)  # mensagem "Senha nao encontrada"
        await human_type(page, campo, senha, delay=70, clear=True)
    else:
        await human_type(page, campo, senha, delay=70)
    await smooth_click(page, botao)
    await page.wait_for_url("**/shop")
    await page.wait_for_load_state("networkidle")
    await pause(3)


async def add_kit(page, kit_href, aluno, goto="cart", show_terms=True):
    await page.goto(f"{ODOO_URL}{kit_href}", wait_until="networkidle")
    await pause(2)
    await human_type(page, page.locator("#bf_student_name"), aluno, delay=70)
    await smooth_click(page, page.locator("#bf_terms"))
    if show_terms:
        await page.wait_for_selector("#bf_terms_modal.show")
        await pause(3)  # o termo abre na primeira marcacao
        await smooth_click(page, page.locator("#bf_terms_modal .btn-primary"))
        await pause(1)
    await smooth_click(page, page.locator(f'button[name="goto"][value="{goto}"]'))
    await page.wait_for_load_state("networkidle")
    await pause(2.5)


async def fill_address(page, cpf):
    for field in ("name", "email", "phone"):
        await human_type(page, page.locator(f'input[name="{field}"]'), COMPRADOR[field], delay=45)
    await human_type(page, page.locator('input[name="vat"]'), cpf, delay=45)
    await human_type(page, page.locator('input[name="street"]'), COMPRADOR["street"], delay=45)
    await human_type(page, page.locator('input[name="city"]'), COMPRADOR["city"], delay=45)
    await human_type(page, page.locator('input[name="zip"]'), COMPRADOR["zip"], delay=45)
    await page.select_option('select[name="country_id"]', label="Brasil")
    await pause(1)
    await page.select_option('select[name="state_id"]', label="São Paulo")
    await pause(1)


async def go_next(page):
    await smooth_click(page, page.locator("a.a-submit").last)
    await page.wait_for_load_state("networkidle")
    await pause(2.5)


async def part_store_exemplo(p):
    print("Parte 1: loja do Colegio Exemplo")
    browser, context, page = await new_context(p, "loja")
    await page.goto(f"{ODOO_URL}/web/login?db={DB}", wait_until="domcontentloaded")
    await page.goto(f"{ODOO_URL}/", wait_until="networkidle")
    await pause(4)  # hero "Volta as aulas" com o campo de senha
    await open_store(page, SENHA_EXEMPLO, wrong_first=True)
    await shot(page, "01_loja")

    # navegacao por serie
    await smooth_click(page, page.locator('.bf-grade-nav a:has-text("2º ano")'))
    await page.wait_for_load_state("networkidle")
    await pause(3)
    await smooth_click(page, page.locator('.bf-grade-nav a:has-text("1º ano")'))
    await page.wait_for_load_state("networkidle")
    await pause(2)
    kit_href = await page.locator('a[href*="kit-1o-ano"]').first.get_attribute("href")

    # kit para o primeiro aluno e depois para o segundo
    await add_kit(page, kit_href, ALUNO_1)
    await add_kit(page, kit_href, ALUNO_2, show_terms=False)
    await shot(page, "02_carrinho_dois_alunos")
    await pause(3)  # duas linhas, uma por aluno

    # checkout: CPF invalido primeiro, depois o valido
    await smooth_click(page, page.locator('a:has-text("Processar compra")').first)
    await page.wait_for_load_state("networkidle")
    await pause(2)
    await fill_address(page, CPF_INVALIDO)
    await go_next(page)
    await shot(page, "03_cpf_invalido")
    await pause(2)
    await human_type(page, page.locator('input[name="vat"]'), CPF_VALIDO, delay=45, clear=True)
    await go_next(page)
    await page.wait_for_url("**/shop/payment", timeout=30000)
    await shot(page, "04_pagamento")
    await pause(5)  # entrega no colegio, frete e total antes do pagamento

    # pagamento simulado
    await smooth_click(page, page.locator('label:has-text("PIX (simulado)")'))
    await pause(1.5)
    await smooth_click(page, page.locator('button[name="o_payment_submit_button"]'))
    await page.wait_for_url("**/shop/confirmation", timeout=30000)
    await page.wait_for_load_state("networkidle")
    await pause(4)
    await shot(page, "05_confirmacao")
    texto = await page.inner_text("body")
    pedido = re.search(r"\bS\d{4,}\b", texto)
    await finish(browser, context, page, "01_loja_colegio_exemplo")
    return pedido.group(0) if pedido else None


async def part_isolation(p):
    print("Parte 2: isolamento e colegio triangular")
    browser, context, page = await new_context(p, "isolamento")
    await open_store(page, SENHA_HORIZONTE)
    await shot(page, "06_horizonte")
    await pause(3)
    kit_href = await page.locator('a[href*="kit-1o-ano"]').first.get_attribute("href")

    # kit de outro colegio pelo endereco direto
    await page.goto(f"{ODOO_URL}/shop/kit-1o-ano-colegio-exemplo-2", wait_until="networkidle")
    await pause(4)
    await shot(page, "07_kit_de_outro_colegio")

    # frete gratis e so boleto e PIX
    await add_kit(page, kit_href, ALUNO_1, goto="checkout")
    if "/shop/address" in page.url:
        await fill_address(page, CPF_VALIDO)
        await go_next(page)
    await page.wait_for_url("**/shop/payment", timeout=30000)
    await shot(page, "08_horizonte_pagamento")
    await pause(6)
    await finish(browser, context, page, "02_isolamento_horizonte")


async def part_admin(p, pedido):
    print("Parte 3: administrativo")
    if not SESSION_FILE.exists():
        print("  Sem session_state.json: rode cosmos_session.py antes. Parte 3 ignorada.")
        return
    browser, context, page = await new_context(p, "admin", storage_state=SESSION_FILE)
    await navigate_to(page, f"{ODOO_URL}/web#action=sale.action_quotations_with_onboarding&model=sale.order&view_type=list")
    if "/web/login" in page.url or "/web/database/selector" in page.url or not await page.locator(".o_navbar, .o_main_navbar").count():
        print("  Sessao expirada: rode cosmos_session.py. Parte 3 ignorada.")
        await context.close()
        await browser.close()
        return
    await pause(3)
    for facet in await page.locator(".o_searchview .o_facet_remove").all():
        await facet.click()  # tira o filtro padrao "Minhas cotacoes"
        await pause(0.5)
    await pause(2)  # lista de cotacoes com a coluna Colegio
    await shot(page, "09_admin_lista")
    if pedido:
        busca = page.locator(".o_searchview_input")
        await human_type(page, busca, pedido, delay=70)
        await page.keyboard.press("Enter")
        await pause(2)
    await smooth_click(page, page.locator(".o_data_row .o_data_cell").first)
    await page.wait_for_selector(".o_form_view", timeout=30000)
    await pause(4)  # colegio, tipo de operacao e entrega
    await shot(page, "10_admin_pedido")
    await page.locator(".o_form_sheet_bg").evaluate("e => e.scrollBy(0, 500)")
    await pause(4)  # linhas com aluno e aceite do termo
    await shot(page, "11_admin_linhas")

    await navigate_to(page, f"{ODOO_URL}/web#action=website_sale_bookfair.bookfair_school_action")
    await pause(3)
    await shot(page, "12_admin_colegios")
    await smooth_click(page, page.locator(".o_data_row .o_data_cell").first)
    await page.wait_for_selector(".o_form_view", timeout=30000)
    await pause(3)
    for aba in ("Frete", "Pagamento"):
        link = page.locator(f'.o_notebook a:has-text("{aba}")')
        if await link.count():
            await smooth_click(page, link)
            await pause(4)
    await shot(page, "13_admin_colegio_pagamento")
    await finish(browser, context, page, "03_administrativo")


async def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    only_admin = "admin" in sys.argv[1:]  # python bookfair_demo.py admin
    async with async_playwright() as p:
        pedido = None
        if not only_admin:
            pedido = await part_store_exemplo(p)
            print(f"  Pedido gerado: {pedido}")
            await part_isolation(p)
        if only_admin:
            args = [a for a in sys.argv[1:] if a != "admin"]
            pedido = args[0] if args else None
        await part_admin(p, pedido)
    print("Pronto. Videos em", OUTPUT_DIR / "videos")


if __name__ == "__main__":
    asyncio.run(main())