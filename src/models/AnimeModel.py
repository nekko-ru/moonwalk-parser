from peewee import *
from datetime import datetime
from playhouse.postgres_ext import ArrayField, PostgresqlExtDatabase


db = PostgresqlExtDatabase('website_development', host='127.0.0.1', user='postgres', password='postgres')


class AnimeModel(Model):
    aid = IntegerField(primary_key=True, column_name='id')
    title = CharField()
    title_en = CharField()
    title_or = CharField()
    annotation = CharField()
    description = TextField()
    posters = ArrayField(CharField)
    genres = ArrayField(CharField)
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
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'animes'


class AnimeTranslatorModel(Model):
    id = IntegerField(primary_key=True, column_name='id')
    name = CharField()
    anime_id = IntegerField(column_name='anime_id')
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'anime_translators'


class EpisodeModel(Model):
    id = IntegerField(primary_key=True, column_name='id')
    name = CharField()
    stream_url = CharField()
    atid = IntegerField(column_name='anime_translator_id')
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        table_name = 'episodes'
