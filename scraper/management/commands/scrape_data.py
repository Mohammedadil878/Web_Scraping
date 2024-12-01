from typing import Any
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from scraper.models import ScrapedData

class Command(BaseCommand):
    help = 'Scrapes the data and saves to the database'

    def handle(self, *args, **kwargs):
        urls = [  
            'https://en.m.wikipedia.org/wiki/Science',
            'https://en.m.wikipedia.org/wiki/Artificial_intelligence',
            'https://en.m.wikipedia.org/wiki/Python_(programming_language)',
            'https://en.m.wikipedia.org/wiki/Blockchain',
            'https://en.m.wikipedia.org/wiki/Nanotechnology',
            'https://en.m.wikipedia.org/wiki/Machine_learning',
            'https://en.m.wikipedia.org/wiki/Artificial_neural_network',
            'https://en.m.wikipedia.org/wiki/Healthy_food',
            'https://en.m.wikipedia.org/wiki/Geography',
            'https://en.m.wikipedia.org/wiki/Lion',
            'https://en.m.wikipedia.org/wiki/Quantum_mechanics',
            'https://en.m.wikipedia.org/wiki/Django_(web_framework)',
            'https://en.m.wikipedia.org/wiki/Bird',
            'https://en.m.wikipedia.org/wiki/Insect',
            'https://en.m.wikipedia.org/wiki/Tree',
            'https://en.m.wikipedia.org/wiki/Social_media',
            'https://en.m.wikipedia.org/wiki/Technology',
            'https://en.m.wikipedia.org/wiki/Cryptocurrency',
            'https://en.m.wikipedia.org/wiki/Photosynthesis',
            'https://en.m.wikipedia.org/wiki/Black_hole',
        ]

        for url in urls:
            self.stdout.write(f'Scraping the data and Storing in the Database')
            try:
                # response = requests.get(url)
                # response.raise_for_status()
            #     soup = BeautifulSoup(response.content, 'html.parser')
            #     page_title = soup.title.string if soup.title else "No Title found"
            #     page_content = ' '.join([p.get_text() for p in soup.find_all('p')])
            #     ScrapedData.objects.create(url = url, title = page_title, content = page_content)
            #     self.stdout.write(self.style.SUCCESS(f'Successfully Scraped and saved { url }: {page_title}'))
            # except requests.exceptions.RequestException as e:
            #     self.stdout.write(self.style.ERROR(f'Failed to scrape { url }: { str(e) }'))

                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                page_title = soup.find('title').get_text(strip=True)
                # page_content = soup.find('<p>').get_text(strip=True)
                # page_content = soup.prettify()
                page_content = ' '.join([str(p) for p in soup.find_all('p')])
                ScrapedData.objects.create(url = url, title = page_title, content = page_content)
                self.stdout.write(self.style.SUCCESS(f'Successfully Scraped and saved { url } : { page_title }'))
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Failed to scrape { url } : { str(e) }'))











'''This is another method which is already written in the utils.py'''

# def scrape_mul_urls(urls):
#     # Create a list to store the scraped data
#     scraped_data = []
#     for url in urls:
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.content, 'html.parser')
#             # Extract the title of the webpage
#             page_title = soup.title.string if soup.title else "No Title found"
#             scraped_data.append({ 'url' : url, 'title' : page_title })
#         except requests.exceptions.RequestException as e:
#             scraped_data.append({ 'url' : url, 'error' : str(e) })
#     return scraped_data


