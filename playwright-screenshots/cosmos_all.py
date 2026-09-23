#!/usr/bin/env python3
"""
Cosmos Advisors - Screenshots de todos os modulos (sessao persistente, sem login).
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

OUTPUT_DIR = Path("output_modules")


async def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser, context, page = await get_logged_in_context(p, OUTPUT_DIR)

        # 1. Discuss/Inbox
        print("1. Discuss...")
        await navigate_to(page, f"{ODOO_URL}/web")
        await asyncio.sleep(3)
        await page.screenshot(path=str(OUTPUT_DIR / "01_discuss.png"), full_page=True)

        # 2. CRM Pipeline
        print("2. CRM Pipeline...")
        await navigate_to(
            page, f"{ODOO_URL}/web#menu_id=129&model=crm.lead&view_type=kanban"
        )
        await asyncio.sleep(3)
        pipeline = page.locator('a:has-text("Pipeline")')
        if await pipeline.count() > 0:
            await pipeline.first.click()
            await asyncio.sleep(5)
        await page.screenshot(
            path=str(OUTPUT_DIR / "02_crm_pipeline.png"), full_page=True
        )

        # 3. Projects
        print("3. Projects...")
        await navigate_to(
            page, f"{ODOO_URL}/web#menu_id=248&model=project.project&view_type=kanban"
        )
        await asyncio.sleep(3)
        projects = page.locator('a:has-text("Projects")')
        if await projects.count() > 0:
            await projects.first.click()
            await asyncio.sleep(5)
        await page.screenshot(path=str(OUTPUT_DIR / "04_projects.png"), full_page=True)

        # 4. Accounting/Invoices
        print("4. Accounting...")
        await navigate_to(
            page, f"{ODOO_URL}/web#menu_id=160&model=account.move&view_type=list"
        )
        await asyncio.sleep(3)
        invoices = page.locator('a:has-text("Invoices"), span:has-text("Invoices")')
        if await invoices.count() > 0:
            await invoices.first.click()
            await asyncio.sleep(5)
        await page.screenshot(
            path=str(OUTPUT_DIR / "05_accounting.png"), full_page=True
        )

        # 5. Helpdesk Tickets
        print("5. Helpdesk...")
        await navigate_to(
            page, f"{ODOO_URL}/web#menu_id=300&model=helpdesk.ticket&view_type=list"
        )
        await asyncio.sleep(3)
        tickets = page.locator('a:has-text("Tickets")')
        if await tickets.count() > 0:
            await tickets.first.click()
            await asyncio.sleep(5)
        await page.screenshot(path=str(OUTPUT_DIR / "06_helpdesk.png"), full_page=True)

        await context.close()
        await browser.close()

        print("Convertendo videos...")
        convert_all_videos(OUTPUT_DIR / "videos")
        print("Concluido!")


if __name__ == "__main__":
    asyncio.run(main())
