from typing import List

import os
import requests
from loguru import logger as log
from dataclasses import dataclass

from src.moonwalk.types.base import Serials, Movies


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
        log.debug('выполнение запроса на получение списка сериалов')
        # выполняем http запрос к видео балансеру для получения всех сериалов
        # и сразу же преобразуем в json
        r = requests.get(f'{self.base_url}/serials_anime.json', params={
            'api_token': self.api_token
        })
        log.debug(f'статус ответа {r.status_code}')

        res = r.json()

        # каждый обьект из json поля 'serials' преобразует в класс для более удобной работы
        # и создаем список из сериалов
        return [Serials.from_dict(i) for i in res['report']['serials']]

    def get_movies(self):
        log.debug('выполнение запроса на получение списка фильмов')
        # выполняем http запрос к видео балансеру для получения всех сериалов
        # и сразу же преобразуем в json
        r = requests.get(f'{self.base_url}/movies_anime.json', params={
            'api_token': self.api_token
        })
        log.debug(f'статус ответа {r.status_code}')

        res = r.json()

        # каждый обьект из json поля 'serials' преобразует в класс для более удобной работы
        # и создаем список из сериалов
        return [Movies.from_dict(i) for i in res['report']['movies']]

    def updates_serials(self):
        log.debug('выполнение запроса на получение списка обновлений сериалов')
        # выполняем http запрос к видео балансеру для получения всех сериалов
        # и сразу же преобразуем в json
        r = requests.get(f'{self.base_url}/serials_updates.json', params={
            'api_token': self.api_token,
            'category': 'Anime'
        })
        log.debug(f'статус ответа {r.status_code}')

        res = r.json()

        # каждый обьект из json поля 'serials' преобразует в класс для более удобной работы
        # и создаем список из сериалов
        # важно: тк это список обновлений и для того что бы сохранить порядок в бд мы добавляем с конца
        return [Serials.from_dict(i['serial']) for i in res['updates'][::-1]]

    def updates_movies(self):
        log.debug('выполнение запроса на получение списка обновлений для фильмов')
        # выполняем http запрос к видео балансеру для получения всех сериалов
        # и сразу же преобразуем в json
        r = requests.get(f'{self.base_url}/movies_updates.json', params={
            'api_token': self.api_token,
            'category': 'Anime'
        })
        log.debug(f'статус ответа {r.status_code}')

        res = r.json()

        # каждый обьект из json поля 'serials' преобразует в класс для более удобной работы
        # и создаем список из сериалов
        # важно: тк это список обновлений и для того что бы сохранить порядок в бд мы добавляем с конца
        return [Serials.from_dict(i) for i in res['updates'][::-1]]


if __name__ == '__main__':
    client = MoonwalkAPI()
    s = client.get_serials()
    print(len(s))
