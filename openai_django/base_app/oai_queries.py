# import settings
from django.conf import settings
import os
import openai
from .google_drive import *
from django.conf import settings

# OpenAI API Key
if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY
else:
    raise Exception('OpenAI API Key not found')

def get_completion(prompt):
    query = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt }]
    )
    response = query.get('choices')[0]['message']['content']
    return response

# process amazon reviews #
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import AirbyteJSONLoader
from langchain.document_loaders import TextLoader

from langchain.text_splitter import CharacterTextSplitter

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings

from langchain.vectorstores import Chroma

import json
import re
from pathlib import Path
from .review_scraper import scrape_review

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
amazonReviewDir = './amazon_reviews/'
amazonQAs = []

def init_review_from_asin(asin):

    if os.path.isfile(os.path.join(amazonReviewDir, asin + '.txt')) and os.path.getsize(os.path.join(amazonReviewDir, asin + '.txt')) > 0:
        # text loader
        try:
            loader = TextLoader(amazonReviewDir + asin + '.txt', 'utf-8')
            documents = loader.load()

            text_splitter = CharacterTextSplitter(chunk_size=1024 * 2, chunk_overlap=0)
            texts = text_splitter.split_documents(documents)

            embeddings = OpenAIEmbeddings()

            db = Chroma.from_documents(texts, embeddings)
            retriever = db.as_retriever()

            return RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever), True
        except:
            return None, False
    return None, False

def init_all_amazon_reviews():    
    pathList = os.listdir(amazonReviewDir)
    for path in pathList:
        if os.path.isfile(os.path.join(amazonReviewDir, path)) and path.endswith(".txt") and os.path.getsize(os.path.join(amazonReviewDir, path)) > 0:
            asin = Path(amazonReviewDir + path).stem

            print( 'train asin:', asin )
            QA, ret = init_review_from_asin(asin)
            if ret == True:
                print('success')
                amazonQAs.append( [asin, QA] )

def generate_response_gpt3(message_list):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                     {"role": "user", "content": "Who are you?"},
                     {"role": "system",
                      "content": "You are an AI named sonic and you are in a conversation with a human. You can answer "
                                 "questions, provide information, and help with a wide variety of tasks."},
                     {"role": "assistant",
                      "content": "I am the sonic powered by ChatGpt.Contact me sonic@deadlyai.com"},
                 ] + message_list
    )

    return response["choices"][0]["message"]["content"].strip()    

def get_amazon_reviews(prompt, asin):
    for i in amazonQAs:
        if i[0] == asin:
            response = i[1].run(prompt)
            return response

    # if it doesn't exits, append new review
    print( 'train asin:', asin )
    QA, ret = init_review_from_asin(asin)
    if ret == True:
        print('success')
        amazonQAs.append( [asin, QA] )
        return get_amazon_reviews(prompt, asin)

    return "Sorry, I don't know."
    # response = generate_response_gpt3(prompt)

def save_reviews(amazonUrl, cookie, asin):
    destPath = amazonReviewDir + asin
    if os.path.exists(destPath + '.txt') and os.path.getsize(destPath + '.txt') > 0:
        return

    results = scrape_review(amazonUrl, cookie)

    destFile = open(destPath + '.txt', 'w', -1, 'utf-8')
    for result in results:
        data = result[2]
        data = re.sub('\n|\r\n', ' ', data)
        destFile.write(data)
        destFile.write('\n\n')
    destFile.close()

    jsonRet = json.dumps(results)
    destFile = open(destPath + '.json', 'w', -1, 'utf-8')
    destFile.write(jsonRet)
    destFile.close()

    upload_reviews(settings.GOOGLE_DRIVE_STORAGE_MEDIA_ROOT, destPath + '.json', asin + '.json' )

    return destPath + '.json'




# query = "OK"
# print(amazonQA.run(query))


#           Convert json 2 text
# for path in os.listdir(amazonReviewDir):
#     if os.path.isfile(os.path.join(amazonReviewDir, path)) and path.endswith(".json"):
#         srcPath = amazonReviewDir + path
#         destPath = amazonReviewDir + Path(srcPath).stem + '.txt'
#         convert_json2txt(srcPath, destPath)
#         print( 'convert asin:' + Path(srcPath).stem)

# def convert_json2txt(srcPath, destPath):
#     # srcFile = open(srcPath, 'r', -1, 'utf-8')
#     # destFile = open(destPath, 'w', -1, 'utf-8')

#     with open(srcPath, 'r', -1, 'utf-8') as srcFile:
#         with open(destPath, 'w', -1, 'utf-8') as destFile:

#             reviewArray = json.load(srcFile)

#             i = 0
#             for review in reviewArray:
#                 if review.get('customer_review'):
#                     data = review['customer_review']
#                     data = re.sub('\n|\r\n', ' ', data)
#                     destFile.write(data)
#                     destFile.write('\n\n')

#                     i = i + 1
#                 # print(i, ':', data)

#             srcFile.close()
#             destFile.close()


# PDF TRAINER #

from langchain.document_loaders import PyPDFLoader # for loading the pdf
from langchain.embeddings import OpenAIEmbeddings # for creating embeddings
from langchain.vectorstores import Chroma # for the vectorization part
from langchain.chains import ChatVectorDBChain # for chatting with the pdf
from langchain.llms import OpenAI # the LLM model we'll use (CHatGPT)

def init_pdf_embeddings():
    pdf_path = "E:/1.pdf"
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(pages, embedding=embeddings,
                                    persist_directory=".")
    vectordb.persist()

    pdf_qa = ChatVectorDBChain.from_llm(OpenAI(temperature=0.9, model_name="gpt-3.5-turbo"),
                                        vectordb, return_source_documents=True)

    while True:
        query = input()
        result = pdf_qa({"question": query, "chat_history": ""})
        print("Answer:")
        print(result["answer"])    
