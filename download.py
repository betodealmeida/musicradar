import os.path
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests


baseurl = 'https://www.musicradar.com/news/tech/free-music-samples-download-loops-hits-and-multis-627820'
content = requests.get(baseurl).text
soup = BeautifulSoup(content, 'html.parser')
for link in soup.findAll('a', attrs={'href': re.compile("^https?://")}):
    if not link.text.endswith('samples'):
        continue

    content = requests.get(link['href']).text
    sample_soup = BeautifulSoup(content, 'html.parser')
    download_link = sample_soup.find('a', attrs={'href': re.compile(".*\.zip$")})
    if download_link is None:
        continue

    url = download_link['href']
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    if os.path.exists(filename):
        continue

    print(f'Downloading from {url}')
    content = requests.get(url, stream=True)

    with open(filename, 'wb') as f:
        print(f'Writing {filename}')
        for chunk in content.iter_content(chunk_size=1024):
            if chunk:            
                f.write(chunk)
