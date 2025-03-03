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
from django.http import Http404
def create_slug(judul):
    # Mengubah ke huruf kecil, mengganti spasi dengan tanda hubung, dan menghapus karakter non-alfanumerik
    slug = re.sub(r'[^a-z0-9\s-]', '', judul.lower())  # Menghapus karakter selain alfanumerik dan spasi
    slug = re.sub(r'[-\s]+', '-', slug)  # Mengganti spasi atau tanda hubung ganda dengan satu tanda hubung
    return slug
def fetch_data_from_api(url, params=None):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Untuk memicu exception jika status code bukan 200
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
    from django.http import Http404

def search_anime(request):
    query = request.GET.get('q', '')  # Ambil query dari parameter 'q'
    search_results = []

    if query:  # Jika ada query
        url = f"https://weeb-scraper.onrender.com/api/anoboy?s={query}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            response_data = response.json()

            # Ambil data hasil pencarian
            search_results = response_data.get('data', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching search data: {e}")
            raise Http404("Terjadi masalah saat mengambil data pencarian.")
        except ValueError as e:
            print(f"Error in response data: {e}")
            raise Http404("Data pencarian tidak valid atau tidak ditemukan.")

    context = {
        "query": query,
        "search_results": search_results,
    }
    return render(request, 'index.html', context)   

def index(request):
    #recent anime
    recent_anime_data = fetch_data_from_api(f'https://weeb-scraper.onrender.com/api/anoboy')

    # Menyiapkan konteks untuk template
    context = {
        'recentanime':recent_anime_data,
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
    url = f"http://weeb-scraper.onrender.com/api/anoboy/{anime_id}"
    response = requests.get(url)
    if response.status_code == 200:
        response_data = response.json()
        watch_anime = response_data.get('data', {}) 
        episode_navigation = watch_anime.get('episode_navigation', [])
        processed_links = []
        for episode in episode_navigation:
            nav_link = episode.get('nav_link', '')
            match = re.search(r'api/anoboy/([^/]+)', nav_link)
            if match:
                # Ekstrak parameter
                watch_anime_params = match.group(1)
                # Format URL
                processed_links.append({
                    "nav_name": episode.get('nav_name', 'Episode'),
                    "url": watch_anime_params
                })
        
    context = {
        "watch_anime": watch_anime,
        "processed_links": processed_links,
        }
    return render(request, 'watch_anime.html', context)