#!/usr/bin/env python3
"""
Shared helpers for Cosmos Advisors tutorial scripts.
Provides a logged-in browser context using saved session state.
"""
import asyncio
import subprocess
from pathlib import Path

ODOO_URL = "http://localhost:16069"
DB = "devel"
SESSION_FILE = Path(__file__).parent / "session_state.json"

CURSOR_OVERLAY_JS = """
(() => {
    if (window.__cosmosCursor) return;
    window.__cosmosCursor = true;

    const SIZE = 52;
    const TIP_X = SIZE * (5 / 24);
    const TIP_Y = SIZE * (3 / 24);
    const EASE = 0.15;

    const mount = () => {
        if (!document.documentElement || !document.head) return false;
        const style = document.createElement('style');
        style.textContent = `
            #cosmos-cursor {
                position: fixed; left: 0; top: 0; pointer-events: none;
                z-index: 2147483647; will-change: transform; opacity: 0;
            }
            #cosmos-cursor svg { display: block; filter: drop-shadow(0 3px 4px rgba(0,0,0,0.4)); }
            #cosmos-halo {
                position: fixed; left: 0; top: 0; pointer-events: none;
                z-index: 2147483647;
                width: 56px; height: 56px; margin: -28px 0 0 -28px;
                border: 3px solid rgba(255, 70, 70, 0.9); border-radius: 50%;
                opacity: 0;
            }
        `;
        document.head.appendChild(style);

        const cursor = document.createElement('div');
        cursor.id = 'cosmos-cursor';
        cursor.innerHTML = `
            <svg width="${SIZE}" height="${SIZE}" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 3L19 11.5L12 13L15.5 19.5L13.5 21L10 14.5L5 18.5V3Z"
                      fill="#ff0000" stroke="#ffffff" stroke-width="1.3" />
            </svg>`;
        document.documentElement.appendChild(cursor);

        const halo = document.createElement('div');
        halo.id = 'cosmos-halo';
        document.documentElement.appendChild(halo);

        let cx = window.innerWidth / 2, cy = window.innerHeight / 2;
        let tx = cx, ty = cy;
        let pendingHalo = null;
        let rafId;
        let shown = false;

        const triggerHalo = (x, y) => {
            halo.style.transition = 'transform .25s ease-out, opacity .3s ease-out';
            halo.style.transform = `translate(${x}px, ${y}px) scale(0.3)`;
            halo.style.opacity = 1;
            requestAnimationFrame(() => {
                halo.style.transform = `translate(${x}px, ${y}px) scale(1.6)`;
            });
            clearTimeout(window.__cosmosHaloTimer);
            window.__cosmosHaloTimer = setTimeout(() => { halo.style.opacity = 0; }, 350);
        };

        const render = () => {
            const dx = tx - cx, dy = ty - cy;
            const dist = Math.hypot(dx, dy);
            if (!shown && (dist > 0.5 || pendingHalo)) {
                shown = true;
                cursor.style.opacity = 1;
            }
            if (dist > 0.5) {
                cx += dx * EASE;
                cy += dy * EASE;
                cursor.style.transform = `translate(${cx - TIP_X}px, ${cy - TIP_Y}px)`;
            } else if (pendingHalo) {
                cx = tx; cy = ty;
                cursor.style.transform = `translate(${cx - TIP_X}px, ${cy - TIP_Y}px)`;
                const h = pendingHalo;
                pendingHalo = null;
                triggerHalo(h.x, h.y);
            }
            rafId = requestAnimationFrame(render);
        };

        document.addEventListener('mousemove', (e) => {
            tx = e.clientX;
            ty = e.clientY;
        }, { passive: true });

        document.addEventListener('mousedown', (e) => {
            pendingHalo = { x: e.clientX, y: e.clientY };
        }, true);

        render();
        return true;
    };

    if (!mount()) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => mount(), { once: true });
        } else {
            const t = setInterval(() => { if (mount()) clearInterval(t); }, 50);
        }
    }
})();
"""


def convert_webm_to_mp4(webm_path):
    mp4_path = webm_path.with_suffix(".mp4")
    if webm_path.stat().st_size > 0:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(webm_path),
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                "23",
                str(mp4_path),
            ],
            capture_output=True,
        )
        webm_path.unlink()
        return mp4_path
    return None


def convert_mp4_to_gif(mp4_path, width=1000, fps=15):
    gif_path = mp4_path.with_suffix(".gif")
    if mp4_path.stat().st_size > 0:
        palette_path = mp4_path.parent / "palette.png"
        vf = f"fps={fps},scale={width}:-1:flags=lanczos"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(mp4_path),
                "-vf",
                f"{vf},palettegen=max_colors=192:stats_mode=diff",
                str(palette_path),
            ],
            capture_output=True,
        )
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(mp4_path),
                "-i",
                str(palette_path),
                "-lavfi",
                f"[0:v] {vf} [x]; [x][1:v] paletteuse=dither=sierra2_4a",
                "-loop",
                "0",
                str(gif_path),
            ],
            capture_output=True,
        )
        palette_path.unlink()
        return gif_path
    return None


def convert_all_videos(videos_dir):
    for webm_file in videos_dir.glob("*.webm"):
        mp4_file = convert_webm_to_mp4(webm_file)
        if mp4_file:
            print(f"  MP4: {mp4_file.name}")
            gif_file = convert_mp4_to_gif(mp4_file)
            if gif_file:
                print(f"  GIF: {gif_file.name}")


async def dismiss_error(page):
    try:
        ok_btn = page.locator('.modal-footer button:has-text("OK")')
        if await ok_btn.count() > 0:
            await ok_btn.first.click()
            await asyncio.sleep(1)
    except Exception:
        pass


async def get_logged_in_context(p, output_dir, record=True):
    """
    Returns a (browser, context, page) tuple with a logged-in session.
    Uses saved session_state.json if available, otherwise does fresh login.
    """
    browser = await p.chromium.launch(headless=True)

    context_kwargs = {"viewport": {"width": 1920, "height": 1080}}
    if record and output_dir:
        videos_dir = output_dir / "videos"
        videos_dir.mkdir(exist_ok=True)
        context_kwargs["record_video_dir"] = str(videos_dir)

    if SESSION_FILE.exists():
        context_kwargs["storage_state"] = str(SESSION_FILE)

    context = await browser.new_context(**context_kwargs)
    page = await context.new_page()
    await page.add_init_script(CURSOR_OVERLAY_JS)

    # If no saved session, do a fresh login
    if not SESSION_FILE.exists():
        print("  Nenhuma sessao salva, fazendo login...")
        await page.goto(f"{ODOO_URL}/web/login?db={DB}")
        await page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(3)
        await page.screenshot(path=str(output_dir / "01_login.png"), full_page=True)

        await page.fill('input[name="login"]', "admin")
        await page.fill('input[name="password"]', "admin")
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(8)
        await dismiss_error(page)

        # Save session for next time
        state = await context.storage_state()
        SESSION_FILE.write_text(json.dumps(state, indent=2))
        print(f"  Sessao salva em {SESSION_FILE}")

    return browser, context, page


async def navigate_to(page, url):
    """Navigate to an Odoo URL, resetting SPA state first if needed."""
    if "/web#" in url:
        await page.goto(f"{ODOO_URL}/web", wait_until="domcontentloaded")
        await asyncio.sleep(3)
        await dismiss_error(page)
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(5)
    await dismiss_error(page)


# Need this for the json import in get_logged_in_context
import json
