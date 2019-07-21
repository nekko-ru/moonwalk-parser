import json
from unittest import TestCase

from src.moonwalk.types.base import serials_from_dict, serials_to_dict


class TestSerials(TestCase):
    def test_from_dict(self):
        with open('./mock-data/serials_anime.json') as f:
            data = json.load(f)

        for case in data['report']['serials'][:10]:
            with self.subTest(msg=f"Testing with '{case['title_ru']}'"):
                movie = serials_from_dict(case)
                self.assertEqual(movie.title_ru, case['title_ru'])

                # testing block info
                self.assertEqual(movie.block.blocked_at, case['block']['blocked_at'])
                self.assertEqual(movie.block.block_ru, case['block']['block_ru'])
                self.assertEqual(movie.block.block_ua, case['block']['block_ua'])

                # testing block info
                self.assertEqual(movie.material_data.poster, case['material_data']['poster'])
                self.assertEqual(movie.material_data.countries, case['material_data']['countries'])
                self.assertEqual(movie.material_data.actors, case['material_data']['actors'])

    def test_to_dict(self):
        with open('./mock-data/serials_anime.json') as f:
            data = json.load(f)

        for case in data['report']['serials'][:10]:
            with self.subTest(msg=f"Testing with '{case['title_ru']}'"):
                movie = serials_from_dict(case)
                raw = serials_to_dict(movie)

                self.assertDictEqual(raw, case)
