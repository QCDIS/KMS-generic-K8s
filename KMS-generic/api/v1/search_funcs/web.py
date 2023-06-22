import os

import numpy as np
from elasticsearch import Elasticsearch

elasticsearch_url = os.environ['ELASTICSEARCH_URL']
elasticsearch_username = os.environ.get('ELASTICSEARCH_USERNAME')
elasticsearch_password = os.environ.get('ELASTICSEARCH_PASSWORD')
base_path = os.environ.get('BASE_PATH').strip()

fields = ["title", "pageContetnts", "organizations", "topics", "people", "workOfArt", "files", "locations", "dates", "researchInfrastructure"]
index = 'webcontents'
minimum_should_match = '100%'
aggregares = {
    "locations": {
        "terms": {
            "field": "locations.keyword",
            "size": 20,
            }
        },
    "people": {
        "terms": {
            "field": "people.keyword",
            "size": 20,
            }
        },
    "organizations": {
        "terms": {
            "field": "organizations.keyword",
            "size": 20,
            }
        },
    "products": {
        "terms": {
            "field": "products.keyword",
            "size": 20,
            }
        },
    "workOfArt": {
        "terms": {
            "field": "workOfArt.keyword",
            "size": 20,
            }
        },
    "ResearchInfrastructure": {
        "terms": {
            "field": "researchInfrastructure.acronym.keyword",
            "size": 20,
            }
        },
    "files": {
        "terms": {
            "field": "files.extension.keyword",
            "size": 20,
            }
        }
    }

def getSearchResults(request, facet, filter, searchtype, page, term):
    es = Elasticsearch(elasticsearch_url, http_auth=[elasticsearch_username, elasticsearch_password])

    if filter != "" and facet != "":
        saved_list = request.session['filters']
        saved_list.append({"term": {facet + ".keyword": filter}})
        request.session['filters'] = saved_list
    else:
        if 'filters' in request.session:
            del request.session['filters']
        request.session['filters'] = []

    page = (int(page) - 1) * 10
    result = {}
    if term == "*" or term == "top10":
        result = es.search(
            index=index,
            body={
                "from": page,
                "size": 10,
                "query": {
                    "bool": {
                        "must": {
                            "match_all": {}
                            },
                        "filter": {
                            "bool": {
                                "must": request.session.get('filters')
                                }
                            }
                        }
                    },
                "aggs": aggregares,
                }
            )
    else:
        user_request = "some_param"
        query_body = {
            "from": page,
            "size": 10,
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": term,
                            "fields": fields,
                            "type": "best_fields",
                            "minimum_should_match": minimum_should_match,
                            }
                        },
                    "filter": {
                        "bool": {
                            "must": request.session.get('filters')
                            }
                        }
                    }
                },
            "aggs": aggregares,
            }
        result = es.search(index=index, body=query_body)

    lstResults = []
    lstImageFilename = []
    lstImageURL = []

    for searchResult in result['hits']['hits']:
        lstResults.append(searchResult['_source'])

        if (searchtype == "imagesearch"):
            url = searchResult['_source']['url']
            ResearchInfrastructure = searchResult['_source']['researchInfrastructure']
            for img in searchResult['_source']['images']:
                a = urlparse(img)
                filename = os.path.basename(a.path)
                extension = os.path.splitext(filename)[1]
                filenameWithoutExt = os.path.splitext(filename)[0]
                if filename not in lstImageFilename:
                    lstImageFilename.append(filename)
                    image = {'imageURL': img, 'imageWebpage': url[0], 'filename': filenameWithoutExt,
                             'extension': extension, 'ResearchInfrastructure': ResearchInfrastructure[0]}
                    lstImageURL.append(image)

    facets = {k: [] for k in aggregares.keys()}
    for bucket_names in facets.keys():
        for searchResult in result['aggregations'][bucket_name]:

        if (searchResult['key'] != "None" and searchResult['key'] != "unknown" and searchResult['key'] != "Unknown"
                searchResult['key'] != "Data" and searchResult['key'] != "Unspecified" and searchResult['key'] != ""):
            val = {
                'key': searchResult['key'],
                'doc_count': searchResult['doc_count']
                }
            facets[bucket_name].append(val)

    numHits = result['hits']['total']['value']

    upperBoundPage = round(np.ceil(numHits / 10) + 1)
    if (upperBoundPage > 10):
        upperBoundPage = 11

    results = {
        "facets": facets,
        "results": lstResults,
        "NumberOfHits": numHits,
        "page_range": range(1, upperBoundPage),
        "cur_page": (page / 10 + 1),
        "searchTerm": term,
        "functionList": getAllfunctionList(request),
        "lstImageURL": lstImageURL
        }

    return results
