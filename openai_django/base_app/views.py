from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .oai_queries import get_completion, get_amazon_reviews


@csrf_exempt
def query_view(request):
    prompt = ''
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
    if request.method == 'GET':
        prompt = request.GET.get('prompt')

    response = prompt
    # response = get_amazon_reviews(prompt)
    # response = get_completion(prompt)
    return JsonResponse({'response': response})
    # return render(request, 'query.html')
