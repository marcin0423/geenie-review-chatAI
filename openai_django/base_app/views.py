from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .oai_queries import get_completion, get_amazon_reviews, init_all_amazon_reviews, init_pdf_embeddings


@csrf_exempt
def query_view(request):
    prompt = ''; asin = ''
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        asin = request.POST.get('asin')
    if request.method == 'GET':
        prompt = request.GET.get('prompt')
        asin = request.POST.get('asin')

    response = get_amazon_reviews(prompt, asin)
    # response = get_completion(prompt)
    return JsonResponse({'response': response})
    # return render(request, 'query.html')

@csrf_exempt
def init_view(request):
    
    init_pdf_embeddings()
    # init_all_amazon_reviews()
    # response = get_completion(prompt)
    return JsonResponse({'response': 'ok'})
    # return render(request, 'query.html')    