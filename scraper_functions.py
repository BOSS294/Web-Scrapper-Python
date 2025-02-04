import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm  
from concurrent.futures import ThreadPoolExecutor


def get_page_info(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title.get_text(strip=True) if soup.title else "No Title"
        
        meta_tags = {
            "description": "No Description",
            "keywords": "No Keywords",
            "og:title": "No OG Title",
            "og:description": "No OG Description",
            "twitter:title": "No Twitter Title",
            "twitter:description": "No Twitter Description"
        }

        for meta in soup.find_all('meta'):
            meta_name = meta.get('name') or meta.get('property')  
            if meta_name in meta_tags:
                meta_tags[meta_name] = meta.get('content', '').strip()

        return title, meta_tags["description"], meta_tags["keywords"], meta_tags["og:title"], meta_tags["og:description"], meta_tags["twitter:title"], meta_tags["twitter:description"]

    except requests.exceptions.RequestException:
        return "Error Fetching Data", "Error Fetching Data", "Error", "Error", "Error", "Error", "Error"


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_images(url, folder_name, downloaded_images, log_func):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        images = soup.find_all('img')

        
        media_folder = os.path.join(folder_name, "Media", os.path.basename(folder_name))
        os.makedirs(media_folder, exist_ok=True)

        for img in images:
            img_url = img.get('src') or img.get('data-src')
            if img_url:
                img_url = urljoin(url, img_url)  

                if img_url in downloaded_images:
                    continue

                img_ext = os.path.splitext(img_url)[1].lower()
                if img_ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    continue  

                img_name = os.path.join(media_folder, sanitize_filename(os.path.basename(img_url)))

                try:
                    img_data = requests.get(img_url, timeout=10).content
                    with open(img_name, 'wb') as file:
                        file.write(img_data)
                        downloaded_images.add(img_url)
                        log_func(f"Downloaded Image: {img_name}", "green")
                except requests.exceptions.RequestException:
                    log_func(f"Error downloading {img_url}", "red")
    except requests.exceptions.RequestException:
        log_func(f"Error fetching images from {url}", "red")


def save_to_csv(data, site_name):
    folder_path = f"SITE/{site_name}"
    os.makedirs(folder_path, exist_ok=True)

    csv_file = os.path.join(folder_path, f"{site_name}_data.csv")

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URL', 'Page Title', 'Meta Description', 'Keywords', 'OG Title', 'OG Description', 'Twitter Title', 'Twitter Description'])
        writer.writerows(data)



def save_to_json(data, site_name):
    folder_path = f"SITE/{site_name}"
    os.makedirs(folder_path, exist_ok=True)

    json_file = os.path.join(folder_path, f"{site_name}_data.json")

    with open(json_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

def fetch_links(url, log_func, scraped_data, folder_name, downloaded_images):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')

        
        download_images(url, folder_name, downloaded_images, log_func)

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for link in links:
                href = link.get('href')
                if href:
                    full_url = urljoin(url, href)
                    
                    futures.append(executor.submit(process_link, full_url, log_func, scraped_data))  

            for future in tqdm(futures, desc="Processing Links", unit="link"):
                future.result()

    except requests.exceptions.RequestException:
        log_func(f"[ERROR] Failed to fetch links from {url}", "red")



def process_link(full_url, log_func, scraped_data):
    title, description, keywords, og_title, og_desc, twitter_title, twitter_desc = get_page_info(full_url)

    log_func(f"Scraped: {full_url} | Title: {title}", "cyan")

    scraped_data.append([full_url, title, description, keywords, og_title, og_desc, twitter_title, twitter_desc])




def scrape_website(url, log_func):
    parsed_url = urlparse(url)
    site_name = parsed_url.netloc.split('.')[0] if parsed_url.netloc else "Unknown_Site"

    folder_name = f"SITE/{site_name}"
    downloaded_images = set()
    scraped_data = []

    log_func("Initializing web scraping...", "yellow")

    try:
        
        fetch_links(url, log_func, scraped_data, folder_name, downloaded_images)

        
        save_to_csv(scraped_data, site_name)
        save_to_json(scraped_data, site_name)
        log_func(f"Data saved to {folder_name}/data.json", "lime")

    except requests.exceptions.RequestException:
        log_func(f"[ERROR] Error scraping {url}", "red")

    log_func("Web Scraping Complete", "cyan")



def log_func(message, color="white"):
    colors = {"red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m", "cyan": "\033[96m", "lime": "\033[92m"}
    reset = "\033[0m"
    print(f"{colors.get(color, '')}{message}{reset}")
