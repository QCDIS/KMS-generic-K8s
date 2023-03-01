import os

from django.test import TestCase
from django.test import Client


class ResponseTest(TestCase):

    def setUp(self):
        self.client = Client()

        BASE_PATH = os.environ.get('BASE_PATH').strip()
        self.urls = [
            (f'/{BASE_PATH}/dataset_elastic/home', 200),
            (f'/{BASE_PATH}/dataset_elastic/result', 200),
            (f'/{BASE_PATH}/dataset_elastic/search', 200),
            (f'/{BASE_PATH}/dataset_elastic/genericsearch?term=*&page=1', 200),
            (f'/{BASE_PATH}/dataset_elastic/rest', 200),
            (f'/{BASE_PATH}/dataset_elastic/aggregates', 200),
            ]

    def test_urls(self):
        for url, status_code in self.urls:
            with self.subTest(msg=f'{url} -> {status_code}'):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status_code)
