import os
from typing import List, Dict, Any

import requests
from loguru import logger as log

from src.moonwalk.types.base import Serials
from src.nekkoch.types.base import Anime, Translator


def _get_episodes(serial: Serials, no_control: bool = True) -> List[str]:
    """
    Создает список ссылок на iframe с указанием серии и сезона, а так же отключеным управление (опционально)
    :param serial:
    :return:
    """
    log.debug(f'Получение ссылок для {serial.title_ru}')

    urls = []
    for season in serial.season_episodes_count:
        log.debug(f' - сезон {season.season_number}, кол-во серий {season.episodes_count}')
        for episode in season.episodes:
            if no_control:
                urls.append(serial.iframe_url + f'?episode={episode}&season={season.season_number}'
                f'&nocontrols_translations=1&nocontrols=1')
            else:
                urls.append(serial.iframe_url + f'?episode={episode}&season={season.season_number}'
                f'&nocontrols_translations=1')

    return urls


class AnimeNotExist(BaseException):
    pass


class Update:
    """
    Класс для обновления серий, проверяет есть ли на сервере это аниме и если есть то добавляет новую серию
    """
    url: str = "http://localhost:8084"
    updated: List[Anime] = []
    access_token: str = os.getenv('NEKKOCH_ACCESS_TOKEN', '')

    def __init__(self, raw: List[Serials]):
        for serial in raw:
            try:
                data = self.get_by_title(serial.title_ru)
                anime = Anime.from_dict(data)
                log.debug(f'Нашли id={anime.id} для {serial.title_ru}')

                def search(d):
                    for i, tr in enumerate(d):
                        if tr.name == serial.translator or tr.id == serial.translator_id:
                            return i
                    return -1

                idx = search(anime.translators)
                if idx == -1:
                    anime.translators.append(Translator(
                        id=serial.translator_id,
                        name=serial.translator,
                        episodes=_get_episodes(serial)
                    ))
                else:
                    anime.translators[idx].episodes = _get_episodes(serial)

                # for i, tr in enumerate(anime.translators):
                #     if tr.name == serial.translator or tr.id == serial.translator_id:
                #         anime.translators[i].episodes = _get_episodes(serial)
                #     else:
                #         anime.translators.append(Translator(
                #             id=serial.translator_id,
                #             name=serial.translator,
                #             episodes=_get_episodes(serial)
                #         ))
                self.updated.append(
                    self.update(anime.id, anime.translators)
                )
            except Exception as e:
                log.exception(e)

            except AnimeNotExist:
                log.info('Аниме не было найдено, нужно создать его')

                for serial in CreateNew([serial]).storage.values():

                    querystring = {"access_token": self.access_token}

                    # отправка запроса
                    # WARNING: замените на свой способ отправки новой серии
                    res = requests.post(f'{self.url}/anime.create', json=serial.to_dict(), params=querystring)
                    if res.ok:
                        log.debug(f' * создано {serial.title}')
                    else:
                        raise Exception(res.json()['data'])

    def get_by_title(self, title: str) -> Dict[str, Any]:
        """
        Получение аниме по его названию из API
        :param title: название
        :return:
        """

        res = requests.get(f'{self.url}/anime.search', params={
            'q': title,
            'access_token': self.access_token
        })

        out = res.json()['animes']
        if out is None:
            raise AnimeNotExist

        res = requests.get(f'{self.url}/anime.get', params={
            'anime_id': out[0]['id'],
            'access_token': self.access_token
        })
        return res.json()['anime']

    def update(self, anime_id: int, translators: List[Translator]) -> Anime:
        res = requests.post(f'{self.url}/anime.update', params={
            'anime_id': anime_id,
            'access_token': self.access_token
        }, json={
            'translators': [tr.to_dict() for tr in translators]
        })
        return Anime.from_dict(res.json()['anime'])


class CreateNew:
    # словарь для группировки и более быстрой работы
    # ключ - kinopoisk_id или world_art_id если нету первого
    storage: Dict[int, Anime] = {}

    # список аниме которые не были импортированы из за отсутствия каких либо важных данных
    with_error: List[Serials] = []

    def __init__(self, raw: List[Serials]):
        for serial in raw:
            self._create_or_append(serial)

        # повторяем еще раз для аниме с ошибками
        # тк в %90 это переводы без material_data и их нужно аттачить
        for serial in self.with_error:
            self._create_or_append(serial, True)

    def _create_or_append(self, serial: Serials, with_error: bool = False):
        """
        Добавляет в хранилище если сериала нету иначе добавляет как перевод
        :param serial:
        :return:
        """
        key = serial.title_ru

        anime = self.storage.get(key, None)
        if anime is None:
            try:
                # на случай если мы руками заполнили material_data (своеобразный fallback для сералов без material_data)
                if serial.material_data.poster == 'https://via.placeholder.com/450' and with_error == False:
                    self.with_error.append(serial)
                    return
                self.storage[key] = Anime(
                    id=None,
                    title=serial.title_ru,
                    title_en=serial.title_en,
                    title_or='-',
                    annotation='-',
                    description=serial.material_data.description,
                    posters=[serial.material_data.poster],
                    type=serial.type,
                    genres=serial.material_data.genres or [],
                    status='Закончено',
                    year=serial.material_data.year,
                    world_art_id=serial.world_art_id,
                    kinopoisk_id=serial.kinopoisk_id,
                    countries=serial.material_data.countries or [],
                    actors=serial.material_data.actors or [],
                    directors=serial.material_data.directors or [],
                    studios=serial.material_data.studios or [],
                    # заполняем перевод
                    translators=[Translator(
                        id=serial.translator_id,
                        name=serial.translator,
                        episodes=_get_episodes(serial)
                    )]
                )
            except AttributeError as e:
                log.error(e)
                # на случай если есть сломаные (не только без material_data)
                pass
        else:
            self.storage[key].translators.append(Translator(
                id=serial.translator_id,
                name=serial.translator,
                episodes=_get_episodes(serial)
            ))
