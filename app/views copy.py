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


url = "https://tv1.anoboy.app/"
req = requests.get(url)

soup = BeautifulSoup(req.content, "html.parser")


output_list = []

# Mengambil elemen utama
items = soup.find_all("div", class_="amv")
# Iterasi melalui setiap elemen
for item in items:
    try:
        # Judul
        judul = item.find("h3", class_="ibox1").text.strip() if item.find("h3", class_="ibox1") else None

        # Updated at
        updated_at = item.find("div", class_="jamup").text.strip() if item.find("div", class_="jamup") else None

        # Gambar
        gambar = item.find("amp-img")["src"] if item.find("amp-img") else None
        gambar = f"https://tv1.anoboy.app{gambar}" if gambar and gambar.startswith("/") else gambar

        # Tidak ada link eksplisit pada elemen ini
        link = None

        # Menyimpan hasil
        output = {
            "judul": judul,
            "updated_at": updated_at,
            "link": link,
            "gambar": gambar
        }
        output_list.append(output)
    except AttributeError:
        # Handle jika ada elemen yang tidak lengkap
        continue

# Menampilkan hasil
for data in output_list:
    data

def filter_anime_by_timeframe(anime_data, days):
    """
    Memfilter anime berdasarkan rentang waktu terakhir (hari).
    """
    filtered_anime = []
    current_date = datetime.now()

    for anime in anime_data:
        start_date_str = anime.get('attributes', {}).get('startDate')  # Ambil startDate
        if start_date_str:
            try:
                # Konversi startDate menjadi objek datetime
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                
                # Hitung perbedaan waktu
                if current_date - start_date <= timedelta(days=days):
                    filtered_anime.append(anime)
            except ValueError:
                # Jika startDate memiliki format yang tidak sesuai
                print(f"Invalid date format: {start_date_str}")
                continue
    
    # Batasi hasil ke 5 item
    return filtered_anime[:5]
def get_season():
    """Determine the current season based on the current month."""
    month = datetime.now().month
    if 3 <= month <= 5:
        return "spring"
    elif 6 <= month <= 8:
        return "summer"
    elif 9 <= month <= 11:
        return "fall"
    else:
        return "winter"
    
def get_genres_by_anime_id(anime_id):
    """Get genres of an anime by anime_id from Kitsu API."""
    url = f'https://kitsu.io/api/edge/anime/{anime_id}'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        anime_data = response.json().get('data', {})
        included_data = response.json().get('included', [])
        
        # Extract genres from included data
        genres = [genre['attributes']['name'] for genre in included_data if genre['type'] == 'genres']
        
        return genres
    else:
        print(f"Error fetching anime data: {response.status_code}")
        return []

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

def fetch_anime_episodes(anime_id):
    """Fetch episode details for a specific anime."""
    try:
        url = f'https://kitsu.io/api/edge/anime/{anime_id}/episodes'
        request = Request(url)
        response = urlopen(request).read()
        return json.loads(response).get('data', [])
    except Exception as e:
        print(f"Error fetching anime episodes: {e}")
        return []

def fetch_data_gogonime_from_api(url, params=None):
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
def fetch_aniwatch():
    """Fetch data from the Aniwatch API."""
    try:
        url = "https://api-anime-rouge.vercel.app/aniwatch/"
        request = Request(url)
        response = urlopen(request).read()
        return json.loads(response)
    except Exception as e:
        print(f"Error fetching Aniwatch data: {e}")
        return None
def index(request):
    #recent anime
    url = "https://tv1.anoboy.app/"
    req = requests.get(url)

    soup = BeautifulSoup(req.content, "html.parser")
    output_list = []

    # Mengambil elemen utama
    items = soup.find_all("div", class_="amv")
    # Iterasi melalui setiap elemen
    for item in items:
        try:
            # Judul
            judul = item.find("h3", class_="ibox1").text.strip() if item.find("h3", class_="ibox1") else None

            # Updated at
            updated_at = item.find("div", class_="jamup").text.strip() if item.find("div", class_="jamup") else None

            # Gambar
            gambar = item.find("amp-img")["src"] if item.find("amp-img") else None
            gambar = f"https://tv1.anoboy.app{gambar}" if gambar and gambar.startswith("/") else gambar

            # Tidak ada link eksplisit pada elemen ini
            link = None

            # Menyimpan hasil
            output = {
                "judul": judul,
                "updated_at": updated_at,
                "link": link,
                "gambar": gambar
            }
            output_list.append(output)
        except AttributeError:
            # Handle jika ada elemen yang tidak lengkap
            continue

    gogonime= fetch_aniwatch()
    # Mendapatkan query pencarian
    query = request.GET.get('search_query', '')
    search_results = []

    if query:
        # URL-encode query untuk menangani karakter khusus
        encoded_query = quote_plus(query)
        search_results = fetch_data_from_api(f'https://kitsu.io/api/edge/anime', {'filter[text]': encoded_query})

    # Menentukan musim dan tahun saat ini
    current_year = datetime.now().year
    season = get_season()

    # Mengambil data anime trending (populer berdasarkan season saat ini)
    trending_anime_data = fetch_data_from_api(f'https://kitsu.io/api/edge/anime', {'filter[season]': season, 'filter[seasonYear]': current_year})
    trend_anime_data = fetch_data_from_api(f'https://kitsu.io/api/edge/trending/anime')

    # Mengambil data anime airing sekarang (seasonal anime)
    airing_now_data = fetch_data_from_api(f'https://kitsu.io/api/edge/anime', {'filter[season]': season, 'filter[seasonYear]': current_year})

    # Mengambil data top anime
    top_anime_data = fetch_data_from_api('https://kitsu.io/api/edge/anime', {'sort': '-averageRating', 'limit': 10})
    
    # Mengambil data populer anime
    popular_anime_data = fetch_data_from_api('https://kitsu.io/api/edge/anime', {'sort': 'popularityRank', 'limit': 10})
    views_anime_data = fetch_data_from_api('https://kitsu.io/api/edge/anime', {'sort': '-userCount', 'limit': 10})
    day_anime = filter_anime_by_timeframe(views_anime_data, days=1)    # Data hari terakhir
    week_anime = filter_anime_by_timeframe(views_anime_data, days=7)  # Data minggu terakhir
    month_anime = filter_anime_by_timeframe(views_anime_data, days=30)  


    # Menyiapkan konteks untuk template
    context = {
        'airing_now_data': airing_now_data[:5],
        'gogonime':gogonime,
        'recentanime':output_list[:9],
        'views_anime_data': views_anime_data[:5],
        'trend_anime_data': trend_anime_data[:5],
        'top_anime_data': top_anime_data[:6],
        'popular_anime_data': popular_anime_data[:6],
        'search_results': search_results,
        'trending_anime': trending_anime_data[:6],
        'day_anime': day_anime[:5],
        'week_anime': week_anime[:5],
        'month_anime': month_anime[:5],
    }

    return render(request, 'index.html', context)


def fetch_anime_details(anime_id):
    """Fetch anime details from Kitsu API."""
    url = f'https://kitsu.io/api/edge/anime/{anime_id}'
    response = requests.get(url)
    
    if response.status_code == 200:
        print(response.json())  # Print the entire response to debug
        return response.json().get('data', {})
    else:
        print(f"Error fetching anime details: {response.status_code}")
        return None


import requests

def fetch_anime_details_with_studios(anime_id):
    """Fetch anime details, including studio information if available."""
    base_url = "https://kitsu.io/api/edge"

    # Fetch anime details
    anime_url = f"{base_url}/anime/{anime_id}"
    anime_response = requests.get(anime_url)
    anime_data = anime_response.json().get("data", {})
    
    # Default studio data (if not available)
    studios = ["Studio data not available"]

    # Check for anime productions data
    anime_productions_url = anime_data.get("relationships", {}).get("animeProductions", {}).get("links", {}).get("related")
    
    if anime_productions_url:
        # Fetch anime productions
        productions_response = requests.get(anime_productions_url)
        productions_data = productions_response.json().get("data", [])
        
        # If there are productions, check for studio information
        for production in productions_data:
            studio_url = production.get("relationships", {}).get("studio", {}).get("links", {}).get("related")
            if studio_url:
                # Fetch studio details
                studio_response = requests.get(studio_url)
                studio_data = studio_response.json().get("data", {})
                studio_name = studio_data.get("attributes", {}).get("name", "Unknown Studio")
                studios.append(studio_name)

    return {
        "anime_data": anime_data,
        "studios": studios,
    }

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
def fetch_free_streaming_links(related_url):
    """Fetch and filter free streaming links."""
    response = requests.get(related_url)
    if response.status_code == 200:
        streaming_links = response.json().get('data', [])
        free_links = []
        for link in streaming_links:
            site = link.get('attributes', {}).get('site', '').lower()
            url = link.get('attributes', {}).get('url', '')
            if site == 'youtube' and 'watch?v=' in url:
                video_id = url.split('watch?v=')[-1]
                free_links.append({
                    'site': site,
                    'video_id': video_id,
                    'full_url': url,
                })
            elif site in ['muse asia', 'crunchyroll']:
                free_links.append({
                    'site': site,
                    'full_url': url,
                })
        return free_links
    return []
def watch_anime(request, anime_id):
    """Fetch anime details and episodes for streaming."""
    base_url = "https://kitsu.io/api/edge"
    anime_url = f"{base_url}/anime/{anime_id}"
    
    # Fetch the anime details from Kitsu API
    anime_response = requests.get(anime_url)
    if anime_response.status_code == 200:
        anime_data = anime_response.json().get("data", {})
        title = anime_data.get("attributes", {}).get("canonicalTitle", "Unknown Anime")
        
        # Attempt to fetch external link
        external_link = None
        relationships = anime_data.get("relationships", {})
        external_links = relationships.get("externalLinks", {}).get("links", {}).get("related", None)
        
        if external_links:
            external_response = requests.get(external_links)
            if external_response.status_code == 200:
                external_link_data = external_response.json().get("data", [])
                if external_link_data:
                    external_link = external_link_data[0].get("attributes", {}).get("url", None)
        # Fetch streaming links
        streaming_links = []
        streaming_links_url = anime_data.get("relationships", {}).get("streamingLinks", {}).get("links", {}).get("related", "")
        if streaming_links_url:
            streaming_links = fetch_free_streaming_links(streaming_links_url)

        # Fetch episodes
        episodes_url = relationships.get("episodes", {}).get("links", {}).get("related", "")
        episodes_data = []
        if episodes_url:
            episodes_response = requests.get(episodes_url)
            if episodes_response.status_code == 200:
                episodes_data = episodes_response.json().get("data", [])
        
        context = {
            'anime_data': anime_data,
            'episodes_data': episodes_data,
            'external_link': external_link,
            'streaming_links': streaming_links,
        }
        return render(request, 'watch_anime.html', context)
    else:
        # Handle the error case
        return render(request, '404.html', {"message": "Anime not found"})