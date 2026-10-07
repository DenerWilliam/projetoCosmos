#!/usr/bin/env python3
"""
Book Fair - Etapa 2 do video: compra no colegio recem-criado e o pedido no backoffice.

Gera em output_bookfair/videos/etapa2_pedido/:
  01_compra_colegio_aurora.mp4     (visitante: senha, kit, aluno, termo, frete, boleto simulado)
  02_pedido_e_entrega.mp4          (admin: pedido, confirmar, entrega com os itens do kit)

Pre-requisito: rodar antes bookfair_etapa1_cadastro.py (cria o Colegio Aurora e o
kit dele) e ter session_state.json valido (cosmos_session.py).
Uso:  python bookfair_etapa2_pedido.py   (HEADED=1 para ver)
"""
import asyncio
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import bookfair_demo as demo  # noqa: E402
from bookfair_demo import (  # noqa: E402
    CPF_VALIDO,
    ODOO_URL,
    SESSION_FILE,
    add_kit,
    fill_address,
    finish,
    go_next,
    human_type,
    navigate_to,
    new_context,
    pause,
    shot,
    smooth_click,
)
from playwright.async_api import async_playwright  # noqa: E402

SENHA = "aurora2027"
ALUNO = "Lucas Pereira"


async def part_store(p):
    print("Etapa 2a: compra no Colegio Aurora")
    browser, context, page = await new_context(p, "etapa2_pedido")
    await demo.open_store(page, SENHA, wrong_first=False)
    await shot(page, "e2_01_loja")
    kit_href = await page.locator('a[href*="kit-1o-ano-colegio-aurora"]').first.get_attribute("href")
    await add_kit(page, kit_href, ALUNO, goto="checkout")
    if "/shop/address" in page.url:
        await fill_address(page, CPF_VALIDO)
        await go_next(page)
    await page.wait_for_url("**/shop/payment", timeout=30000)
    await pause(2)
    await shot(page, "e2_02_pagamento")
    await pause(5)  # entrega no colegio, frete e total antes do pagamento
    await smooth_click(page, page.locator('label:has-text("Boleto (simulado)")'))
    await pause(1.5)
    await smooth_click(page, page.locator('button[name="o_payment_submit_button"]'))
    await page.wait_for_url("**/shop/confirmation", timeout=30000)
    await page.wait_for_load_state("load")
    await pause(4)
    await shot(page, "e2_03_confirmacao")
    texto = await page.inner_text("body")
    pedido = re.search(r"\bS\d{4,}\b", texto)
    await finish(browser, context, page, "01_compra_colegio_aurora")
    return pedido.group(0) if pedido else None


async def part_admin(p, pedido):
    print("Etapa 2b: pedido e entrega no administrativo")
    browser, context, page = await new_context(p, "etapa2_pedido", storage_state=SESSION_FILE)
    await navigate_to(page, f"{ODOO_URL}/web#action=sale.action_quotations_with_onboarding&model=sale.order&view_type=list")
    await page.wait_for_selector(".o_list_view", timeout=30000)
    if "/web/login" in page.url or "/web/database/selector" in page.url:
        print("  Sessao expirada: rode cosmos_session.py.")
        await context.close()
        await browser.close()
        return
    await pause(2)
    for facet in await page.locator(".o_searchview .o_facet_remove").all():
        await facet.click()
        await pause(0.5)
    if pedido:
        await human_type(page, page.locator(".o_searchview_input"), pedido, delay=70)
        await page.keyboard.press("Enter")
        await pause(2)
    await shot(page, "e2_04_lista")
    await smooth_click(page, page.locator(".o_data_row .o_data_cell").first)
    await page.wait_for_selector(".o_form_view", timeout=30000)
    await pause(4)  # colegio, operacao, entrega, aluno, aceite e frete
    await shot(page, "e2_05_pedido")

    # confirmar o pedido
    await smooth_click(page, page.locator('button[name="action_confirm"]').first)
    await page.wait_for_selector('.o_statusbar_status button[data-value="sale"].o_arrow_button_current, .o_statusbar_status .o_arrow_button_current[data-value="sale"]', timeout=30000)
    await pause(3)
    await shot(page, "e2_06_confirmado")

    # entrega gerada: os itens do kit saem do estoque
    await smooth_click(page, page.locator('.oe_stat_button:has-text("Entrega")').first)
    await page.wait_for_selector(".o_form_view", timeout=30000)
    await pause(5)
    await shot(page, "e2_07_entrega")
    await finish(browser, context, page, "02_pedido_e_entrega")


async def main():
    demo.OUTPUT_DIR.mkdir(exist_ok=True)
    async with async_playwright() as p:
        pedido = await part_store(p)
        print(f"  Pedido gerado: {pedido}")
        await part_admin(p, pedido)
    print("Pronto. Videos em", demo.OUTPUT_DIR / "videos" / "etapa2_pedido")


if __name__ == "__main__":
    asyncio.run(main())
