from django.shortcuts import render
from django.shortcuts import render
import requests
from datetime import datetime
import math
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
import json
import requests
from datetime import datetime
from django.shortcuts import render
from urllib.parse import quote_plus
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from anime_api.apis import HmtaiAPI
from anime_api.apis.hmtai.types import ImageCategory
from bs4 import BeautifulSoup
import requests
import re
def create_slug(judul):
    # Mengubah ke huruf kecil, mengganti spasi dengan tanda hubung, dan menghapus karakter non-alfanumerik
    slug = re.sub(r'[^a-z0-9\s-]', '', judul.lower())  # Menghapus karakter selain alfanumerik dan spasi
    slug = re.sub(r'[-\s]+', '-', slug)  # Mengganti spasi atau tanda hubung ganda dengan satu tanda hubung
    return slug
def fetch_data_from_api(url, params=None):
    """Fungsi untuk melakukan request ke API dan mengembalikan data JSON."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Untuk memicu exception jika status code bukan 200
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []

def index(request):
    #recent anime
    recent_anime_data = fetch_data_from_api(f'https://weeb-scraper.onrender.com/api/anoboy')

    # Menyiapkan konteks untuk template
    context = {
        'recentanime':recent_anime_data,
        # 'rekomendasi':output_list[:9],
    }

    return render(request, 'index.html', context)


def anime_detail_view(request, anime_id):
    """Fetch anime details from Kitsu API."""
    url = f'https://kitsu.io/api/edge/anime/{anime_id}'
    response = requests.get(url)
    if response.status_code == 200:
        response_data = response.json()
        anime_data = response_data.get('data', {}) 
        

    context = {
        # 'studios': studios['studios'],
        'anime_data': anime_data,
    }
    
    return render(request, 'anime-view.html', context)
def watch_anime(request, anime_id):
    url = f"http://weeb-scraper.onrender.com/api/anoboy/{anime_id}/"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")

    # Mengambil data yang diinginkan
    pagetitle = soup.find("div", class_="pagetitle").h1.text.strip() if soup.find("div", class_="pagetitle") else None
    name = soup.find("span", itemprop="name").text.strip() if soup.find("span", itemprop="name") else None
    episode = soup.find("span", itemprop="name").text.strip() if soup.find("span", itemprop="name") else None
    update_at = soup.find("time", class_="updated").text.strip() if soup.find("time", class_="updated") else None
    judul = soup.find("h1").text.strip() if soup.find("h1") else None
    centered_div = soup.find("iframe", id="mediaplayer")
    b_tube_section = soup.find("div", id="centered")

    # Extract all anchor tags within this section
    section = soup.find("div", id="centered")  # Adjust the selector as needed
    if section:
        links = section.find_all("a", class_="link")
        for link in links:
            resolution = link.text.strip()
            href = link.get("href")
            print(f"Resolution: {resolution}, Link: {href}")
    else:
        print("No section with the specified ID was found.")

    # Iterate through the links and print the href attributes
    # for link in links:
    #     resolution = link.text.strip()
    #     href = link.get("href")
    #     print(f"Resolution: {resolution}, Link: {href}")
    # link = soup.find("div",class_="column-three-fourth")
    # if centered_div:
    #     # Extract all the links inside this div
    #     links = [a['href'] for a in centered_div.find_all('a', href=True)]
    #     print(links)
    # else:
    #     print("The div with id 'centered' was not found.")
    context = {
        "pagetitle": pagetitle,
        "name": name,
        "episode": episode,
        "update_at": update_at,
        "judul": judul,
        # "links": link
        }
    return render(request, 'watch_anime.html', context)