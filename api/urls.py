from django.urls import path
from scraper import views
from scraper.views import ScrapeDataAPI

urlpatterns = [
    path('scraped-data/', ScrapeDataAPI.as_view(), name='scrape'),
]