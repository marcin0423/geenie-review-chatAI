from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .oai_queries import *


@csrf_exempt
def chat_review(request):
    prompt = ''; asin = ''
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        asin = request.POST.get('asin')
    if request.method == 'GET':
        prompt = request.GET.get('prompt')
        asin = request.POST.get('asin')

    response = get_amazon_reviews(prompt, asin)
    return JsonResponse({'response': response})

@csrf_exempt
def ext_chat_review(request):
    prompt = ''; asin = ''; amazonUrl = ''; cookie = ''
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        asin = request.POST.get('asin')
        amazonUrl = request.POST.get('url')
        cookie = request.POST.get('cookie')
    if request.method == 'GET':
        prompt = request.GET.get('prompt')
        asin = request.GET.get('asin')
        amazonUrl = request.GET.get('url')
        cookie = request.GET.get('cookie')

    if prompt == None or prompt == '':
        return JsonResponse({'response': 'Fetch error, try again'})
    if asin == None or asin == '':
        return JsonResponse({'response': 'Fetch error, try again'})
    if amazonUrl == None or amazonUrl == '':
        return JsonResponse({'response': 'Fetch error, try again'})
    if cookie == None or cookie == '':
        return JsonResponse({'response': 'Fetch error, try again'})

    reviewPath = save_reviews(amazonUrl, cookie, asin)
    response = get_amazon_reviews(prompt, asin)

    return JsonResponse({'response': response})

@csrf_exempt
def init_view(request):
    
    init_pdf_embeddings()
    # init_all_amazon_reviews()
    # response = get_completion(prompt)
    return JsonResponse({'response': 'ok'})
    # return render(request, 'query.html')    