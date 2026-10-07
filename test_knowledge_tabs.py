#!/usr/bin/env python3
"""Test Knowledge edit form with markdown tabs."""

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
            p, Path("/tmp/knowledge_tabs"), record=False
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

        # Click on the content to enter edit mode
        try:
            content_area = page.locator(
                ".o_content, .oe_view_only, field[name='content']"
            ).first
            await content_area.click(timeout=5000)
            await asyncio.sleep(3)

            await dismiss_error(page)

            await page.screenshot(
                path="/home/dener/Documentos/Escodoo/projetoCosmos/knowledge_edit_tabs.png",
                full_page=True,
            )
            print("Edit tabs screenshot saved")
        except Exception as e:
            print(f"Error: {e}")
            # Try clicking elsewhere
            await page.click("body", position={"x": 100, "y": 300})
            await asyncio.sleep(3)
            await page.screenshot(
                path="/home/dener/Documentos/Escodoo/projetoCosmos/knowledge_edit_tabs.png",
                full_page=True,
            )
            print("Edit tabs screenshot saved (fallback)")

        await browser.close()


asyncio.run(main())
