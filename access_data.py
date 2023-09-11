import aiohttp
import asyncio
from bs4 import BeautifulSoup

import aiofiles
from pprint import pprint
from aiohttp import ClientTimeout

from tqdm import tqdm

failed_downloads = []

async def download_file_async(link, local_filename):
    timeout = ClientTimeout(total=60 * 60 * 10)  # 10 hour
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(link) as response:
            # Ensure the response status is OK
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc=local_filename)

            # Asynchronously write to a local file
            async with aiofiles.open(local_filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(8192)  # 8KB chunks
                    if not chunk:
                        break
                    await f.write(chunk)
                    progress_bar.update(len(chunk))

            progress_bar.close()

async def fetch(url, session):
    try:
        async with session.get(url) as response:
            result = await response.text()
            
            # Extract the download link from the HTML
            soup = BeautifulSoup(result, 'lxml')
            a_tag = soup.find('a', attrs={'tooltip': 'Download file'})
            if a_tag:
                link = a_tag['href']
            else:
                link = ''
                
            div_tag = soup.find('div', attrs={'class': 'j9gCL'})
            
            if div_tag:
                data_identifier = div_tag['title']
            else:
                data_identifier = 'missing'
                return Exception('Missing data identifier')
            
            # Download and save the file
            await download_file_async(link, './data/' + data_identifier)
                
            return link

    except Exception as e:
        pprint(f"Error fetching {url} at {link}: {e}")
        failed_downloads.append({'url_public_html': url, 'reason': str(e), 'link': link})
        return ''

async def main(urls, semaphore_size=10):
    # NOTE: limit the number of simultaneous requests using a Semaphore
    semaphore = asyncio.Semaphore(semaphore_size)

    async with aiohttp.ClientSession(timeout=ClientTimeout(total=60 * 60 * 1000)) as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(bounded_fetch(semaphore, url, session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        
        return responses

async def bounded_fetch(sem, url, session):
    # Use semaphore to limit number of requests
    async with sem:
        return await fetch(url, session)

if __name__ == "__main__":
    import json
    from pathlib import Path
    
    Path('./data').mkdir(parents=True, exist_ok=True)
    
    # Load the figshare data paths
    with open('./code/figshare_data_paths.json') as f:
        data = json.load(f)
    
    urls = sorted([ URL['url_public_html'] for URL in data ])
    
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(urls))
    loop.close()
    
    with open('./code/failed_downloads.json', 'w') as f:
        json.dump(failed_downloads, f)
