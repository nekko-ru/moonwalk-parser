import os
from datetime import datetime
from typing import List, Dict, Any

from loguru import logger as log
from playhouse.shortcuts import model_to_dict

from src.models.AnimeModel import AnimeModel, AnimeTranslatorModel, EpisodeModel, Genres, AnimeGenres
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
            # if need https
            serial.iframe_url = serial.iframe_url.replace('http://moonwalk.cc', 'https://streamguard.cc')
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
    updated: List[Anime] = []

    def __init__(self, raw: List[Serials]):
        for serial in raw:
            try:
                data = self.get_by_title(serial.title_ru)
                log.debug(f'Нашли id={data.aid} для {data.title}')

                tr, _ = AnimeTranslatorModel.get_or_create(
                    name=serial.translator,
                    anime_id=data.aid
                )

                deleted = EpisodeModel.delete().where(EpisodeModel.atid == tr.id).execute()
                for e_idx, episode in enumerate(_get_episodes(serial)):
                    # fix errors if pg not ++ id
                    EpisodeModel.create(id=EpisodeModel.select().order_by(EpisodeModel.id.desc()).get().id + 1, name=e_idx, stream_url=episode, atid=tr.id)

                data.save()
                self.updated.append(
                    data
                )
            except Exception as e:
                log.exception(e)

            except AnimeNotExist:
                log.info('Аниме не было найдено, нужно создать его')
                prepared = Anime(
                    id=None,
                    title=serial.title_ru,
                    title_en=serial.title_en,
                    title_or='-',
                    annotation=serial.material_data.description,
                    description=serial.material_data.description,
                    posters=[serial.material_data.poster or 'https://via.placeholder.com/450'],
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
                    rating=serial.material_data.kinopoisk_rating,
                    votes=serial.material_data.kinopoisk_votes,
                    # заполняем перевод
                    translators=[Translator(
                        id=serial.translator_id,
                        name=serial.translator,
                        episodes=_get_episodes(serial)
                    )]
                )

                output = prepared.to_dict()
                # fixme: rewrite
                del output['id']
                anime = AnimeModel.create(**output, aid=AnimeModel.select().count() + 1, hide=True)

                for genre in prepared.genres:
                    try:
                        gr = Genres.select().where(Genres.name.contains(genre)).get()
                    except Genres.DoesNotExist:
                        continue
                    AnimeGenres.create(anime_id=anime.aid, genre_id=gr.id)

                log.debug(f' * обновление {anime.title}')

                for tr in prepared.translators:
                    a_tr = AnimeTranslatorModel.create(anime_id=anime.aid, translator_id=tr.id, name=tr.name)

                    for e_idx, episode in enumerate(tr.episodes):
                        EpisodeModel.create(id=EpisodeModel.select().order_by(EpisodeModel.id.desc()).get().id + 1, name=e_idx, stream_url=episode, atid=a_tr.id)

    def get_by_title(self, title: str) -> AnimeModel:
        """
        Получение аниме по его названию из API
        :param title: название
        :return:
        """
        out: AnimeModel = AnimeModel.get_or_none(title=title)
        if out is None:
            raise AnimeNotExist

        return out

    def update(self, anime_id: int, translators: List[Translator]) -> Anime:
        anime = AnimeModel.get_or_none(aid=anime_id)
        for tr in translators:
            translator = AnimeTranslatorModel.get_or_create(anime_id=anime_id, name=tr.name, translator_id=tr.id)

            EpisodeModel.delete().where(EpisodeModel.atid == translator.id).execute()
            for e_idx, episode in enumerate(tr.episodes):
                EpisodeModel.create(name=e_idx, stream_url=episode, atid=translator.id)

        return anime


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
                    annotation=serial.material_data.description,
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
                    rating=serial.material_data.kinopoisk_rating,
                    votes=serial.material_data.kinopoisk_votes,
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
