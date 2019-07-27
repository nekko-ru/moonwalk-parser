import json
from unittest import TestCase
from src.nekkoch.types.base import anime_from_dict, anime_to_dict


class TestAnime(TestCase):
    def test_from_dict(self):
        with open('./mock-data/nekko-ch.json') as f:
            data = json.load(f)

        anim = anime_from_dict(data)
        self.assertEqual(anim.title, data['title'])
        self.assertEqual(anim.title_en, data['title_en'])
        self.assertEqual(anim.title_or, data['title_or'])
        self.assertEqual(anim.posters, data['posters'])
        self.assertEqual(len(anim.translators), len(data['translators']))
        self.assertEqual(anim.translators[0].episodes, data['translators'][0]['episodes'])

    # def test_to_dict(self):
    #     with open('./mock-data/nekko-ch.json') as f:
    #         data = json.load(f)
    #
    #     anim = anime_from_dict(data)
    #     row = anime_to_dict(anim)
    #     self.assertDictEqual(row, data)
