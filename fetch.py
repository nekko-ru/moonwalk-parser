#!/usr/bin/env python3
import requests
from loguru import logger as log

from src.models.AnimeModel import AnimeModel, AnimeTranslatorModel, EpisodeModel, AnimeGenres, Genres, db
from src.moonwalk.api import MoonwalkAPI
from src.transform import CreateNew


@db.atomic()
def main():
    log.info('Получение списка всех сериалов')
    raw = MoonwalkAPI().get_serials()

    data = CreateNew(raw)
    log.debug(f'После преобразования {len(data.storage)}')

    log.debug(f'Создание сериалов на сервере')
    for idx, serial in enumerate(data.storage.values()):
        output = serial.to_dict()

        anime = AnimeModel.create(**output, aid=idx)

        for genre in serial.genres:
            try:
                gr = Genres.select().where(Genres.name.contains(genre)).get()
            except Genres.DoesNotExist:
                continue
            AnimeGenres.create(anime_id=anime.aid, genre_id=gr.id)

        log.debug(f' * создано {anime.title}')

        for tr in serial.translators:
            translator = tr.to_dict()
            a_tr = AnimeTranslatorModel.create(anime_id=anime.aid, translator_id=tr.id, name=tr.name)

            for e_idx, episode in enumerate(tr.episodes):
                EpisodeModel.create(name=e_idx, stream_url=episode, atid=a_tr.id)

            log.debug(f'  + перевод добавлен от {tr.name} кол-во серий {len(tr.episodes)}')


if __name__ == '__main__':
    main()
