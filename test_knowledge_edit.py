#!/usr/bin/env python3
"""Test Knowledge edit form."""

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "playwright-screenshots"))


async def main():
    from cosmos_helpers import dismiss_error, get_logged_in_context
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser, context, page = await get_logged_in_context(
            p, Path("/tmp/knowledge_edit"), record=False
        )

        # Go to Knowledge > Pages
        print("Navigating to Knowledge...")
        await page.goto(
            "http://localhost:16069/web#action=430", wait_until="domcontentloaded"
        )
        await asyncio.sleep(5)

        # Click on first tutorial
        tutorial_link = page.locator("td:has-text('Tutorial: CRM')").first
        await tutorial_link.click(timeout=10000)
        await asyncio.sleep(3)

        # Click Edit button
        try:
            edit_btn = page.locator(
                "button:has-text('Editar'), button:has-text('Edit')"
            ).first
            await edit_btn.click(timeout=5000)
            await asyncio.sleep(3)

            await dismiss_error(page)

            await page.screenshot(
                path="/home/dener/Documentos/Escodoo/projetoCosmos/knowledge_edit_form.png",
                full_page=True,
            )
            print("Edit form screenshot saved")
        except Exception as e:
            print(f"Error: {e}")
            await page.screenshot(
                path="/home/dener/Documentos/Escodoo/projetoCosmos/knowledge_edit_error.png"
            )

        await browser.close()


asyncio.run(main())
