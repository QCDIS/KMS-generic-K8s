import os

import numpy as np
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from elasticsearch import Elasticsearch
from spellchecker import SpellChecker

# elasticsearch_url = os.environ['ELASTICSEARCH_URL']
# elasticsearch_username = os.environ.get('ELASTICSEARCH_USERNAME')
# elasticsearch_password = os.environ.get('ELASTICSEARCH_PASSWORD')
# base_path = os.environ.get('BASE_PATH').strip()
base_path = "search"
# es = Elasticsearch(elasticsearch_url, http_auth=[elasticsearch_username, elasticsearch_password])


# # Nafis Updated Elastic
# elasticsearch_username = "elastic"
# #os.environ.get('ELASTICSEARCH_USERNAME')
# elasticsearch_password = "3g53NNL+Xusi3yzEV+Od"
# #os.environ.get('ELASTICSEARCH_PASSWORD')
# if elasticsearch_username and elasticsearch_password:
#     http_auth = [elasticsearch_username, elasticsearch_password]
# else:
#     http_auth = None

# es = Elasticsearch([{'host': 'localhost', 'port': 9200, "scheme": "https"}], http_auth=http_auth, ca_certs="/home/ubuntu/test/indexer/web_indexers/http_ca.crt")


# -------------------------------------------------------------------------------------------
def genericsearch(request):
    try:
        term = request.GET['term']
    except:
        term = ''
    response_data = {}

    if (term == "*"):
        term = ""
    # response_data= search_github_by_url(term)
    #   response_data=search_repository_github(term)
    # search_projects_Gitlab(term)

    #   indexFile= open("notebooks.json","w+")
    #   indexFile.write(json.dumps(response_data))
    #   indexFile.close()

    #    return HttpResponse(json.dumps(response_data), content_type="application/json")

    try:
        term = request.GET['term']
        term = term.rstrip()
        term = term.lstrip()
    except:
        term = ''

    try:
        page = request.GET['page']
    except:
        page = 0

    try:
        filter = request.GET['filter']
    except:
        filter = ''

    try:
        facet = request.GET['facet']
    except:
        facet = ''

    # searchResults = getSearchResults(request, facet, filter, page, term)

    # searchResults['suggestedSearchTerm'] = ''
    # if searchResults['NumberOfHits'] == 0:
    #     suggestedSearchTerm = potentialSearchTerm(term)
    #     suggestedResults = getSearchResults(request, facet, filter, page, suggestedSearchTerm)
    #     if suggestedResults["NumberOfHits"] > 0:
    #         searchResults["suggestedSearchTerm"] = suggestedSearchTerm

    # searchResults['base_path'] = base_path

    # port = "8004"
    # append = "&"
    # equal = "="

    port = os.environ.get('SEARCHAPI_PORT')
    domain = os.environ.get('SEARCHAPI_DOMAIN')
    append = "&"
    equal = "="

    url = domain + port + "/notebooksearch/search?" + "term" + equal + term + append + "page" + equal + page + append  + "filter" + equal + filter + append + "facet" + equal + facet
    print("Final URL for the get request = ", url)
    
    "http://145.100.135.113:8002/notebooksearch/search?term=fire+ice&page=2"

    try:
        print("************** Calling the notebookAPI from the website **************")
        response = requests.get(url)

        if response.status_code == 200:
            searchResults = response.json()
        else:
            print('Error:', response.status_code)
    except requests.exceptions.RequestException as e:
        print('Error:', e)

    return render(request, 'notebook_results.html', searchResults)


# # -----------------------------------------------------------------------------------------------------------------------
# def potentialSearchTerm(term):
#     spell = SpellChecker()
#     search_term = term.split()
#     alternative_search_term = ""
#     for sTerm in search_term:
#         alter_word = spell.correction(sTerm)
#         if alter_word:
#             alternative_search_term = alternative_search_term + " " + alter_word

#     alternative_search_term = alternative_search_term.rstrip()
#     alternative_search_term = alternative_search_term.lstrip()

#     if alternative_search_term == term:
#         alternative_search_term = ""
#         for sTerm in search_term:
#             syn = synonyms(sTerm)
#             if len(syn) > 0:
#                 alter_word = syn[0]
#                 alternative_search_term = alternative_search_term + " " + alter_word

#     alternative_search_term = alternative_search_term.rstrip()
#     alternative_search_term = alternative_search_term.lstrip()

#     return alternative_search_term




# # -----------------------------------------------------------------------------------------------------------------------

# def getSearchResults(request, facet, filter, page, term):
#     if filter != "" and facet != "":
#         saved_list = request.session['filters']
#         saved_list.append({"term": {facet + ".keyword": filter}})
#         request.session['filters'] = saved_list
#     else:
#         if 'filters' in request.session:
#             del request.session['filters']
#         request.session['filters'] = []

#     page = (int(page) - 1) * 10
#     result = {}
#     if term == "*" or term == "top10":
#         result = es.search(
#             index="notebooks",
#             body={
#                 "from": page,
#                 "size": 10,
#                 "query": {
#                     "bool": {
#                         "must": {
#                             "match_all": {}
#                         }
#                     }
#                 }
#             }
#         )
#     else:
#         user_request = "some_param"
#         query_body = {
#             "from": page,
#             "size": 10,
#             "query": {
#                 "bool": {
#                     "must": {
#                         "multi_match": {
#                             "query": term,
#                             "fields": ["name", "description"],
#                             "type": "best_fields",
#                             "minimum_should_match": "50%"
#                         }
#                     },
#                 }
#             }
#         }

#         result = es.search(index="notebooks", body=query_body)
#     lstResults = []

#     for searchResult in result['hits']['hits']:
#         lstResults.append(searchResult['_source'])

#     numHits = result['hits']['total']['value']

#     upperBoundPage = round(np.ceil(numHits / 10) + 1)
#     if (upperBoundPage > 10):
#         upperBoundPage = 11

#     facets = []

#     results = {
#         "facets": facets,
#         "results": lstResults,
#         "NumberOfHits": numHits,
#         "page_range": range(1, upperBoundPage),
#         "cur_page": (page / 10 + 1),
#         "searchTerm": term,
#         "functionList": getAllfunctionList(request)
#     }

#     return results


# # -----------------------------------------------------------------------------------------------------------------------
# def synonyms(term):
#     response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
#     soup = BeautifulSoup(response.text, 'html.parser')
#     soup.find('section', {'class': 'css-191l5o0-ClassicContentCard e1qo4u830'})
#     return [span.text for span in soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})]

# # -----------------------------------------------------------------------------------------------------------------------
# def getAllfunctionList(request):
#     if not 'BasketURLs' in request.session or not request.session['BasketURLs']:
#         request.session['BasketURLs'] = []
#     if not 'MyBasket' in request.session or not request.session['MyBasket']:
#         request.session['MyBasket'] = []

#     functionList = ""
#     saved_list = request.session['MyBasket']
#     for item in saved_list:
#         functionList = functionList + r"modifyCart({'operation':'add','type':'" + item['type'] + "','title':'" + item[
#             'title'] + "','url':'" + item['url'] + "','id':'" + item['id'] + "' });"
#     return functionList
