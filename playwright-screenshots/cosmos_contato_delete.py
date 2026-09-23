#!/usr/bin/env python3
"""
Cosmos Advisors - Fluxo de Exclusao de Contato (sessao persistente).
Cria um contato demo, salva e exclui - banco termina limpo.
"""
import asyncio
import xmlrpc.client
from pathlib import Path

from cosmos_helpers import (
    DB,
    ODOO_URL,
    convert_all_videos,
    dismiss_error,
    get_logged_in_context,
    navigate_to,
)
from playwright.async_api import async_playwright

OUTPUT_DIR = Path("output_contato_delete")

DEMO_NAME = "Contato Demo - Excluir"

DEMO_CONTACT = {
    "name": DEMO_NAME,
    "function": "Contato de teste",
    "phone": "+55 11 98765-4321",
    "email": "demo.excluir@cosmos.com.br",
}


def cleanup_pending_demo_contacts():
    """Remove resquicios do contato demo de execucoes anteriores via XML-RPC."""
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    uid = common.authenticate(DB, "admin", "admin", {})
    if not uid:
        print("  WARNING: nao autenticou para cleanup, seguindo sem limpeza")
        return
    models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
    partner_ids = models.execute_kw(
        DB,
        uid,
        "admin",
        "res.partner",
        "search",
        [[["name", "=", DEMO_NAME], ["is_company", "=", False]]],
    )
    if partner_ids:
        models.execute_kw(DB, uid, "admin", "res.partner", "unlink", [partner_ids])
        print(f"  Cleanup: removidos resquicios pendentes: {partner_ids}")
    else:
        print("  Cleanup: nenhum resquicio pendente")


async def create_demo_contact(page):
    print("  Navegando para Contatos...")
    await navigate_to(page, f"{ODOO_URL}/web#menu_id=111")
    await asyncio.sleep(3)
    contacts_link = page.locator('a:has-text("Contacts"), span:has-text("Contacts")')
    if await contacts_link.count() > 0:
        await contacts_link.first.click()
        await asyncio.sleep(5)
    await page.screenshot(
        path=str(OUTPUT_DIR / "01_contatos_lista.png"), full_page=True
    )

    print("  Clicando NOVO...")
    novo_btn = page.locator('button:has-text("NOVO"), button:has-text("New")')
    await novo_btn.first.click()
    await asyncio.sleep(5)

    print("  Selecionando Individual...")
    await page.locator('input[type="radio"]').first.click()
    await asyncio.sleep(1)

    print("  Preenchendo nome...")
    await page.locator(
        'input[placeholder*="Joao"], input[placeholder*="Jo"]'
    ).first.fill(DEMO_CONTACT["name"])
    await asyncio.sleep(0.5)

    print("  Preenchendo cargo...")
    await page.locator(
        'input[placeholder*="Diretor"], input[placeholder*="Job"], input[placeholder*="Function"]'
    ).first.fill(DEMO_CONTACT["function"])
    await asyncio.sleep(0.5)

    print("  Preenchendo telefone...")
    tel_inputs = page.locator('input[type="tel"]')
    if await tel_inputs.count() > 0:
        await tel_inputs.first.fill(DEMO_CONTACT["phone"])
        await asyncio.sleep(0.5)

    print("  Preenchendo email...")
    email = page.locator('input[type="email"]').first
    if await email.count() > 0:
        await email.fill(DEMO_CONTACT["email"])
        await asyncio.sleep(0.5)

    await page.screenshot(path=str(OUTPUT_DIR / "02_form_contato.png"), full_page=True)

    print("  Salvando contato...")
    save_btn = page.locator(
        '.o_form_button_save, button:has-text("Salvar"), button:has-text("Save")'
    )
    if await save_btn.count() > 0:
        await save_btn.first.click()
    else:
        await page.keyboard.press("Control+s")
    await asyncio.sleep(5)
    await page.screenshot(path=str(OUTPUT_DIR / "03_contato_salvo.png"), full_page=True)


async def delete_contact_flow(page):
    print("  Voltando a lista de contatos...")
    await navigate_to(page, f"{ODOO_URL}/web#menu_id=111")
    await asyncio.sleep(3)
    contacts_link = page.locator('a:has-text("Contacts"), span:has-text("Contacts")')
    if await contacts_link.count() > 0:
        await contacts_link.first.click()
        await asyncio.sleep(5)

    print("  Buscando pelo nome...")
    search = page.locator(
        '.o_searchview_input, input[placeholder*="Pesquisar"], input[placeholder*="Search"]'
    ).first
    if await search.count() > 0:
        await search.click()
        await search.fill(DEMO_NAME)
        await page.keyboard.press("Enter")
        await asyncio.sleep(5)
    await page.screenshot(path=str(OUTPUT_DIR / "04_busca_contato.png"), full_page=True)

    print("  Abrindo o contato...")
    contact_row = page.locator(
        f'.o_kanban_record:has-text("{DEMO_NAME}"), .o_data_row:has-text("{DEMO_NAME}"), tr:has-text("{DEMO_NAME}")'
    ).first
    if await contact_row.count() > 0:
        await contact_row.click()
        await asyncio.sleep(5)
    await page.screenshot(
        path=str(OUTPUT_DIR / "05_form_contato_aberto.png"), full_page=True
    )

    print("  Abrindo menu de acoes do registro...")
    actions_btn = page.locator(".fa-cog")
    if await actions_btn.count() > 0:
        await actions_btn.first.click()
        await asyncio.sleep(2)
    await page.screenshot(path=str(OUTPUT_DIR / "06_menu_acoes.png"), full_page=True)

    print("  Clicando Excluir...")
    delete_item = page.locator(
        '.dropdown-item:has-text("Excluir"), '
        '.dropdown-menu a:has-text("Excluir"), '
        '.o-dropdown-menu a:has-text("Excluir"), '
        '.dropdown-menu a:has-text("Delete"), '
        '.dropdown-item:has-text("Delete")'
    ).first
    if await delete_item.count() > 0:
        await delete_item.click()
        await asyncio.sleep(3)
    else:
        print("    WARNING: item Excluir nao encontrado")
    await dismiss_error(page)
    await page.screenshot(
        path=str(OUTPUT_DIR / "07_confirmacao_excluir.png"), full_page=True
    )

    print("  Confirmando exclusao...")
    confirm_btn = page.locator(
        ".modal .btn-primary, "
        '.modal-footer button:has-text("Confirmar"), '
        '.modal-footer button:has-text("Excluir"), '
        '.modal-footer button:has-text("Delete"), '
        '.modal-footer button:has-text("OK")'
    ).first
    if await confirm_btn.count() > 0:
        await confirm_btn.click()
        await asyncio.sleep(5)
    else:
        await page.keyboard.press("Enter")
        await asyncio.sleep(5)
    await dismiss_error(page)

    print("  Voltando a lista (confirmacao extra) ...")
    await navigate_to(page, f"{ODOO_URL}/web#menu_id=111")
    await asyncio.sleep(3)
    contacts_link = page.locator('a:has-text("Contacts"), span:has-text("Contacts")')
    if await contacts_link.count() > 0:
        await contacts_link.first.click()
        await asyncio.sleep(5)
    await page.screenshot(
        path=str(OUTPUT_DIR / "08_contato_excluido.png"), full_page=True
    )


async def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    cleanup_pending_demo_contacts()

    async with async_playwright() as p:
        browser, context, page = await get_logged_in_context(p, OUTPUT_DIR)

        print("Criar contato demo...")
        await create_demo_contact(page)

        print("Excluir contato...")
        await delete_contact_flow(page)

        await context.close()
        await browser.close()

        print("Convertendo videos...")
        convert_all_videos(OUTPUT_DIR / "videos")
        print("Concluido!")


if __name__ == "__main__":
    asyncio.run(main())
