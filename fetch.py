#!/usr/bin/env python3
import requests
from loguru import logger as log

from src.models.Anime import Anime, AnimeTranslator, Episode
from src.moonwalk.api import MoonwalkAPI
from src.transform import CreateNew


log.info('Получение списка всех сериалов')
raw = MoonwalkAPI().get_serials()

data = CreateNew(raw)
log.debug(f'После преобразования {len(data.storage)}')

log.debug(f'Создание сериалов на сервере')
for idx, serial in enumerate(data.storage.values()):
    output = serial.to_dict()

    anime = Anime.create(**output)

    log.debug(f' * создано {anime.title}')

    for tr in serial.translators:
        translator = tr.to_dict()
        a_tr = AnimeTranslator.create(anime_id=anime.aid, translator_id=tr.id, name=tr.name)

        for e_idx, episode in enumerate(tr.episodes):
            Episode.create(name=e_idx, stream_url=episode, atid=a_tr.id)

        log.debug(f'  + перевод добавлен от {tr.name} кол-во серий {len(tr.episodes)}')
