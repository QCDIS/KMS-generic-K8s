import json
import os
import re

import numpy as np
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from spellchecker import SpellChecker


# elasticsearch_url = os.environ['ELASTICSEARCH_URL']
# elasticsearch_username = os.environ.get('ELASTICSEARCH_USERNAME')
# elasticsearch_password = os.environ.get('ELASTICSEARCH_PASSWORD')
# base_path = os.environ.get('BASE_PATH').strip()
base_path = "search"

elasticsearch_username = "elastic"
#os.environ.get('ELASTICSEARCH_USERNAME')
elasticsearch_password = "3g53NNL+Xusi3yzEV+Od"
#os.environ.get('ELASTICSEARCH_PASSWORD')
if elasticsearch_username and elasticsearch_password:
    http_auth = [elasticsearch_username, elasticsearch_password]
else:
    http_auth = None

es = Elasticsearch([{'host': 'localhost', 'port': 9200, "scheme": "https"}], http_auth=http_auth, ca_certs="/home/ubuntu/test/indexer/web_indexers/http_ca.crt")

#es = Elasticsearch(elasticsearch_url, http_auth=[elasticsearch_username, elasticsearch_password])

aggregares = {
    "repo": {
        "terms": {
            "field": "repo.keyword",
            "size": 50,
        }
    },
    "spatial_coverage": {
        "terms": {
            "field": "spatial_coverage.keyword",
            "size": 50,
        }
    },
    "theme": {
        "terms": {
            "field": "theme.keyword",
            "size": 50,
        }
    },
    "publisher": {
        "terms": {
            "field": "publisher.keyword",
            "size": 50,
        }
    },
    "instrument": {
        "terms": {
            "field": "instrument.keyword",
            "size": 50,
        }
    },
}


# ----------------------------------------------------------------------------------------
def genericsearch(request):
    try:
        term = request.GET['term']
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

    #searchResults = getSearchResults(request, facet, filter, page, term)

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
    # domain = "http://145.100.135.113:"
    
    
    port = os.environ.get('SEARCHAPI_PORT')
    domain = os.environ.get('SEARCHAPI_DOMAIN')
    append = "&"
    equal = "="

    url = domain + port + "/datasetsearch/search?" + "term" + equal + term + append + "page" + equal + page + append  + "filter" + equal + filter + append + "facet" + equal + facet
    print("Final URL for the get request = ", url)
    
    "http://145.100.135.113:8002/datasetsearch/search?term=fire+ice&page=2"

    try:
        print("************** Calling the datasetAPI from the website **************")
        response = requests.get(url)

        if response.status_code == 200:
            searchResults = response.json()
        else:
            print('Error:', response.status_code)
    except requests.exceptions.RequestException as e:
        print('Error:', e)

    return render(request, 'dataset_results.html', searchResults)


# -----------------------------------------------------------------------------------------------------------------------
# def getSearchResults(request, facet, filter, page, term):
#     print("you are here ... ... ... inside dataset search")
#     #es = Elasticsearch(elasticsearch_url, http_auth=[elasticsearch_username, elasticsearch_password])
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
#             index="dataset",
#             body={
#                 "from": page,
#                 "size": 10,
#                 "query": {
#                     "bool": {
#                         "must": {
#                             "match_all": {}
#                         },
#                         "filter": {
#                             "bool": {
#                                 "must": request.session.get('filters')
#                             }
#                         }
#                     }
#                 },
#                 "aggs": aggregares
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
#                             "fields": ["description", "keywords", "contact", "publisher", "citation",
#                                        "genre", "creator", "headline", "abstract", "theme", "producer", "author",
#                                        "sponsor", "provider", "title",
#                                        "instrument", "maintainer", "editor",
#                                        "copyrightHolder", "contributor", "contentLocation", "about", "rights",
#                                        "useConstraints",
#                                        "status", "scope", "metadataProfile", "metadataIdentifier", "distributionInfo",
#                                        "dataQualityInfo",
#                                        "contentInfo",
#                                        "repo",
#                                        "essential_variables",
#                                        "potential_topics"],
#                             "type": "best_fields",
#                             "minimum_should_match": "50%"
#                         }
#                     },
#                     "filter": {
#                         "bool": {
#                             "must": request.session.get('filters')
#                         }
#                     }
#                 }
#             },
#             "aggs": aggregares
#         }

#         result = es.search(index="dataset", body=query_body)

#     lstResults = []
#     LocationspatialCoverage = []
#     spatialCounter = 0
#     for searchResult in result['hits']['hits']:
#         lstResults.append(searchResult['_source'])
#         for potentialocation in searchResult['_source']['spatial_coverage']:
#             location = re.sub(r'[^A-Za-z0-9 ]+', '', potentialocation)
#             if (location != "") and (location != "None") and (len(location) < 20) and (
#                     location not in LocationspatialCoverage) and (spatialCounter < 10):
#                 spatialCounter = spatialCounter + 1
#                 geoLocation = {"location": location, "RI": searchResult['_source']['repo'][0]}
#                 LocationspatialCoverage.append(geoLocation)

#     # ......................
#     repo = []
#     spatial_coverage = []
#     theme = []
#     publisher = []
#     instrument = []
#     # ......................
#     for searchResult in result['aggregations']['repo']['buckets']:
#         if (searchResult['key'] != "None" and searchResult['key'] != "unknown" and searchResult['key'] != "Unknown" and
#                 searchResult['key'] != "Data" and searchResult['key'] != "Unspecified" and searchResult['key'] != "" and
#                 searchResult['key'] != "N/A"):
#             RI = {
#                 'key': searchResult['key'],
#                 'doc_count': searchResult['doc_count']
#             }
#             repo.append(RI)
#     # ......................
#     for searchResult in result['aggregations']['spatial_coverage']['buckets']:
#         if (searchResult['key'] != "None" and searchResult['key'] != "unknown" and searchResult['key'] != "Unknown" and
#                 searchResult['key'] != "Data" and searchResult['key'] != "Unspecified" and searchResult[
#                     'key'] != "N/A" and searchResult['key'] != "" and ("ANE" not in searchResult['key']) and (
#                         "Belgian" not in searchResult['key']) and ("calculated BB" not in searchResult['key']) and int(
#                         searchResult['doc_count'] > 1)):
#             SC = {
#                 'key': searchResult['key'],
#                 'doc_count': searchResult['doc_count']
#             }
#             spatial_coverage.append(SC)
#         # ......................
#     for searchResult in result['aggregations']['theme']['buckets']:
#         if (searchResult['key'] != "None" and searchResult['key'] != "unknown" and searchResult['key'] != "Unknown" and
#                 searchResult['key'] != "Data" and searchResult['key'] != "Unspecified" and searchResult[
#                     'key'] != "N/A" and searchResult['key'] != "" and int(searchResult['doc_count'] > 1)):
#             Th = {
#                 'key': searchResult['key'],
#                 'doc_count': searchResult['doc_count']
#             }
#             theme.append(Th)
#     # ......................
#     for searchResult in result['aggregations']['publisher']['buckets']:
#         if (searchResult['key'] != "None" and searchResult['key'] != "unknown" and searchResult['key'] != "Unknown" and
#                 searchResult['key'] != "Data" and searchResult['key'] != "Unspecified" and searchResult[
#                     'key'] != "N/A" and searchResult['key'] != "" and int(searchResult['doc_count'] > 1)):
#             Pub = {
#                 'key': searchResult['key'],
#                 'doc_count': searchResult['doc_count']
#             }
#             publisher.append(Pub)
#     # ......................
#     for searchResult in result['aggregations']['instrument']['buckets']:
#         if (searchResult['key'] != "None" and searchResult['key'] != "unknown" and searchResult['key'] != "Unknown" and
#                 searchResult['key'] != "Data" and searchResult['key'] != "Unspecified" and searchResult[
#                     'key'] != "N/A" and searchResult['key'] != "" and int(searchResult['doc_count'] > 1)):
#             meT = {
#                 'key': searchResult['key'],
#                 'doc_count': searchResult['doc_count']
#             }
#             instrument.append(meT)
#     # ......................
#     facets = {
#         'repo': repo,
#         'spatial_coverage': spatial_coverage,
#         'theme': theme,
#         'publisher': publisher,
#         'instrument': instrument
#     }

#     # envri-statics
#     # print("Got %d Hits:" % result['hits']['total']['value'])
#     # return JsonResponse(result, safe=True, json_dumps_params={'ensure_ascii': False})

#     numHits = result['hits']['total']['value']

#     upperBoundPage = round(np.ceil(numHits / 10) + 1)
#     if (upperBoundPage > 10):
#         upperBoundPage = 11

#     result = {
#         "facets": facets,
#         "results": lstResults,
#         "NumberOfHits": numHits,
#         "page_range": range(1, upperBoundPage),
#         "cur_page": (page / 10 + 1),
#         "searchTerm": term,
#         "functionList": getAllfunctionList(request),
#         "spatial_coverage": LocationspatialCoverage
#     }

#     print("Result Found ... ... ... ", result)
#     return result


# # -----------------------------------------------------------------------------------------------------------------------
# def synonyms(term):
#     response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
#     soup = BeautifulSoup(response.text, 'html.parser')
#     soup.find('section', {'class': 'css-191l5o0-ClassicContentCard e1qo4u830'})
#     return [span.text for span in soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})]


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


# ----------------------------------------------------------------------------------------
def rest(request):
    try:
        term = request.GET['term']
        term = term.rstrip()
        term = term.lstrip()
    except:
        term = ''
    try:
        year_from = request.GET['year_from']
    except:
        year_from = "0"
    try:
        year_to = request.GET['year_to']
    except:
        year_to = "3000"
    try:
        lon = request.GET['lon']
    except:
        lon = "0"
    try:
        lat = request.GET['lat']
    except:
        lat = "0"
    try:
        station = request.GET['station']
    except:
        station = '*'
    try:
        genre = request.GET['genre']
    except:
        genre = '*'
    try:
        author = request.GET['author']
    except:
        author = '*'
    try:
        distributor = request.GET['distributor']
    except:
        distributor = '*'
    try:
        keywords = request.GET['keywords']
    except:
        keywords = '*'
    try:
        abstract = request.GET['abstract']
    except:
        abstract = '*'

    result = esearch(all_fields=term, year_from=year_from, year_to=year_to, lon=lon,
                     lat=lat, station=station.lower(), discipline=genre.lower(), author=author.lower(),
                     distributor=distributor.lower(),
                     keywords=keywords.lower(), abstract=abstract.lower())
    return JsonResponse(result, safe=True, json_dumps_params={'ensure_ascii': False})


# ----------------------------------------------------------------
def esearch(keywords="",
            abstract="",
            all_fields="",
            year_from="",
            year_to="",
            lon="0",
            lat="0",
            station="",
            discipline="",
            author="",
            distributor="",
            ):
    client = es
    if all_fields == "*":
        filter_type_all_fields = "wildcard"
    else:
        filter_type_all_fields = "match_phrase"

    if keywords == "*":
        filter_type_keywords = "wildcard"
    else:
        filter_type_keywords = "match"

    if abstract == "*":
        filter_type_abstract = "wildcard"
    else:
        filter_type_abstract = "match"

    if station == '*':
        filter_type_provider = "wildcard"
    else:
        filter_type_provider = "match_phrase"

    if discipline == '*':
        filter_type_genre = "wildcard"
    else:
        filter_type_genre = "match_phrase"

    if author == '*':
        filter_type_author = "wildcard"
    else:
        filter_type_author = "match_phrase"

    if distributor == '*':
        filter_type_distributor = "wildcard"
    else:
        filter_type_distributor = "match_phrase"

    if lon == "0":
        lon_gte = "-90.0"
        lon_lte = "90.0"

    else:
        lon_gte = (float(lon) - 1)
        lon_lte = (float(lon) + 1)

    if lat == "0":
        lat_gte = "-90.0"
        lat_lte = "90.0"

    else:
        lat_gte = (float(lat) - 1)
        lat_lte = (float(lat) + 1)

    q = Q("bool",

          should=[
              Q(filter_type_all_fields, keywords=keywords),
              Q(filter_type_all_fields, abstract=abstract),
              Q(filter_type_all_fields, keywords=all_fields),
              Q(filter_type_all_fields, abstract=all_fields),
              Q(filter_type_all_fields, title=all_fields),
              Q(filter_type_all_fields, material=all_fields),
              Q(filter_type_all_fields, publisher=all_fields),
              Q(filter_type_all_fields, description=all_fields),
              Q(filter_type_all_fields, provider=all_fields),
              Q(filter_type_all_fields, distributionInfo=all_fields),
              Q(filter_type_all_fields, about=all_fields),
              Q(filter_type_all_fields, citation=all_fields),
              Q(filter_type_all_fields, responsibleParty=all_fields),
              Q(filter_type_all_fields, creator=all_fields),
              Q(filter_type_all_fields, accountablePerson=all_fields),
              Q(filter_type_all_fields, locationCreated=all_fields),
          ],
          minimum_should_match=1
          )

    s = Search(using=client, index="dataset") \
            .filter("range", temporal={'gte': year_from, 'lte': year_to}) \
            .filter("range", longitude={'gte': lon_gte, 'lte': lon_lte}) \
            .filter("range", latitude={'gte': lat_gte, 'lte': lat_lte}) \
            .filter(filter_type_provider, provider=station) \
            .filter(filter_type_genre, genre=discipline) \
            .filter(filter_type_distributor, distributor=distributor) \
            .filter(filter_type_author, author=author) \
            .query(q)[:1000]

    response = s.execute()
    search = get_results_rest(response)
    return search


# ----------------------------------------------------------------------------------------

def get_results_rest(response):
    results = {}
    for hit in response:
        result = {
            'identifier': str(hit.identifier),
            'title': str(hit.title),
            'temporal': str(hit.temporal),
            'author': [name for name in hit.author],
            'landing_page': str(hit.landing_page),
            'keywords': [keyword for keyword in hit.keywords],
            'distributor': str(hit.distributor),
            'station': str(hit.provider),
            'genre': str(hit.genre),
            'longitude': str(hit.longitude),
            'latitude': str(hit.latitude),
            'abstract': str(hit.abstract)
        }
        results[hit.identifier] = result
    return results


# -----------------------------------------------------------------------------------------------------------------------
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
