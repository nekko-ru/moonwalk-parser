from typing import List, Dict

from loguru import logger as log
from src.moonwalk.types.base import Serials, Movies
from src.nekkoch.types.base import Anime, Translator


def _get_episodes(serial: Serials or Movies, no_control: bool = True) -> List[str]:
    """
    Создает список ссылок на iframe с указанием серии и сезона, а так же отключеным управление (опционально)
    :param serial:
    :return:
    """
    log.debug(f'Получение ссылок для {serial.title_ru}')
    urls = []

    if getattr(serial, 'season_episodes_count', None) is None:
        if no_control:
            urls.append(serial.iframe_url + f'?nocontrols_translations=1&nocontrols=1')
        else:
            urls.append(serial.iframe_url)
    else:
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


class CreateNew:
    # словарь для группировки и более быстрой работы
    # ключ - kinopoisk_id или world_art_id если нету первого
    storage: Dict[int, Anime] = {}

    # список аниме которые не были импортированы из за отсутствия каких либо важных данных
    with_error: List[Serials] = []

    def __init__(self, raw: List[Serials or Movies]):
        self.storage = {}
        self.with_error = []

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
        key = serial.title_en

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
                    poster=serial.material_data.poster,
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
            if [i for i in self.storage[key].translators if i.name == serial.translator]:
                return

            self.storage[key].translators.append(Translator(
                id=serial.translator_id,
                name=serial.translator,
                episodes=_get_episodes(serial)
            ))
