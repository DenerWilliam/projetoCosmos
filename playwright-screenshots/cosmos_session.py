#!/usr/bin/env python3
"""
Cosmos Advisors - Salva sessao do Odoo para reutilizar nos scripts de tutorial.
Rode uma vez: python cosmos_session.py
"""
import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

ODOO_URL = "http://localhost:16069"
DB = "devel"
USER = "admin"
PASSWORD = "admin"
SESSION_FILE = Path("session_state.json")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()

        print("Fazendo login...")
        await page.goto(f"{ODOO_URL}/web/login?db={DB}")
        await page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(3)
        await page.fill('input[name="login"]', USER)
        await page.fill('input[name="password"]', PASSWORD)
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(8)

        # Dismiss any error dialogs
        try:
            ok_btn = page.locator('.modal-footer button:has-text("OK")')
            if await ok_btn.count() > 0:
                await ok_btn.first.click()
                await asyncio.sleep(1)
        except Exception:
            pass

        # Save storage state (cookies + localStorage)
        state = await context.storage_state()
        SESSION_FILE.write_text(json.dumps(state, indent=2))
        print(f"Sessao salva em {SESSION_FILE}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
