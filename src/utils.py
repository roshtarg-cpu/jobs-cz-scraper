"""Utility functions for fetching pages with Camoufox browser."""
import re
from urllib.parse import urlparse
from camoufox.async_api import AsyncCamoufox


def _parse_proxy(proxy_url):
    """Parse Apify proxy URL into components."""
    if not proxy_url:
        return None
    
    parsed = urlparse(proxy_url)
    return {
        'server': f'{parsed.scheme}://{parsed.hostname}:{parsed.port}',
        'username': parsed.username,
        'password': parsed.password,
    }


async def _fetch(url, proxy_url=None):
    """Fetch a URL using Camoufox with residential proxy."""
    proxy = _parse_proxy(proxy_url) if proxy_url else None
    
    async with AsyncCamoufox(
        headless=True,
        geoip=True,
        proxy=proxy,
    ) as browser:
        page = await browser.new_page()
        
        try:
            response = await page.goto(
                url,
                wait_until='networkidle',
                timeout=90000
            )
            
            # Wait a bit for dynamic content
            await page.wait_for_timeout(3000)
            
            content = await page.content()
            
            # Return None if response is too small (likely blocked)
            if len(content) < 500:
                return None
            
            return content
            
        except Exception as e:
            print(f'Error fetching {url}: {e}')
            return None
        finally:
            await page.close()
