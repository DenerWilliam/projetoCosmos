#!/usr/bin/env python3
"""
Book Fair - Etapa 1 do video: como a equipe cadastra um colegio e um kit.

Gera em output_bookfair/videos/:
  etapa1_cadastro/01_cadastro_colegio_e_kit.mp4   (admin)
  etapa1_cadastro/02_loja_do_colegio_novo.mp4     (visitante, com a senha recem-criada)

Cria o "Colegio Aurora" e o kit dele ao vivo. Antes de gravar, apaga o que uma
execucao anterior deixou (cleanup). Precisa de session_state.json valido
(cosmos_session.py). Uso:  python bookfair_etapa1_cadastro.py   (HEADED=1 para ver)
"""
import asyncio
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import bookfair_demo as demo  # noqa: E402
from bookfair_demo import (  # noqa: E402
    DB,
    ODOO_URL,
    SESSION_FILE,
    finish,
    human_type,
    navigate_to,
    new_context,
    pause,
    shot,
    smooth_click,
)
from playwright.async_api import async_playwright  # noqa: E402

COMPOSE_DIR = Path.home() / "Documentos/Escodoo/Templates/Odoo16/odoo"
NOME = "Colégio Aurora"
SENHA = "aurora2027"
KIT = "Kit 1º ano - Colégio Aurora"

CLEANUP = """
S = env["bookfair.school"].with_context(active_test=False).search([("name", "=", "Colégio Aurora")])
K = env["product.template"].with_context(active_test=False).search([("name", "=", "Kit 1º ano - Colégio Aurora")])
orders = env["sale.order"].with_context(active_test=False).search([("bookfair_school_id", "in", S.ids)])
orders.transaction_ids.unlink()
for o in orders.filtered(lambda o: o.state not in ("draft", "cancel")):
    o._action_cancel()
moves = env["stock.move"].search([("product_id", "in", K.product_variant_ids.ids)]) | orders.picking_ids.move_ids
pickings = moves.picking_id
for pk in pickings.filtered(lambda pk: pk.state not in ("draft", "cancel")):
    pk.action_cancel()
(moves.filtered(lambda m: not m.picking_id)).write({"state": "cancel"})
moves.filtered(lambda m: not m.picking_id).unlink()
pickings.unlink()
orders.unlink()
env["mrp.bom"].with_context(active_test=False).search([("product_tmpl_id", "in", K.ids)]).unlink()
K.unlink()
pl = S.pricelist_id
partner = S.partner_id
S.unlink()
pl.unlink()
partner.unlink()
env.cr.commit()
print("LIMPO", len(orders))
"""


def cleanup():
    """Remove o colegio e o kit criados por uma execucao anterior."""
    result = subprocess.run(
        ["docker", "compose", "exec", "-T", "odoo", "odoo", "shell", "-d", DB,
         "--http-port=18071", "--gevent-port=18074", "--workers=0"],
        input=CLEANUP, text=True, capture_output=True, cwd=COMPOSE_DIR,
    )
    print("  Limpeza:", "ok" if "LIMPO" in result.stdout else result.stderr[-300:])


async def wait_form(page):
    await page.wait_for_selector(".o_form_view", timeout=30000)
    await pause(1.5)


async def m2o(page, field, text, create=False):
    """Preenche um campo de relacao: digita e escolhe a opcao (ou cria)."""
    campo = page.locator(f'div[name="{field}"] input')
    await human_type(page, campo, text, delay=70)
    await page.wait_for_selector(".ui-autocomplete", timeout=10000)
    await pause(1)
    if create:
        opcao = page.locator(".ui-autocomplete li.o_m2o_dropdown_option_create a").first
    else:
        opcao = page.locator(".ui-autocomplete li a", has_text=text).first
    await smooth_click(page, opcao)
    await pause(1)


async def tab(page, nome, seconds=3):
    await smooth_click(page, page.locator(f'.o_notebook a:has-text("{nome}")'))
    await pause(seconds)


async def part_admin(p):
    print("Etapa 1a: cadastro no administrativo")
    browser, context, page = await new_context(p, "etapa1_cadastro", storage_state=SESSION_FILE)
    await navigate_to(page, f"{ODOO_URL}/web#action=website_sale_bookfair.bookfair_school_action&view_type=list")
    await page.wait_for_selector(".o_list_view", timeout=30000)
    await pause(3)  # colegios ja cadastrados
    await shot(page, "e1_01_lista")

    # novo colegio
    await smooth_click(page, page.locator("button.o_list_button_add"))
    await wait_form(page)
    await m2o(page, "partner_id", NOME, create=True)
    await human_type(page, page.locator('div[name="access_code"] input'), SENHA, delay=70)
    await page.select_option('div[name="operation_type"] select', label="Operação Book Fair")
    await pause(1)
    await human_type(page, page.locator('div[name="discount_percent"] input'), "3", delay=120, clear=True)
    await human_type(page, page.locator('div[name="street"] input'), "Rua das Acácias, 120", delay=60)
    await human_type(page, page.locator('div[name="city"] input'), "Mogi das Cruzes", delay=60)
    await human_type(page, page.locator('div[name="zip"] input'), "08830-000", delay=70)
    await m2o(page, "country_id", "Brasil")
    await m2o(page, "state_id", "São Paulo")
    await shot(page, "e1_02_dados")
    await pause(2)

    # frete por data
    await tab(page, "Frete", 1)
    await smooth_click(page, page.locator('.o_field_x2many_list_row_add a'))
    await pause(1)
    await human_type(page, page.locator('.o_data_row .o_data_cell[name="date_from"] input'), "01/01/2026", delay=80)
    await page.keyboard.press("Tab")
    await human_type(page, page.locator('.o_data_row .o_data_cell[name="amount"] input'), "45", delay=100, clear=True)
    await pause(1)
    await smooth_click(page, page.locator('div[name="name"], .o_form_sheet').first)
    await shot(page, "e1_03_frete")
    await pause(3)

    # pagamento
    await tab(page, "Pagamento", 2)
    await smooth_click(page, page.locator('div[name="allow_two_cards"] input'))  # tira "Dois cartões"
    await pause(1.5)
    await smooth_click(page, page.locator('div[name="allow_two_cards"] input'))  # e volta
    await human_type(page, page.locator('div[name="installments_first_reduction"] input'), "21/03/2027", delay=80)
    await page.keyboard.press("Enter")
    await pause(1)
    await smooth_click(page, page.locator('div[name="two_cards_rule_ids"] .o_field_x2many_list_row_add a'))
    await pause(1)
    await human_type(page, page.locator('.o_data_row .o_data_cell[name="amount_from"] input'), "500", delay=100, clear=True)
    await page.keyboard.press("Tab")
    await human_type(page, page.locator('.o_data_row .o_data_cell[name="min_installments"] input'), "3", delay=100, clear=True)
    await smooth_click(page, page.locator(".o_form_sheet").first)
    await shot(page, "e1_04_pagamento")
    await pause(4)

    # comunicado
    await tab(page, "Comunicado", 1)
    editor = page.locator('div[name="notice"] .odoo-editor-editable, div[name="notice"] .note-editable').first
    await human_type(page, editor, "Pedidos até o dia 10 entram no primeiro lote de entrega.", delay=45)
    await pause(2)

    # salvar
    await smooth_click(page, page.locator("button.o_form_button_save"))
    await pause(3)
    await shot(page, "e1_05_salvo")

    # series
    await smooth_click(page, page.locator('.o_menu_sections a:has-text("Séries")'))
    await page.wait_for_selector(".o_list_view", timeout=30000)
    await pause(4)
    await shot(page, "e1_06_series")

    # kit novo
    await navigate_to(page, f"{ODOO_URL}/web#action=sale.product_template_action&view_type=list")
    await page.wait_for_selector(".o_list_view", timeout=30000)
    await smooth_click(page, page.locator("button.o_list_button_add"))
    await wait_form(page)
    await human_type(page, page.locator('div[name="name"] input'), KIT, delay=60)
    await human_type(page, page.locator('div[name="list_price"] input'), "280", delay=100, clear=True)
    await m2o(page, "school_id", NOME)
    await m2o(page, "grade_id", "1º ano")
    await shot(page, "e1_07_kit")
    await pause(3)
    await smooth_click(page, page.locator("button.o_form_button_save"))
    await pause(3)

    # lista de materiais do kit, cadastrada ao vivo
    await smooth_click(page, page.locator('.oe_stat_button:has-text("Lista")').first)
    await page.wait_for_selector(".o_list_view, .o_form_view", timeout=30000)
    await pause(2)
    if not await page.locator(".o_form_view").count():
        await smooth_click(page, page.locator("button.o_list_button_add"))
        await wait_form(page)
    await smooth_click(page, page.locator('div[name="type"] label:has-text("Kit")').first)
    await pause(1.5)
    for busca in ("Livro de Mat", "Livro de Port", "Caderno univ", "Estojo"):
        await smooth_click(page, page.locator('div[name="bom_line_ids"] .o_field_x2many_list_row_add a'))
        await pause(1)
        campo = page.locator('.o_selected_row .o_data_cell[name="product_id"] input')
        await human_type(page, campo, busca, delay=70)
        await page.wait_for_selector(".ui-autocomplete", timeout=10000)
        await pause(1)
        await smooth_click(page, page.locator(".ui-autocomplete li a").first)
        await pause(1)
    await smooth_click(page, page.locator(".o_form_sheet").first)
    await pause(2)
    await smooth_click(page, page.locator("button.o_form_button_save"))
    await pause(5)  # tipo Kit e os livros e materiais
    await shot(page, "e1_08_lista_materiais")
    await finish(browser, context, page, "01_cadastro_colegio_e_kit")


async def part_store(p):
    print("Etapa 1b: loja do colegio recem-criado")
    browser, context, page = await new_context(p, "etapa1_cadastro")
    await demo.open_store(page, SENHA, wrong_first=False)
    await shot(page, "e1_09_loja_nova")
    await pause(5)
    await finish(browser, context, page, "02_loja_do_colegio_novo")


async def main():
    demo.OUTPUT_DIR.mkdir(exist_ok=True)
    cleanup()
    async with async_playwright() as p:
        await part_admin(p)
        await part_store(p)
    print("Pronto. Videos em", demo.OUTPUT_DIR / "videos" / "etapa1_cadastro")


if __name__ == "__main__":
    asyncio.run(main())
