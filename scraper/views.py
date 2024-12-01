from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404, redirect, render
import requests
from rest_framework.response import Response
from .serializers import ScrapedDataSerializer
from .utils import scrape_mul_urls
from rest_framework.views import APIView
from .models import ScrapedData
from django.core.paginator import Paginator
from rest_framework import status
from django.contrib import messages

# Create your views here.

# def scrape_view(request):
#     urls = [
#         'https://en.m.wikipedia.org/wiki/Science',
#         'https://en.m.wikipedia.org/wiki/Artificial_intelligence',
#         'https://en.m.wikipedia.org/wiki/Python_(programming_language)',
#         'https://en.m.wikipedia.org/wiki/Blockchain',
#         'https://en.m.wikipedia.org/wiki/Nanotechnology',
#         'https://en.m.wikipedia.org/wiki/Machine_learning',
#         'https://en.m.wikipedia.org/wiki/Artificial_neural_network',
#         'https://en.m.wikipedia.org/wiki/Healthy_food',
#         'https://en.m.wikipedia.org/wiki/Geography',
#         'https://en.m.wikipedia.org/wiki/Lion',
#         'https://en.m.wikipedia.org/wiki/Quantum_mechanics',
#         'https://en.m.wikipedia.org/wiki/Django_(web_framework)',
#         'https://en.m.wikipedia.org/wiki/Bird',
#         'https://en.m.wikipedia.org/wiki/Insect',
#         'https://en.m.wikipedia.org/wiki/Tree',
#         'https://en.m.wikipedia.org/wiki/Social_media',
#         'https://en.m.wikipedia.org/wiki/Technology',
#         'https://en.m.wikipedia.org/wiki/Cryptocurrency',
#         'https://en.m.wikipedia.org/wiki/Photosynthesis',
#         'https://en.m.wikipedia.org/wiki/Black_hole',
#     ]
#     results = scrape_mul_urls(urls)
#     return render(request, 'scraper/index.html', { 'results' : results })

def scrape_view(request):
    results = ScrapedData.objects.all().order_by('-ScrapedAt')
    return render(request, 'scraper/index.html', { 'results' : results } )

class ScrapeDataAPI(APIView):
    def get(self, request):
        scraped_data = ScrapedData.objects.all()
        serializer = ScrapedDataSerializer(scraped_data, many=True)
        # serializer.save()
        page = request.GET.get('page', 1)
        page_size = 3

        paginator = Paginator(scraped_data, page_size)

        serializer = ScrapedDataSerializer(paginator.page(page), many = True)
        return Response(serializer.data)

    # return Response(serializer.errors)

    def post(self, request):
        data = request.data
        serializer = ScrapedDataSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({ 'status' : True, 'message' : 'Successfully saved the Data' }, status=status.HTTP_201_CREATED )
        else:
            return Response({ 'status' : False, 'message' : serializer.errors }, status=status.HTTP_400_BAD_REQUEST )

def scrape_url_post_view(request):
    if request.method == "POST":
        url = request.POST.get('url')
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            page_title = soup.find('title').get_text(strip=True)
            page_content = ' '.join([str(p) for p in soup.find_all('p')])
            # page_content = soup.prettify()
            scraped_data = ScrapedData.objects.create(url=url, title=page_title, content=page_content)
            # return render(request, 'scraper/scrape_form.html', { 'title' : scraped_data.title, 'content' : scraped_data.content })
            return redirect('scraped-data-detail', pk = scraped_data.id)
        except requests.exceptions.RequestException as e:
            # return render(request, 'scraper/index.html', { 'title' : page_title, 'content' : page_content })
            return render(request, 'scraper/scrape_form.html', { 'error' : str(e) })
    return render(request, 'scraper/scrape_form.html')

def scrape_data_detail_view(request, pk):
    scraped_data = get_object_or_404(ScrapedData, pk = pk)
    return render(request, 'scraper/scrape-data.html', { 'scraped_data' : scraped_data })

def search(request):
    query = request.GET['query']
    # allPosts = Post.objects.all()
    if len(query) > 74:
        scraped_data = ScrapedData.objects.none()
    else:
        scraped_dataTitle = ScrapedData.objects.filter(title__icontains=query)
        scraped_dataContent = ScrapedData.objects.filter(content__icontains=query)
        scraped_data = scraped_dataTitle.union(scraped_dataContent)

    if scraped_data.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = { 'scraped_data' : scraped_data, 'query' : query }
    return render(request, 'scraper/search.html', params)
    # return HttpResponse("This is search")