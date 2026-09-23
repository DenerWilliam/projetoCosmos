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
    human_type,
    navigate_to,
    smooth_click,
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
    await human_type(
        page,
        page.locator(
            'input[placeholder*="Joao"], input[placeholder*="Jo"]'
        ),
        contact["name"],
    )
    await asyncio.sleep(0.5)

    print("  Preenchendo empresa...")
    company_input = page.locator(
        'input[placeholder*="Empresa"], input[placeholder*="Company"]'
    ).first
    await smooth_click(page, company_input)
    await asyncio.sleep(0.5)
    await page.keyboard.press("Tab")
    await asyncio.sleep(0.5)

    print("  Preenchendo endereco...")
    await human_type(
        page,
        page.locator(
            'input[placeholder*="Endere"], input[placeholder*="Address"]'
        ),
        contact["street"],
    )
    await asyncio.sleep(0.5)

    print("  Preenchendo complemento...")
    await human_type(
        page,
        page.locator(
            'input[placeholder*="Complemento"], input[placeholder*="Suite"]'
        ),
        contact["street2"],
    )
    await asyncio.sleep(0.5)

    print("  Preenchendo cidade...")
    await human_type(
        page,
        page.locator(
            'input[placeholder="Cidade"], input[placeholder="City"]'
        ),
        contact["city"],
    )
    await asyncio.sleep(0.5)

    print("  Preenchendo CEP...")
    await human_type(
        page,
        page.locator('input[placeholder="CEP"], input[placeholder="ZIP"]'),
        contact["zip"],
    )
    await asyncio.sleep(0.5)

    print("  Preenchendo CNPJ...")
    await human_type(
        page,
        page.locator(
            'input[placeholder*="BE04"], input[placeholder*="Tax"]'
        ),
        contact["vat"],
    )
    await asyncio.sleep(0.5)

    print("  Preenchendo cargo...")
    await human_type(
        page,
        page.locator(
            'input[placeholder*="Diretor"], input[placeholder*="Job"], input[placeholder*="Function"]'
        ),
        contact["function"],
    )
    await asyncio.sleep(0.5)

    print("  Preenchendo telefone...")
    tel_inputs = page.locator('input[type="tel"]')
    await human_type(page, tel_inputs.nth(0), contact["phone"])
    await asyncio.sleep(0.5)

    print("  Preenchendo celular...")
    await human_type(page, tel_inputs.nth(1), contact["mobile"])
    await asyncio.sleep(0.5)

    print("  Preenchendo email...")
    await human_type(page, page.locator('input[type="email"]'), contact["email"])
    await asyncio.sleep(0.5)

    print("  Preenchendo website...")
    await human_type(
        page,
        page.locator(
            'input[placeholder*="odoo"], input[placeholder*="http"]'
        ),
        contact["website"],
    )
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
        await smooth_click(page, contacts_link.first)
        await asyncio.sleep(5)
    await page.screenshot(
        path=str(OUTPUT_DIR / "01_contatos_lista.png"), full_page=True
    )

    print("  Clicando NOVO...")
    novo_btn = page.locator('button:has-text("NOVO"), button:has-text("New")')
    await smooth_click(page, novo_btn.first)
    await asyncio.sleep(5)

    print("  Selecionando Individual...")
    await smooth_click(page, page.locator('input[type="radio"]').first)
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
        await smooth_click(page, save_btn.first)
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
