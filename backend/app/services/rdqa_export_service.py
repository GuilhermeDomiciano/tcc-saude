import asyncio
import hashlib
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Optional

from pyppeteer import launch
from pyppeteer.chromium_downloader import chromium_executable, download_chromium


class RDQAExportService:
    def __init__(self):
        self._browser = None

    async def _get_browser(self):
        if self._browser is None:
            executable = await self._resolve_executable()
            args = ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
            try:
                if executable:
                    self._browser = await launch(executablePath=str(executable), args=args)
                else:
                    self._browser = await launch(args=args)
            except Exception as e:
                logging.error(f"Failed to launch Chromium: {e}")
                raise
        return self._browser

    async def _resolve_executable(self) -> Optional[Path]:
        env_path = os.getenv('PUPPETEER_EXECUTABLE_PATH')
        if env_path and Path(env_path).exists():
            return Path(env_path)
        try:
            exe = Path(chromium_executable())
            if exe.exists():
                return exe
        except Exception:
            pass
        candidates = []
        for name in ['chrome', 'google-chrome', 'chromium', 'chromium-browser', 'msedge', 'edge']:
            found = shutil.which(name)
            if found:
                candidates.append(Path(found))
        if sys.platform.startswith('win'):
            win_paths = [
                r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                r"C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
                r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            ]
            candidates.extend(Path(p) for p in win_paths)
        for p in candidates:
            if p.exists():
                return p
        try:
            logging.info("Ensuring managed Chromium is available (downloading if needed)...")
            await download_chromium()
            exe = Path(chromium_executable())
            if exe.exists():
                return exe
        except Exception as e:
            logging.error(f"Chromium download failed: {e}")
        return None

    async def render_pdf_from_html(self, html: str, format_: str = 'A4', margin_mm: int = 12) -> bytes:
        browser = await self._get_browser()
        page = await browser.newPage()
        await page.setContent(html)
        try:
            await page.waitForSelector('body', { 'timeout': 3000 })
        except Exception:
            pass
        pdf_bytes = await page.pdf({
            'format': format_,
            'margin': {
                'top': f'{margin_mm}mm',
                'bottom': f'{margin_mm}mm',
                'left': f'{margin_mm}mm',
                'right': f'{margin_mm}mm',
            },
            'printBackground': True,
            'preferCSSPageSize': False,
        })
        await page.close()
        return pdf_bytes

    async def render_pdf_from_url(self, url: str, format_: str = 'A4', margin_mm: int = 12) -> bytes:
        browser = await self._get_browser()
        page = await browser.newPage()
        await page.goto(url, waitUntil=['load', 'networkidle0'])
        pdf_bytes = await page.pdf({
            'format': format_,
            'margin': {
                'top': f'{margin_mm}mm',
                'bottom': f'{margin_mm}mm',
                'left': f'{margin_mm}mm',
                'right': f'{margin_mm}mm',
            },
            'printBackground': True,
            'preferCSSPageSize': False,
        })
        await page.close()
        return pdf_bytes

    @staticmethod
    def sha256_hex(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

