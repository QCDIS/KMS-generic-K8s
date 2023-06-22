import os

import numpy as np
from elasticsearch import Elasticsearch

elasticsearch_url = os.environ['ELASTICSEARCH_URL']
elasticsearch_username = os.environ.get('ELASTICSEARCH_USERNAME')
elasticsearch_password = os.environ.get('ELASTICSEARCH_PASSWORD')
base_path = os.environ.get('BASE_PATH').strip()

fields = ["description", "keywords", "contact", "publisher", "citation", "genre", "creator", "headline", "abstract", "theme", "producer", "author", "sponsor", "provider", "title", "instrument", "maintainer", "editor", "copyrightHolder", "contributor", "contentLocation", "about", "rights", "useConstraints", "status", "scope", "metadataProfile", "metadataIdentifier", "distributionInfo", "dataQualityInfo", "contentInfo", "repo", "essential_variables", "potential_topics"]
index = 'dataset'
minimum_should_match = '50%'
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

def getSearchResults(request, facet, filter, page, term):
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
    LocationspatialCoverage = []
    spatialCounter = 0

    for searchResult in result['hits']['hits']:
        lstResults.append(searchResult['_source'])

        for potentialocation in searchResult['_source']['spatial_coverage']:
            location = re.sub(r'[^A-Za-z0-9 ]+', '', potentialocation)
            if (location != "") and (location != "None") and (len(location) < 20) and (
                    location not in LocationspatialCoverage) and (spatialCounter < 10):
                spatialCounter = spatialCounter + 1
                geoLocation = {"location": location, "RI": searchResult['_source']['repo'][0]}
                LocationspatialCoverage.append(geoLocation)

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
        "spatial_coverage": LocationspatialCoverage,
        }

    return results
