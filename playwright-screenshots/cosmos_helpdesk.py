#!/usr/bin/env python3
"""
Cosmos Advisors - Fluxo de Ticket no Helpdesk (sessao persistente, sem login).
"""
import asyncio
from pathlib import Path

from cosmos_helpers import (
    ODOO_URL,
    convert_all_videos,
    get_logged_in_context,
    navigate_to,
)
from playwright.async_api import async_playwright

OUTPUT_DIR = Path("output_helpdesk")
TICKET = {
    "subject": "Duvida sobre Integracao ERP",
    "description": "Cliente gostaria de saber sobre a integracao do sistema ERP com o modulo financeiro para automatizacao de processos contabeis.",
    "customer": "Cosmos Advisors",
}


async def create_ticket_flow(page, ticket):
    print("  Navegando para Helpdesk...")
    await navigate_to(page, f"{ODOO_URL}/web#menu_id=300")
    await asyncio.sleep(3)

    tickets_link = page.locator('a:has-text("Tickets"), span:has-text("Tickets")')
    if await tickets_link.count() > 0:
        await tickets_link.first.click()
        await asyncio.sleep(5)
    else:
        await navigate_to(
            page,
            f"{ODOO_URL}/web#action=helpdesk_mgmt.helpdesk_ticket_action_main&model=helpdesk.ticket&view_type=list",
        )
    await page.screenshot(path=str(OUTPUT_DIR / "01_tickets_list.png"), full_page=True)

    # Click NOVO
    print("  Clicando NOVO...")
    novo_btn = page.locator(
        'button:has-text("NOVO"), button:has-text("New"), a:has-text("NOVO")'
    )
    if await novo_btn.count() > 0:
        await novo_btn.first.click()
        await asyncio.sleep(5)
    await page.screenshot(path=str(OUTPUT_DIR / "02_ticket_form.png"), full_page=True)

    # Fill Subject
    print("  Preenchendo assunto...")
    name_input = page.locator('input[name="name"]')
    if await name_input.count() > 0:
        await name_input.first.click()
        await name_input.first.fill(ticket["subject"])
    else:
        title_area = page.locator('.o_field_widget[name="name"]')
        if await title_area.count() > 0:
            await title_area.first.click()
            await asyncio.sleep(0.5)
            await page.keyboard.type(ticket["subject"], delay=30)
    await asyncio.sleep(1)

    # Fill Contact
    print("  Preenchendo contato...")
    partner_input = page.locator('input[name="partner_id"]')
    if await partner_input.count() > 0:
        await partner_input.first.click()
        await partner_input.first.fill(ticket["customer"])
        await asyncio.sleep(2)
        await page.keyboard.press("Enter")
        await asyncio.sleep(2)

    # Fill Description
    print("  Preenchendo descricao...")
    desc_tab = page.locator(
        'a:has-text("Descricao"), a:has-text("Description"), a:has-text("Descrição")'
    )
    if await desc_tab.count() > 0:
        await desc_tab.first.click()
        await asyncio.sleep(2)

    desc_textarea = page.locator('textarea[name="description"]')
    if await desc_textarea.count() > 0:
        await desc_textarea.first.click()
        await desc_textarea.first.fill(ticket["description"])
    else:
        desc_div = page.locator('.o_field_html[name="description"]')
        if await desc_div.count() > 0:
            await desc_div.first.click()
            await asyncio.sleep(0.5)
            await page.keyboard.type(ticket["description"], delay=10)
    await asyncio.sleep(1)

    await page.screenshot(path=str(OUTPUT_DIR / "03_ticket_filled.png"), full_page=True)

    # Save
    print("  Salvando com Ctrl+S...")
    await page.keyboard.press("Control+s")
    await asyncio.sleep(5)
    await page.screenshot(path=str(OUTPUT_DIR / "04_ticket_saved.png"), full_page=True)

    # Back to list
    print("  Voltando para lista...")
    await navigate_to(
        page, f"{ODOO_URL}/web#menu_id=300&model=helpdesk.ticket&view_type=list"
    )
    await asyncio.sleep(3)
    tickets = page.locator('a:has-text("Tickets")')
    if await tickets.count() > 0:
        await tickets.first.click()
        await asyncio.sleep(5)
    await page.screenshot(
        path=str(OUTPUT_DIR / "05_tickets_with_new.png"), full_page=True
    )


async def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser, context, page = await get_logged_in_context(p, OUTPUT_DIR)

        print("Criando ticket...")
        await create_ticket_flow(page, TICKET)

        await context.close()
        await browser.close()

        print("Convertendo videos...")
        convert_all_videos(OUTPUT_DIR / "videos")
        print("Concluido!")


if __name__ == "__main__":
    asyncio.run(main())
