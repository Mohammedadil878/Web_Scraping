# from django.contrib import admin
from django.urls import path
from scraper import views
# from .views import scrape_view, scrape_url_post_view, scrape_data_detail_view

urlpatterns = [
    path('', views.scrape_view, name='scraper'),
    path('scrape-url/', views.scrape_url_post_view, name='scrape-url-post'),
    path('scrape-data/<int:pk>/', views.scrape_data_detail_view, name='scraped-data-detail'),
    path('search/', views.search, name='search'),
]
