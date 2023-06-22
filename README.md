[![Build and push container](https://github.com/QCDIS/KMS-generic/actions/workflows/make-relese.yml/badge.svg)](https://github.com/QCDIS/KMS-generic/actions/workflows/make-relese.yml)

# envri-kbs

```
python3 -m spacy download en_core_web_md
```

```
manage.py migrate
manage.py  makemigrations
manage.py  runserver 0.0.0.0:8000
```

## Environment variables

- ACCESS_TOKEN_Github=<A_GITHUB_TOKEN>
- ACCESS_TOKEN_Gitlab=<A_GITLAB_TOKEN>
- ELASTICSEARCH_PASSWORD=<ES_PASSWORD>
- ELASTICSEARCH_URL=https://HOST:PORT/BASE_PATH/
- ELASTICSEARCH_USERNAME=<ES_USERNAME>
- GITHUB_QUERY_URL=https://api.github.com/search/code?l=Jupyter+Notebook&q=ipynb+in:path+extension:ipynb
- KMS_ADMIN_USERNAME=<ADMIN_USERNAME>
- KMS_ADMIN_PASSWORD=<ADMIN_PASSWORD>
- BASE_PATH=search
- DEBUG=False
- SECRET_KEY=<DJANGO_SECRET_KEY>
- ALLOWED_HOST=HOST
- CSRF_TRUSTED_ORIGINS=https://HOST:PORT


## Testing

### Test elasticsearch server

```bash
docker run --rm \
  -e "discovery.type=single-node" \
  -e "ELASTIC_PASSWORD=changeme" \
  -e "xpack.security.http.ssl.enabled=false" \
  --name es01 \
  -p 9200:9200 \
  docker.elastic.co/elasticsearch/elasticsearch:8.8.1
```

Load test data:

```bash
python fixtures/load_fixtures.py
```

### UI

Frontend tests are run with [Cypress](https://www.cypress.io/).
To get started:

```bash
npm install cypress --save-dev
npx cypress open
```

With Pycharm, tests can be run with the plugin
[Cypress Support](https://plugins.jetbrains.com/plugin/13819-cypress-support).

### API

API tests are generated and run with [Portman](http://getportman.com).
To get started:

```bash
npm install --save-dev @apideck/portman
npx portman --cliOptionsFile portman/portman-cli.yaml
```


## License

Copyright 2023 University of Amsterdam / LifeWatch ERIC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
