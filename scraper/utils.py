import requests
from bs4 import BeautifulSoup

def scrape_mul_urls(urls):
    # Create a list to store the scraped data
    scraped_data = []
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract the title of the webpage
            page_title = soup.title.string if soup.title else "No Title found"
            scraped_data.append({ 'url' : url, 'title' : page_title })
        except requests.exceptions.RequestException as e:
            scraped_data.append({ 'url' : url, 'error' : str(e) })
    return scraped_data
