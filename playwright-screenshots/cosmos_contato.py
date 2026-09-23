#!/usr/bin/env python3
"""
Cosmos Advisors - Fluxo de Cadastro de Contato (sessao persistente).
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

OUTPUT_DIR = Path("output_contato")

CONTACT = {
    "name": "Joao Silva",
    "function": "Diretor Financeiro",
    "phone": "+55 11 99999-1234",
    "mobile": "+55 11 98888-5678",
    "email": "joao.silva@cosmos.com.br",
    "website": "www.cosmosadvisors.com.br",
    "street": "Av. Brigadeiro Faria Lima, 3477",
    "street2": "Torre Norte, 18 andar",
    "city": "Sao Paulo",
    "zip": "04538-133",
    "vat": "12.345.678/0001-99",
}


async def fill_contact_form(page, contact):
    print("  Preenchendo nome...")
    await page.locator(
        'input[placeholder*="Joao"], input[placeholder*="Jo"]'
    ).first.fill(contact["name"])
    await asyncio.sleep(0.5)

    print("  Preenchendo empresa...")
    company_input = page.locator(
        'input[placeholder*="Empresa"], input[placeholder*="Company"]'
    ).first
    await company_input.click()
    await asyncio.sleep(0.5)
    await page.keyboard.press("Tab")
    await asyncio.sleep(0.5)

    print("  Preenchendo endereco...")
    await page.locator(
        'input[placeholder*="Endere"], input[placeholder*="Address"]'
    ).first.fill(contact["street"])
    await asyncio.sleep(0.5)

    print("  Preenchendo complemento...")
    await page.locator(
        'input[placeholder*="Complemento"], input[placeholder*="Suite"]'
    ).first.fill(contact["street2"])
    await asyncio.sleep(0.5)

    print("  Preenchendo cidade...")
    await page.locator(
        'input[placeholder="Cidade"], input[placeholder="City"]'
    ).first.fill(contact["city"])
    await asyncio.sleep(0.5)

    print("  Preenchendo CEP...")
    await page.locator('input[placeholder="CEP"], input[placeholder="ZIP"]').first.fill(
        contact["zip"]
    )
    await asyncio.sleep(0.5)

    print("  Preenchendo CNPJ...")
    await page.locator(
        'input[placeholder*="BE04"], input[placeholder*="Tax"]'
    ).first.fill(contact["vat"])
    await asyncio.sleep(0.5)

    print("  Preenchendo cargo...")
    await page.locator(
        'input[placeholder*="Diretor"], input[placeholder*="Job"], input[placeholder*="Function"]'
    ).first.fill(contact["function"])
    await asyncio.sleep(0.5)

    print("  Preenchendo telefone...")
    tel_inputs = page.locator('input[type="tel"]')
    await tel_inputs.nth(0).fill(contact["phone"])
    await asyncio.sleep(0.5)

    print("  Preenchendo celular...")
    await tel_inputs.nth(1).fill(contact["mobile"])
    await asyncio.sleep(0.5)

    print("  Preenchendo email...")
    await page.locator('input[type="email"]').first.fill(contact["email"])
    await asyncio.sleep(0.5)

    print("  Preenchendo website...")
    await page.locator(
        'input[placeholder*="odoo"], input[placeholder*="http"]'
    ).first.fill(contact["website"])
    await asyncio.sleep(0.5)

    print("  Fechando dropdowns...")
    await page.locator(
        'input[placeholder*="odoo"], input[placeholder*="http"]'
    ).first.press("Tab")
    await asyncio.sleep(1)
    await page.keyboard.press("Escape")
    await asyncio.sleep(1)


async def create_contact_flow(page):
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

    print("  Preenchendo formulario...")
    await fill_contact_form(page, CONTACT)
    await asyncio.sleep(1)
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


async def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser, context, page = await get_logged_in_context(p, OUTPUT_DIR)

        print("Cadastrar contato...")
        await create_contact_flow(page)

        await context.close()
        await browser.close()

        print("Convertendo videos...")
        convert_all_videos(OUTPUT_DIR / "videos")
        print("Concluido!")


if __name__ == "__main__":
    asyncio.run(main())
