import os

from peewee import *
from datetime import datetime
from playhouse.db_url import connect
from playhouse.postgres_ext import ArrayField, PostgresqlExtDatabase

database_url = os.getenv('DATABASE_URL', False)
if database_url:
    db = connect(database_url)
else:
    db = PostgresqlExtDatabase('website_development', host='127.0.0.1', user='postgres', password='postgres')


class BaseDbModel(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    def save(self, **kwargs):
        self.updated_at = datetime.utcnow()

        super().save(**kwargs)


class AnimeModel(BaseDbModel):
    aid = IntegerField(primary_key=True, column_name='id')
    title = CharField()
    title_en = CharField()
    title_or = CharField()
    annotation = CharField()
    description = TextField()
    status = CharField()
    year = IntegerField()
    rating = DecimalField()
    blocked_ru = BooleanField(default=False)
    blocked_ua = BooleanField(default=False)
    world_art_id = CharField()
    kinopoisk_id = CharField()
    countries = ArrayField(CharField)
    actors = ArrayField(CharField)
    directors = ArrayField(CharField)
    studios = ArrayField(CharField)
    youtube_trailer_url = CharField()
    slug = CharField()

    class Meta:
        database = db
        table_name = 'animes'


class AnimeGenres(Model):
    genre_id = IntegerField(column_name='genre_id')
    anime_id = IntegerField(column_name='anime_id')

    class Meta:
        database = db
        primary_key = False
        table_name = 'animes_genres'


class Genres(BaseDbModel):
    id = IntegerField(primary_key=True, column_name='id')
    name = CharField()

    class Meta:
        database = db
        table_name = 'genres'


class AnimeTranslatorModel(BaseDbModel):
    id = IntegerField(primary_key=True, column_name='id')
    name = CharField()
    anime_id = IntegerField(column_name='anime_id')

    class Meta:
        database = db
        table_name = 'anime_translators'


class EpisodeModel(BaseDbModel):
    id = IntegerField(primary_key=True, column_name='id')
    name = CharField()
    stream_url = CharField()
    atid = IntegerField(column_name='anime_translator_id')

    class Meta:
        database = db
        table_name = 'episodes'
