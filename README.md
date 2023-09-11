# Figshare Asynchronous File Downloader (for HunCRC)

This script is specifically designed to scrape and download files from Figshare based on provided URLs. It asynchronously fetches multiple URLs and extracts essential data for downloading. Files are then saved on the `janos` server using their respective data identifiers.

## Features

- Designed for Figshare: Tailored to scrape Figshare URLs and extract relevant information.
- Efficient File Retrieval: Uses asynchronous programming to fetch and download multiple files concurrently.
- Server Storage: Saves the downloaded files on the `janos` server.

## Requirements

Ensure you have the following Python libraries installed:

- aiohttp
- asyncio
- BeautifulSoup
- aiofiles

To install the necessary libraries, run:

```bash
pip install aiohttp aiofiles beautifulsoup4 lxml
```

## How to Use

1. Ensure the `figshare_data_paths.json` file is placed in the `./code/` directory. This file contains a list of Figshare URL details under the key `url_public_html`.

2. Navigate outside the `code` directory and run the script:

```bash
python code/access_data.py
```

3. The script will:
   - Asynchronously fetch each Figshare URL.
   - Extract the download link and data identifier from the Figshare page's HTML.
   - Download the respective file using the extracted link.
   - Save the file on the `janos` server with its data identifier as its filename.

## Important Notes

- You can adjust the `semaphore_size` in the `main` function to control the number of simultaneous fetch requests.
- Ensure you have the necessary permissions and access rights to the `janos` server for storing the downloaded files.
- If there's an issue with missing data identifiers or download links during the process, the script will print appropriate error messages.

---

Feel free to adjust the README details to match any specific needs or changes in your setup.