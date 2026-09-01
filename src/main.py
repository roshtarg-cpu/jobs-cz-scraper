"""Main actor logic for Jobs.cz scraper."""
import asyncio
from apify import Actor
from .utils import _fetch
from .parser import _extract_jobs


async def main():
    """Main actor entry point."""
    async with Actor() as actor:
        # Get input
        actor_input = await actor.get_input() or {}
        search_keyword = actor_input.get('searchKeyword', '')
        location = actor_input.get('location', '')
        category = actor_input.get('category', '')
        max_results = actor_input.get('maxResults', 50)
        
        # Get proxy configuration
        proxy_config = actor_input.get('proxyConfiguration')
        if proxy_config:
            proxy_cfg = await actor.create_proxy_configuration(proxy_config)
            proxy_url = await proxy_cfg.new_url()
        else:
            # Default to RESIDENTIAL proxy
            env = actor.get_env()
            password = env.get('APIFY_PROXY_PASSWORD')
            if password:
                groups = 'RESIDENTIAL'
                proxy_url = f"http://groups-{groups}:{password}@proxy.apify.com:8000"
            else:
                proxy_url = None
        
        actor.log.info(f'Starting Jobs.cz scraper')
        actor.log.info(f'Search: {search_keyword}, Location: {location}, Max: {max_results}')
        
        results_collected = 0
        page_num = 1
        max_pages = 50  # Safety limit
        
        while results_collected < max_results and page_num <= max_pages:
            # Build URL with search parameters
            url = _build_url(search_keyword, location, category, page_num)
            
            actor.log.info(f'Fetching page {page_num}: {url}')
            
            # Fetch with retries
            html = None
            for attempt in range(3):
                try:
                    html = await _fetch(url, proxy_url)
                    if html:
                        break
                    actor.log.warning(f'Attempt {attempt + 1}: Got empty response')
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                except Exception as e:
                    actor.log.error(f'Attempt {attempt + 1} failed: {e}')
                    if attempt < 2:
                        await asyncio.sleep(2 ** attempt)
            
            if not html:
                actor.log.error(f'Failed to fetch page {page_num} after 3 attempts')
                break
            
            # Parse jobs
            jobs = _extract_jobs(html)
            
            if not jobs:
                actor.log.info(f'No jobs found on page {page_num}, stopping')
                break
            
            actor.log.info(f'Extracted {len(jobs)} jobs from page {page_num}')
            
            # Push results
            for job in jobs:
                if results_collected >= max_results:
                    break
                
                await actor.push_data(job)
                results_collected += 1
                
                if results_collected % 10 == 0:
                    actor.log.info(f'Collected {results_collected}/{max_results} jobs')
            
            page_num += 1
            
            # Small delay between pages
            await asyncio.sleep(1)
        
        actor.log.info(f'✅ Scraping complete. Total jobs collected: {results_collected}')


def _build_url(keyword, location, category, page):
    """Build Jobs.cz search URL."""
    base = "https://www.jobs.cz"
    
    # Jobs.cz URL structure varies, common patterns:
    # /rpd/  - job listings
    # /prace/  - job search
    # Query params: q= for keyword, locality= for location, page= for pagination
    
    params = []
    if keyword:
        params.append(f'q={keyword.replace(" ", "+")}')
    if location:
        params.append(f'locality={location.replace(" ", "+")}')
    if page > 1:
        params.append(f'page={page}')
    
    if params:
        return f"{base}/prace/?{'&'.join(params)}"
    else:
        # Default: all jobs
        return f"{base}/prace/?page={page}" if page > 1 else f"{base}/prace/"
