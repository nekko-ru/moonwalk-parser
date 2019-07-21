from typing import List

import os
import requests
from dataclasses import dataclass

from src.moonwalk.types.base import Serials


@dataclass
class MoonwalkAPI:
    """
    Класс для работы с апи moonwalk
    Пример:
        # если не установлен в окружении MOONWALK_API_TOKEN нужно указать api_token
        client = MoonwalkAPI(api_token='sometoken')

        # получить список всех аниме сериалов
        _ = client.get_serials()

        # todo: another examples
    """

    # api токен, можно задать по умолчанию через переменную окружения MOONWALK_API_TOKEN
    # например так: MOONWALK_API_TOKEN=123c1ax2j345hkj3 main.py
    api_token: str = os.getenv('MOONWALK_API_TOKEN', '')
    # ссылка на видеобалансер
    base_url: str = 'http://moonwalk.cc/api'

    def get_serials(self) -> List[Serials]:
        # выполняем http запрос к видео балансеру для получения всех сериалов
        # и сразу же преобразуем в json
        r = requests.get(f'{self.base_url}/serials_anime.json', params={
            'api_token': self.api_token
        }).json()

        # каждый обьект из json поля 'serials' преобразует в класс для более удобной работы
        # и создаем список из сериалов
        return list(map(Serials.from_dict, r['report']['serials']))

    def get_movies(self):
        pass

    def updates_serials(self):
        pass

    def updates_movies(self):
        pass


if __name__ == '__main__':
    client = MoonwalkAPI()
    s = client.get_serials()
    print(len(s))
