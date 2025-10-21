import asyncio
import hashlib
from typing import Optional

from pyppeteer import launch


class RDQAExportService:
    def __init__(self):
        self._browser = None

    async def _get_browser(self):
        if self._browser is None:
            self._browser = await launch(args=['--no-sandbox'])
        return self._browser

    async def render_pdf_from_html(self, html: str, format_: str = 'A4', margin_mm: int = 12) -> bytes:
        browser = await self._get_browser()
        page = await browser.newPage()
        await page.setContent(html, waitUntil=['load', 'networkidle0'])
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

