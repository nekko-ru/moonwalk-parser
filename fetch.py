#!/usr/bin/env python3
import requests
from loguru import logger as log

from src.models.AnimeModel import AnimeModel, AnimeTranslatorModel, EpisodeModel, AnimeGenres, Genres, db, Media
from src.moonwalk.api import MoonwalkAPI
from src.transform import CreateNew


@db.atomic()
def main():
    log.info('Получение списка всех сериалов')
    raw = MoonwalkAPI().get_serials()

    data = CreateNew(raw)
    log.debug(f'После преобразования {len(data.storage)}')

    log.debug(f'Создание сериалов на сервере')
    new_id_offset = int(AnimeModel.select(AnimeModel.aid).order_by(AnimeModel.aid.desc()).get().aid + 1)
    for idx, serial in enumerate(data.storage.values()):
        if AnimeModel.select().where(AnimeModel.title == serial.title).count() > 0:
            log.debug(f' - skip {serial.title}')
            continue

        media = Media.create(
            id=Media.select().order_by(Media.id.desc()).get().id + 1,
            nsfw=False,
            media_type=0,
            rating=5,
        )
        anime = AnimeModel.create(**serial.to_dict(),
                                  aid=new_id_offset + idx, media_id=media)

        for genre in serial.genres:
            try:
                gr = Genres.select().where(Genres.name.contains(genre)).get()
            except Genres.DoesNotExist:
                continue
            AnimeGenres.create(anime_id=anime.aid, genre_id=gr.id)

        log.debug(f' * создано {anime.title}')

        for tr in serial.translators:
            translator = tr.to_dict()
            a_tr = AnimeTranslatorModel.create(
                id = AnimeTranslatorModel.select().order_by(AnimeTranslatorModel.id.desc()).get().id + 1,
                anime_id=anime.aid, translator_id=tr.id, name=tr.name
            )

            for e_idx, episode in enumerate(tr.episodes):
                EpisodeModel.create(
                    id=EpisodeModel.select().order_by(EpisodeModel.id.desc()).get().id + 1,
                    name=e_idx, stream_url=episode, atid=a_tr.id
                )

            log.debug(f'  + перевод добавлен от {tr.name} кол-во серий {len(tr.episodes)}')

    log.info('Получение списка всех фильмов')
    raw = MoonwalkAPI().get_movies()

    data = CreateNew(raw)
    log.debug(f'После преобразования {len(data.storage)}')

    log.debug(f'Создание фильмов на сервере')

    new_id_offset = int(AnimeModel.select(AnimeModel.aid).order_by(AnimeModel.aid.desc()).get().aid + 1)
    for idx, movie in enumerate(data.storage.values()):
        output = movie.to_dict()

        if AnimeModel.select().where(AnimeModel.title == movie.title).count() > 0:
            log.debug(f' - skip {movie.title}')
            continue

        media = Media.create(
            id=Media.select().order_by(Media.id.desc()).get().id + 1,
            nsfw=False,
            media_type=0,
            rating=5,
        )
        anime = AnimeModel.create(**output,
                                  aid=new_id_offset + idx, media_id=media)

        for genre in movie.genres:
            try:
                gr = Genres.select().where(Genres.name.contains(genre)).get()
            except Genres.DoesNotExist:
                continue
            AnimeGenres.create(anime_id=anime.aid, genre_id=gr.id)

        log.debug(f' * создано {anime.title}')

        tr_id_offset = int(AnimeTranslatorModel.select(AnimeTranslatorModel.id).order_by(AnimeTranslatorModel.id.desc()).get().id + 1)
        for tr_idx, tr in enumerate(movie.translators):
            a_tr = AnimeTranslatorModel.create(
                id=tr_id_offset + tr_idx,
                anime_id=anime.aid, translator_id=tr.id, name=tr.name
            )

            for e_idx, episode in enumerate(tr.episodes):
                EpisodeModel.create(
                    id=EpisodeModel.select().order_by(EpisodeModel.id.desc()).get().id + 1,
                    name=e_idx, stream_url=episode, atid=a_tr.id
                )

            log.debug(f'  + перевод добавлен от {tr.name} кол-во серий {len(tr.episodes)}')


if __name__ == '__main__':
    main()
