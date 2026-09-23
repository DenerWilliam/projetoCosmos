#!/usr/bin/env python3
"""
Cosmos Advisors - Fluxo de Lead no CRM (sessao persistente).
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

OUTPUT_DIR = Path("output_lead")

LEAD = {
    "partner": "Cosmos Advisors",
    "opportunity": "Consultoria M&A - Fusao Corporativa",
    "email": "contato@cosmosadvisors.com.br",
    "phone": "+55 11 3000-1234",
    "revenue": "150000",
}


async def create_lead_flow(page, lead):
    print("  Navegando para CRM...")
    await navigate_to(page, f"{ODOO_URL}/web#menu_id=129")
    await asyncio.sleep(3)
    await page.screenshot(path=str(OUTPUT_DIR / "01_crm_pipeline.png"), full_page=True)

    # Click NOVO to open quick-add form
    print("  Clicando NOVO...")
    await page.click('button:has-text("NOVO"), button:has-text("New")')
    await asyncio.sleep(3)

    # Fill organization
    print("  Preenchendo organizacao...")
    org_input = page.locator(
        '.o_kanban_quick_create input[placeholder*="exemplo"], .o_kanban_quick_create div[name="partner_id"] input'
    ).first
    if await org_input.count() == 0:
        org_input = page.locator('.o_form_nosheet div[name="partner_id"] input').first
    if await org_input.count() > 0:
        await org_input.click()
        await org_input.fill(lead["partner"])
        await asyncio.sleep(2)
        await page.keyboard.press("Enter")
        await asyncio.sleep(2)

    # Fill opportunity
    print("  Preenchendo oportunidade...")
    opp_input = page.locator(
        '.o_kanban_quick_create input[placeholder*="Preco"], .o_kanban_quick_create input[placeholder*="exemplo"]'
    ).first
    if await opp_input.count() == 0:
        opp_input = page.locator('.o_form_nosheet input[placeholder*="exemplo"]').first
    if await opp_input.count() > 0:
        await opp_input.click()
        await opp_input.fill("")
        await opp_input.fill(lead["opportunity"])
        await asyncio.sleep(1)

    await page.screenshot(path=str(OUTPUT_DIR / "02_form_quick.png"), full_page=True)

    # Click EDITAR to open full form
    print("  Clicando EDITAR para formulario completo...")
    editar_btn = page.locator('button:has-text("EDITAR")').first
    if await editar_btn.count() > 0:
        await editar_btn.click()
        await asyncio.sleep(5)
    await page.screenshot(path=str(OUTPUT_DIR / "03_form_full.png"), full_page=True)

    # Fill email
    print("  Preenchendo email...")
    email_input = page.locator('.o_form_view input[type="email"]').first
    if await email_input.count() > 0:
        await email_input.click()
        await email_input.fill(lead["email"])
        await asyncio.sleep(1)

    # Fill phone
    print("  Preenchendo telefone...")
    phone_input = page.locator('.o_form_view input[type="tel"]').first
    if await phone_input.count() > 0:
        await phone_input.click()
        await phone_input.fill(lead["phone"])
        await asyncio.sleep(1)

    # Fill expected revenue
    print("  Preenchendo receita esperada...")
    revenue_label = page.locator('label:has-text("Receita Esperada")').first
    if await revenue_label.count() > 0:
        for_id = await revenue_label.get_attribute("for")
        if for_id:
            revenue_input = page.locator(f"#{for_id}")
        else:
            revenue_input = page.locator('.o_form_view input[type="text"]').nth(1)
    else:
        revenue_input = page.locator('.o_form_view input[type="text"]').nth(1)

    if await revenue_input.count() > 0:
        await revenue_input.click()
        await asyncio.sleep(0.3)
        await revenue_input.click(click_count=3)
        await asyncio.sleep(0.3)
        await page.keyboard.press("Backspace")
        await asyncio.sleep(0.3)
        await page.keyboard.type(lead["revenue"], delay=50)
        await asyncio.sleep(0.5)
        await page.keyboard.press("Tab")
        await asyncio.sleep(1)

    await asyncio.sleep(1)
    await page.screenshot(path=str(OUTPUT_DIR / "04_form_filled.png"), full_page=True)

    # Save
    print("  Salvando com Ctrl+S...")
    await page.keyboard.press("Control+s")
    await asyncio.sleep(5)
    await page.screenshot(path=str(OUTPUT_DIR / "05_lead_saved.png"), full_page=True)

    # Go back to pipeline
    print("  Voltando ao pipeline...")
    await navigate_to(page, f"{ODOO_URL}/web#menu_id=129")
    await asyncio.sleep(3)
    pipeline = page.locator('a:has-text("Pipeline")')
    if await pipeline.count() > 0:
        await pipeline.first.click()
        await asyncio.sleep(5)
    await page.screenshot(
        path=str(OUTPUT_DIR / "06_pipeline_with_lead.png"), full_page=True
    )


async def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser, context, page = await get_logged_in_context(p, OUTPUT_DIR)

        print("Criar lead...")
        await create_lead_flow(page, LEAD)

        await context.close()
        await browser.close()

        print("Convertendo videos...")
        convert_all_videos(OUTPUT_DIR / "videos")
        print("Concluido!")


if __name__ == "__main__":
    asyncio.run(main())
