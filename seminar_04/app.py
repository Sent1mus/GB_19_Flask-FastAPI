import argparse
import os
import time
from pathlib import Path
import requests
import threading
import multiprocessing
import asyncio
from bs4 import BeautifulSoup

# URL of the webpage you want to scrape
url = 'https://www.wallpaperflare.com/' # Replace with your target URL

# Fetch the HTML content
response = requests.get(url)
html_content = response.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all <img> tags
img_tags = soup.find_all('img')

# Extract and filter image URLs
jpg_urls = [img['src'] if 'src' in img.attrs else img['data-src'] for img in img_tags if 'src' in img.attrs or 'data-src' in img.attrs]
jpg_urls = [url for url in jpg_urls if url.endswith('.jpg')]

# Write the first 50 JPG URLs to images.txt
with open('images.txt', 'w', encoding='utf-8') as file:
    for i, jpg_url in enumerate(jpg_urls):
        if i >= 50:
            break
        file.write(f'{jpg_url}\n')


image_urls = []
image_path = Path('./images/')
image_path.mkdir(parents=True, exist_ok=True)
with open('images.txt', 'r') as images:
    for image in images.readlines():
        image_urls.append(image.strip())


def generate_filename(index, method, directory='images'):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Generate the filename with the directory path
    filename = os.path.join(directory, f"image_{index}_{method}.jpg")
    return filename


def download_image(url, index, method):
    start_time = time.time()
    response = requests.get(url, stream=True)
    filename = generate_filename(index, method)
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    end_time = time.time() - start_time
    print(f"Downloaded {filename} in {end_time:.2f} seconds")


async def download_image_async(url, index, method):
    start_time = time.time()
    response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url, {"stream": True})
    filename = generate_filename(index, method)
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    end_time = time.time() - start_time
    print(f"Downloaded {filename} in {end_time:.2f} seconds")


def download_images_threading(urls, method):
    start_time = time.time()
    threads = []
    for index, url in enumerate(urls):
        t = threading.Thread(target=download_image, args=(url, index, method))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end_time = time.time() - start_time
    print(f"Total time using {method}: {end_time:.2f} seconds")


def download_images_multiprocessing(urls, method):
    start_time = time.time()
    processes = []
    for index, url in enumerate(urls):
        p = multiprocessing.Process(target=download_image, args=(url, index, method))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    end_time = time.time() - start_time
    print(f"Total time using {method}: {end_time:.2f} seconds")


async def download_images_asyncio(urls, method):
    start_time = time.time()
    tasks = []
    for index, url in enumerate(urls):
        task = asyncio.ensure_future(download_image_async(url, index, method))
        tasks.append(task)

    await asyncio.gather(*tasks)

    end_time = time.time() - start_time
    print(f"Total time using {method}: {end_time:.2f} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images from URLs and save them to disk.")
    parser.add_argument("--urls", nargs="+", help="A list of URLs to download images from.")
    args = parser.parse_args()

    urls = args.urls
    if not urls:
        urls = image_urls

    print(f"Downloading {len(urls)} images using threading...")
    download_images_threading(urls, "threading")

    print(f"\nDownloading {len(urls)} images using multiprocessing...")
    download_images_multiprocessing(urls, "multiprocessing")

    print(f"\nDownloading {len(urls)} images using asyncio...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_images_asyncio(urls, "asyncio"))
