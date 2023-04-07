# import settings
from django.conf import settings
import os
import openai

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

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

def init_amazon_reviews(srcPath):
    # text loader
    loader = TextLoader(srcPath, 'utf-8')
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)    

    # json loader
    # loader = AirbyteJSONLoader('1.json')
    # documents = loader.load()

    embeddings = OpenAIEmbeddings()

    db = Chroma.from_documents(texts, embeddings)
    retriever = db.as_retriever()

    return RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)
    return RetrievalQA.from_llm(llm=OpenAI(), retriever=retriever)


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

def get_amazon_reviews(prompt):
    response = amazonQA.run(prompt)
    # response = generate_response_gpt3(prompt)
    return response

amazonQA = init_amazon_reviews('./amazon_reviews/B0839DH2LW.txt')
query = "OK"
print(amazonQA.run(query))