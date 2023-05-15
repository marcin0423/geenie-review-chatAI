from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .oai_queries import *


# @csrf_exempt
# def chat_review(request):
#     prompt = ''; asin = ''
#     if request.method == 'POST':
#         prompt = request.POST.get('prompt')
#         asin = request.POST.get('asin')
#     if request.method == 'GET':
#         prompt = request.GET.get('prompt')
#         asin = request.POST.get('asin')

#     response = get_amazon_reviews(prompt, asin)
#     return JsonResponse({'response': response})

# @csrf_exempt
# def ext_chat_review(request):
#     type = ''; prompt = ''; asin = ''; amazonUrl = ''; cookie = ''
#     if request.method == 'POST':
#         prompt = request.POST.get('prompt')
#         asin = request.POST.get('asin')
#         amazonUrl = request.POST.get('url')
#         cookie = request.POST.get('cookie')
#         type = request.POST.get('type')
#     if request.method == 'GET':
#         prompt = request.GET.get('prompt')
#         asin = request.GET.get('asin')
#         amazonUrl = request.GET.get('url')
#         cookie = request.GET.get('cookie')
#         type = request.GET.get('type')

#     print(prompt, asin, amazonUrl, cookie)

#     # if prompt == None or prompt == '':
#     #     return JsonResponse({'response': 'Fetch error, try again'})
#     if asin == None or asin == '':
#         return JsonResponse({'response': 'Fetch error, try again'})
#     if amazonUrl == None or amazonUrl == '':
#         return JsonResponse({'response': 'Fetch error, try again'})
#     # if cookie == None or cookie == '':
#     #     return JsonResponse({'response': 'Fetch error, try again'})

#     reviewPath, pdInfo = save_reviews(amazonUrl, cookie, asin)

#     if type == "initReviews" :
#         prompts = [ 
#             { 'title': '🌟Top Negative Keywords and Phrases', 'question':'Please provide a 5-7 bullet-point list of the most frequently mentioned negative keywords and phrases in the customer reviews, indicating areas for improvement. Include relevant quotations or snippets from the reviews to illustrate each point. Additionally, include an estimated hit rate in percentage (no more than 60%) for each topic, representing how often it appears in the reviews.', 'answer': ''},
#             { 'title': '🌟Top Positive Keywords and Phrases', 'question':'Please provide a 5 bullet-point list of the most frequently mentioned positive keywords and phrases in the customer reviews, indicating areas for improvement. Include relevant quotations or snippets from the reviews to illustrate each point. Additionally, provide an estimated hit rate in percentage (no more than 60%) for each topic, representing how often it appears in the reviews.', 'answer': ''},
#             { 'title': '🌟Product Features Requests:', 'question':'Analyze the customer reviews to identify 4 to 8 product features that could be improved, starting with the most requested feature. For each feature, provide a practical suggestion on how to improve the product.', 'answer': ''},
#             { 'title': '🌟New Variation Recommendations:', 'question':'Analyze the customer reviews and identify product variation suggestions, such as additional colors, sizes, or flavors, that customers mention. Please provide a bullet-point list of the new variation ideas.', 'answer': ''},
#             { 'title': '🌟Bundle opportunities:',     'question':"Analyze the customer reviews and examine research on the consumer decision-making process within the product's niche, providing a brief overview of the stages customers go through before making a purchase and any unique aspects related to this product category.", 'answer': ''}
#         ]
#         for prompt in prompts:
#             response = get_amazon_reviews(prompt.get("question"), asin)
#             prompt["answer"] = response
#         return JsonResponse({'productInformation': pdInfo, 'response': json.dumps(prompts)})
#     if type == "QA" :
#         response = get_amazon_reviews(prompt, asin)
#         return JsonResponse({'response': response})

# @csrf_exempt
# def init_pdInfos(request):
#     asin = ''; amazonUrl = ''; cookie = ''
#     if request.method == 'POST':
#         asin = request.POST.get('asin')
#         amazonUrl = request.POST.get('url')
#         cookie = request.POST.get('cookie')
#     if request.method == 'GET':
#         prompt = request.GET.get('prompt')
#         asin = request.GET.get('asin')
#         amazonUrl = request.GET.get('url')
#         cookie = request.GET.get('cookie')

#     if asin == None or asin == '':
#         return JsonResponse({'response': 'Fetch error, try again'})
#     if amazonUrl == None or amazonUrl == '':
#         return JsonResponse({'response': 'Fetch error, try again'})    

# @csrf_exempt
# def init_view(request):
    
#     init_pdf_embeddings()
#     # init_all_amazon_reviews()
#     # response = get_completion(prompt)
#     return JsonResponse({'response': 'ok'})
#     # return render(request, 'query.html')    

@csrf_exempt
def getProductInformation(request):
    asin = ''; amazonUrl = ''; cookie = ''
    if request.method == 'POST':
        asin = request.POST.get('asin')
        amazonUrl = request.POST.get('url')
        cookie = request.POST.get('cookie')
    if request.method == 'GET':
        prompt = request.GET.get('prompt')
        asin = request.GET.get('asin')
        amazonUrl = request.GET.get('url')
        cookie = request.GET.get('cookie')

    if asin == None or asin == '':
        return JsonResponse({'response': 'Fetch error, try again'})
    if amazonUrl == None or amazonUrl == '':
        return JsonResponse({'response': 'Fetch error, try again'})
    
    pdInfo = scrape_amazon_data(amazonUrl, cookie, True)
    return JsonResponse({'response': pdInfo})

@csrf_exempt
def getAnswerFromReviews(request):
    asin = ''; amazonUrl = ''; cookie = ''; prompt = ''
    if request.method == 'POST':
        asin = request.POST.get('asin')
        amazonUrl = request.POST.get('url')
        cookie = request.POST.get('cookie')
        prompt = request.POST.get('prompt')
    if request.method == 'GET':
        asin = request.GET.get('asin')
        amazonUrl = request.GET.get('url')
        cookie = request.GET.get('cookie')
        prompt = request.GET.get('prompt')

    if asin == None or asin == '':
        return JsonResponse({'response': 'Fetch error, try again'})
    if amazonUrl == None or amazonUrl == '':
        return JsonResponse({'response': 'Fetch error, try again'})
    if prompt == None or prompt == '':
        return JsonResponse({'response': 'Fetch error, try again'})

    save_reviews(amazonUrl, cookie, asin)

    if prompt == 'Initial Question':
        prompts = [ 
            { 'asin': asin, 'title': '🌟Top Negative Keywords and Phrases', 'question':'Please provide a 5-7 bullet-point list of the most frequently mentioned negative keywords and phrases in the customer reviews, indicating areas for improvement. Include relevant quotations or snippets from the reviews to illustrate each point. Additionally, include an estimated hit rate in percentage (no more than 60%) for each topic, representing how often it appears in the reviews.', 'answer': ''},
            { 'asin': asin, 'title': '🌟Top Positive Keywords and Phrases', 'question':'Please provide a 5 bullet-point list of the most frequently mentioned positive keywords and phrases in the customer reviews, indicating areas for improvement. Include relevant quotations or snippets from the reviews to illustrate each point. Additionally, provide an estimated hit rate in percentage (no more than 60%) for each topic, representing how often it appears in the reviews.', 'answer': ''},
            { 'asin': asin, 'title': '🌟Product Features Requests:', 'question':'Analyze the customer reviews to identify 4 to 8 product features that could be improved, starting with the most requested feature. For each feature, provide a practical suggestion on how to improve the product.', 'answer': ''},
            { 'asin': asin, 'title': '🌟New Variation Recommendations:', 'question':'Analyze the customer reviews and identify product variation suggestions, such as additional colors, sizes, or flavors, that customers mention. Please provide a bullet-point list of the new variation ideas.', 'answer': ''},
            { 'asin': asin, 'title': '🌟Bundle opportunities:',     'question':"Analyze the customer reviews and examine research on the consumer decision-making process within the product's niche, providing a brief overview of the stages customers go through before making a purchase and any unique aspects related to this product category.", 'answer': ''}
        ]
        for item in prompts:
            ret, response = getAnswer(item.get("question"), asin)
            item["answer"] = response
        return JsonResponse({'response': json.dumps(prompts)})
    else:
        ret, response = getAnswer(prompt, asin)
        return JsonResponse({'response': response})
    
    return JsonResponse({'response': pdInfo})    