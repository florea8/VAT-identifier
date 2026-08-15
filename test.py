import requests
from bs4 import BeautifulSoup
import os

# Base URL pentru sectiunea de date de import/export HMRC
PAGE_URL = "https://www.uktradeinfo.com/trade-data/uk-importers-details/"

def get_latest_importers_dataset():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(PAGE_URL, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Eroare la accesarea paginii: {response.status_code}")
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Caută link-urile de descărcare pentru fișierele .csv sau .zip
    download_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.csv') or href.endswith('.zip'):
            if not href.startswith('http'):
                href = f"https://www.uktradeinfo.com{href}"
            download_links.append(href)
            
    if not download_links:
        print("Nu au fost găsite fișiere CSV/ZIP direct pe pagină. Verifică API-ul de date sau structura HTML.")
        return None
        
    # Descarcă cel mai recent fișier găsitor
    latest_file_url = download_links[0]
    filename = latest_file_url.split('/')[-1]
    
    print(f"Descărcare dataset: {filename} de la {latest_file_url}")
    file_res = requests.get(latest_file_url, headers=headers)
    
    with open(filename, 'wb') as f:
        f.write(file_res.content)
        
    print(f"Fișier salvat local ca: {filename}")
    return filename

# Rulare:
# downloaded_file = get_latest_importers_dataset()