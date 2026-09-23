#!/usr/bin/env python3
"""
Cosmos Advisors - Screenshots e Video dos modulos (sessao persistente).
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

OUTPUT_DIR = Path("output")


async def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser, context, page = await get_logged_in_context(p, OUTPUT_DIR)

        print("1. Discuss...")
        await navigate_to(page, f"{ODOO_URL}/web")
        await asyncio.sleep(3)
        await page.screenshot(path=str(OUTPUT_DIR / "01_discuss.png"), full_page=True)

        print("2. CRM Pipeline...")
        await navigate_to(page, f"{ODOO_URL}/web#menu_id=129")
        await asyncio.sleep(5)
        await page.screenshot(path=str(OUTPUT_DIR / "02_crm.png"), full_page=True)

        print("3. Projetos...")
        await navigate_to(page, f"{ODOO_URL}/web#menu_id=242")
        await asyncio.sleep(5)
        await page.screenshot(path=str(OUTPUT_DIR / "03_projetos.png"), full_page=True)

        print("4. Contabilidade...")
        await navigate_to(page, f"{ODOO_URL}/web#menu_id=157")
        await asyncio.sleep(5)
        await page.screenshot(
            path=str(OUTPUT_DIR / "04_contabilidade.png"), full_page=True
        )

        await context.close()
        await browser.close()

        print("Convertendo videos...")
        convert_all_videos(OUTPUT_DIR / "videos")
        print("Concluido!")


if __name__ == "__main__":
    asyncio.run(main())
