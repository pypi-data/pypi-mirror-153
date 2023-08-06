import json

import django.test
from django.conf import settings


class TestCase(django.test.TestCase):
    test_data_base_dir = settings.BASE_DIR

    def json_data(self, *path):
        path = self.test_data_base_dir.joinpath(*path)
        with path.open() as fp:
            return json.load(fp)

    def raw_data(self, *path):
        path = self.test_data_base_dir.joinpath(*path)
        with path.open() as fp:
            return fp.read()
