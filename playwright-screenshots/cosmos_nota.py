#!/usr/bin/env python3
"""
Cosmos Advisors - Fluxo de Emissao de Nota Fiscal (sessao persistente).
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

OUTPUT_DIR = Path("output_nota")

INVOICE = {
    "partner": "Joao Silva",
    "invoice_date": "20/09/2026",
    "ref": "COSMOS-2026-001",
    "lines": [
        {"name": "Consultoria Financeira - M&A", "qty": "10", "price": "5000"},
        {"name": "Due Diligence Corporativa", "qty": "1", "price": "25000"},
    ],
}


async def create_invoice_flow(page, invoice):
    print("  Navegando para Faturas...")
    await navigate_to(page, f"{ODOO_URL}/web#menu_id=160")
    await asyncio.sleep(3)
    invoices = page.locator('a:has-text("Invoices"), span:has-text("Invoices")')
    if await invoices.count() > 0:
        await smooth_click(page, invoices.first)
        await asyncio.sleep(5)
    await page.screenshot(path=str(OUTPUT_DIR / "01_faturas_lista.png"), full_page=True)

    print("  Clicando NOVO...")
    novo_btn = page.locator('button:has-text("NOVO"), button:has-text("New")')
    await smooth_click(page, novo_btn.first)
    await asyncio.sleep(5)

    print("  Preenchendo cliente...")
    partner_input = page.locator(
        'div[name="partner_id"] input, input[placeholder*="Cliente"], input[placeholder*="Customer"]'
    ).first
    await human_type(page, partner_input, invoice["partner"])
    await asyncio.sleep(2)
    await page.keyboard.press("Enter")
    await asyncio.sleep(2)

    print("  Preenchendo data...")
    date_input = page.locator(
        'input[name="invoice_date"], input[placeholder*="Data"]'
    ).first
    if await date_input.count() > 0:
        await human_type(page, date_input, invoice["invoice_date"], clear=True)
        await asyncio.sleep(1)
        await page.keyboard.press("Tab")
        await asyncio.sleep(1)

    print("  Preenchendo referencia...")
    ref_input = page.locator(
        'input[name="ref"], input[placeholder*="Referencia"]'
    ).first
    if await ref_input.count() > 0:
        await human_type(page, ref_input, invoice["ref"])
        await asyncio.sleep(1)

    await asyncio.sleep(2)
    await page.screenshot(path=str(OUTPUT_DIR / "02_form_fatura.png"), full_page=True)

    print("  Adicionando linhas de produto...")
    for i, line in enumerate(invoice["lines"]):
        print(f"    Linha {i+1}: {line['name']}")
        add_line_btn = page.locator(
            'a:has-text("Adicionar uma linha"), button:has-text("Adicionar uma linha")'
        )
        if await add_line_btn.count() > 0:
            await smooth_click(page, add_line_btn.first)
            await asyncio.sleep(3)

        name_td = page.locator('td[name="name"]')
        if await name_td.count() > 0:
            last_name = name_td.last
            name_input = last_name.locator("input")
            if await name_input.count() > 0:
                await human_type(page, name_input, line["name"])
            else:
                await page.keyboard.type(line["name"], delay=10)
            await asyncio.sleep(0.5)
            await page.keyboard.press("Tab")
            await asyncio.sleep(1)

        qty_td = page.locator('td[name="quantity"]')
        if await qty_td.count() > 0:
            last_qty = qty_td.last
            qty_input = last_qty.locator("input")
            if await qty_input.count() > 0:
                await human_type(page, qty_input, line["qty"], clear=True)
            else:
                await page.keyboard.press("Control+a")
                await page.keyboard.type(line["qty"], delay=10)
            await asyncio.sleep(0.5)
            await page.keyboard.press("Tab")
            await asyncio.sleep(1)

        price_td = page.locator('td[name="price_unit"]')
        if await price_td.count() > 0:
            last_price = price_td.last
            price_input = last_price.locator("input")
            if await price_input.count() > 0:
                await human_type(page, price_input, line["price"], clear=True)
            else:
                await page.keyboard.press("Control+a")
                await page.keyboard.type(line["price"], delay=10)
            await asyncio.sleep(0.5)
            await page.keyboard.press("Tab")
            await asyncio.sleep(1)

    await asyncio.sleep(2)
    await page.screenshot(path=str(OUTPUT_DIR / "03_linhas_fatura.png"), full_page=True)

    print("  Salvando fatura...")
    await page.keyboard.press("Control+s")
    await asyncio.sleep(5)
    await page.screenshot(path=str(OUTPUT_DIR / "04_fatura_salva.png"), full_page=True)

    print("  Confirmando fatura...")
    confirm_btn = page.locator(
        'button:has-text("Confirmar"), button:has-text("Confirm")'
    )
    if await confirm_btn.count() > 0:
        await smooth_click(page, confirm_btn.first)
        await asyncio.sleep(5)
    await page.screenshot(
        path=str(OUTPUT_DIR / "05_fatura_confirmada.png"), full_page=True
    )

    print("  Registrando pagamento...")
    register_btn = page.locator(
        'button:has-text("Registrar Pagamento"), button:has-text("Register Payment")'
    )
    if await register_btn.count() > 0:
        await smooth_click(page, register_btn.first)
        await asyncio.sleep(3)
        pay_btn = page.locator(
            'button:has-text("Criar Pagamento"), button:has-text("Create Payment")'
        )
        if await pay_btn.count() > 0:
            await smooth_click(page, pay_btn.first)
            await asyncio.sleep(5)
    await page.screenshot(path=str(OUTPUT_DIR / "06_pagamento.png"), full_page=True)


async def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser, context, page = await get_logged_in_context(p, OUTPUT_DIR)

        print("Criar fatura...")
        await create_invoice_flow(page, INVOICE)

        await context.close()
        await browser.close()

        print("Convertendo videos...")
        convert_all_videos(OUTPUT_DIR / "videos")
        print("Concluido!")


if __name__ == "__main__":
    asyncio.run(main())
