# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = movies_from_dict(json.loads(json_string))
#     result = serials_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_none(x: Any) -> Any:
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except Exception as e:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    return x or '-'


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Block:
    blocked_at: None
    block_ru: Optional[bool]
    block_ua: Optional[bool]

    @staticmethod
    def from_dict(obj: Any) -> 'Block':
        assert isinstance(obj, dict)
        blocked_at = from_none(obj.get("blocked_at"))
        block_ru = from_union([from_bool, from_none], obj.get("block_ru"))
        block_ua = from_union([from_bool, from_none], obj.get("block_ua"))
        return Block(blocked_at, block_ru, block_ua)

    def to_dict(self) -> dict:
        result: dict = {}
        result["blocked_at"] = from_none(self.blocked_at)
        result["block_ru"] = from_union([from_bool, from_none], self.block_ru)
        result["block_ua"] = from_union([from_bool, from_none], self.block_ua)
        return result


@dataclass
class Duration:
    seconds: Optional[int]
    human: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Duration':
        assert isinstance(obj, dict)
        seconds = from_union([from_int, from_none], obj.get("seconds"))
        human = from_union([from_str, from_none], obj.get("human"))
        return Duration(seconds, human)

    def to_dict(self) -> dict:
        result: dict = {}
        result["seconds"] = from_union([from_int, from_none], self.seconds)
        result["human"] = from_union([from_str, from_none], self.human)
        return result


@dataclass
class MaterialData:
    updated_at: Optional[datetime]
    poster: Optional[str]
    year: Optional[int]
    tagline: Optional[str]
    description: Optional[str]
    age: Optional[int]
    countries: Optional[List[str]]
    genres: Optional[List[str]]
    actors: Optional[List[str]]
    directors: Optional[List[str]]
    studios: Optional[List[str]]
    kinopoisk_rating: Optional[float]
    kinopoisk_votes: Optional[int]
    imdb_rating: Optional[float]
    imdb_votes: Optional[int]
    mpaa_rating: Optional[int]
    mpaa_votes: Optional[int]

    @staticmethod
    def from_dict(obj: Any) -> 'MaterialData':
        assert isinstance(obj, dict)
        updated_at = from_union([from_datetime, from_none], obj.get("updated_at"))
        poster = from_union([from_str, from_none], obj.get("poster", ''))
        year = from_union([from_int, from_none], obj.get("year"))
        tagline = from_union([from_str, from_none], obj.get("tagline", ''))
        description = from_union([from_str, from_none], obj.get("description", ''))
        age = from_union([from_int, from_none], obj.get("age"))
        countries = from_union([lambda x: from_list(from_str, x), from_none], obj.get("countries"))
        genres = from_union([lambda x: from_list(from_str, x), from_none], obj.get("genres"))
        actors = from_union([lambda x: from_list(from_str, x), from_none], obj.get("actors"))
        directors = from_union([lambda x: from_list(from_str, x), from_none], obj.get("directors"))
        studios = from_union([lambda x: from_list(from_str, x), from_none], obj.get("studios"))
        kinopoisk_rating = from_union([from_float, from_none], obj.get("kinopoisk_rating"))
        kinopoisk_votes = from_union([from_int, from_none], obj.get("kinopoisk_votes"))
        imdb_rating = from_union([from_float, from_none], obj.get("imdb_rating"))
        imdb_votes = from_union([from_int, from_none], obj.get("imdb_votes"))
        mpaa_rating = from_union([from_int, from_none], obj.get("mpaa_rating"))
        mpaa_votes = from_union([from_int, from_none], obj.get("mpaa_votes"))
        return MaterialData(updated_at, poster, year, tagline, description, age, countries, genres, actors, directors, studios, kinopoisk_rating, kinopoisk_votes, imdb_rating, imdb_votes, mpaa_rating, mpaa_votes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["updated_at"] = from_union([lambda x: x.strftime('%Y-%m-%d %H:%M:%S'), from_none], self.updated_at)
        result["poster"] = from_union([from_str, from_none], self.poster)
        result["year"] = from_union([from_int, from_none], self.year)
        result["tagline"] = from_union([from_str, from_none], self.tagline)
        result["description"] = from_union([from_str, from_none], self.description)
        result["age"] = from_union([from_int, from_none], self.age)
        result["countries"] = from_union([lambda x: from_list(from_str, x), from_none], self.countries)
        result["genres"] = from_union([lambda x: from_list(from_str, x), from_none], self.genres)
        result["actors"] = from_union([lambda x: from_list(from_str, x), from_none], self.actors)
        result["directors"] = from_union([lambda x: from_list(from_str, x), from_none], self.directors)
        result["studios"] = from_union([lambda x: from_list(from_str, x), from_none], self.studios)
        result["kinopoisk_rating"] = from_union([to_float, from_none], self.kinopoisk_rating)
        result["kinopoisk_votes"] = from_union([from_int, from_none], self.kinopoisk_votes)
        result["imdb_rating"] = from_union([to_float, from_none], self.imdb_rating)
        result["imdb_votes"] = from_union([from_int, from_none], self.imdb_votes)
        result["mpaa_rating"] = from_union([from_int, from_none], self.mpaa_rating)
        result["mpaa_votes"] = from_union([from_int, from_none], self.mpaa_votes)
        return result


@dataclass
class Movies:
    title_ru: Optional[str]
    title_en: Optional[str]
    year: Optional[int]
    duration: Optional[Duration]
    kinopoisk_id: Optional[int]
    world_art_id: Optional[int]
    pornolab_id: None
    token: Optional[str]
    type: Optional[str]
    camrip: Optional[bool]
    source_type: Optional[str]
    source_quality_type: None
    instream_ads: Optional[bool]
    directors_version: Optional[bool]
    iframe_url: Optional[str]
    trailer_token: Optional[str]
    trailer_iframe_url: Optional[str]
    translator: Optional[str]
    translator_id: Optional[int]
    added_at: Optional[datetime]
    category: Optional[str]
    block: Optional[Block]
    material_data: Optional[MaterialData]

    @staticmethod
    def from_dict(obj: Any) -> 'Movies':
        assert isinstance(obj, dict)
        title_ru = from_union([from_str, from_none], obj.get("title_ru"))
        title_en = from_union([from_str, from_none], obj.get("title_en"))
        year = from_union([from_int, from_none], obj.get("year"))
        duration = from_union([Duration.from_dict, from_none], obj.get("duration"))
        kinopoisk_id = from_union([from_int, from_none], obj.get("kinopoisk_id"))
        world_art_id = from_union([from_int, from_none], obj.get("world_art_id"))
        pornolab_id = from_none(obj.get("pornolab_id"))
        token = from_union([from_str, from_none], obj.get("token"))
        type = from_union([from_str, from_none], obj.get("type"))
        camrip = from_union([from_bool, from_none], obj.get("camrip"))
        source_type = from_union([from_none, from_str], obj.get("source_type"))
        source_quality_type = from_none(obj.get("source_quality_type"))
        instream_ads = from_union([from_bool, from_none], obj.get("instream_ads"))
        directors_version = from_union([from_bool, from_none], obj.get("directors_version"))
        iframe_url = from_union([from_str, from_none], obj.get("iframe_url"))
        trailer_token = from_union([from_none, from_str], obj.get("trailer_token"))
        trailer_iframe_url = from_union([from_none, from_str], obj.get("trailer_iframe_url"))
        translator = from_union([from_str, from_none], obj.get("translator"))
        translator_id = from_union([from_int, from_none], obj.get("translator_id"))
        added_at = from_union([from_datetime, from_none], obj.get("added_at"))
        category = from_union([from_str, from_none], obj.get("category"))
        block = from_union([Block.from_dict, from_none], obj.get("block"))
        material_data = from_union([MaterialData.from_dict, from_none], obj.get("material_data"))
        return Movies(title_ru, title_en, year, duration, kinopoisk_id, world_art_id, pornolab_id, token, type, camrip, source_type, source_quality_type, instream_ads, directors_version, iframe_url, trailer_token, trailer_iframe_url, translator, translator_id, added_at, category, block, material_data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title_ru"] = from_union([from_str, from_none], self.title_ru)
        result["title_en"] = from_union([from_str, from_none], self.title_en)
        result["year"] = from_union([from_int, from_none], self.year)
        result["duration"] = from_union([lambda x: to_class(Duration, x), from_none], self.duration)
        result["kinopoisk_id"] = from_union([from_int, from_none], self.kinopoisk_id)
        result["world_art_id"] = from_union([from_int, from_none], self.world_art_id)
        result["pornolab_id"] = from_none(self.pornolab_id)
        result["token"] = from_union([from_str, from_none], self.token)
        result["type"] = from_union([from_str, from_none], self.type)
        result["camrip"] = from_union([from_bool, from_none], self.camrip)
        result["source_type"] = from_union([from_none, from_str], self.source_type)
        result["source_quality_type"] = from_none(self.source_quality_type)
        result["instream_ads"] = from_union([from_bool, from_none], self.instream_ads)
        result["directors_version"] = from_union([from_bool, from_none], self.directors_version)
        result["iframe_url"] = from_union([from_str, from_none], self.iframe_url)
        result["trailer_token"] = from_union([from_none, from_str], self.trailer_token)
        result["trailer_iframe_url"] = from_union([from_none, from_str], self.trailer_iframe_url)
        result["translator"] = from_union([from_str, from_none], self.translator)
        result["translator_id"] = from_union([from_int, from_none], self.translator_id)
        result["added_at"] = from_union([lambda x: x.strftime('%Y-%m-%d %H:%M:%S'), from_none], self.added_at)
        result["category"] = from_union([from_str, from_none], self.category)
        result["block"] = from_union([lambda x: to_class(Block, x), from_none], self.block)
        result["material_data"] = from_union([lambda x: to_class(MaterialData, x), from_none], self.material_data)
        return result


@dataclass
class SeasonEpisodesCount:
    season_number: Optional[int]
    episodes_count: Optional[int]
    episodes: Optional[List[int]]

    @staticmethod
    def from_dict(obj: Any) -> 'SeasonEpisodesCount':
        assert isinstance(obj, dict)
        season_number = from_union([from_int, from_none], obj.get("season_number"))
        episodes_count = from_union([from_int, from_none], obj.get("episodes_count"))
        episodes = from_union([lambda x: from_list(from_int, x), from_none], obj.get("episodes"))
        return SeasonEpisodesCount(season_number, episodes_count, episodes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["season_number"] = from_union([from_int, from_none], self.season_number)
        result["episodes_count"] = from_union([from_int, from_none], self.episodes_count)
        result["episodes"] = from_union([lambda x: from_list(from_int, x), from_none], self.episodes)
        return result


@dataclass
class Serials:
    title_ru: Optional[str]
    title_en: Optional[str]
    year: Optional[int]
    token: Optional[str]
    type: Optional[str]
    kinopoisk_id: Optional[int]
    world_art_id: Optional[int]
    translator: Optional[str]
    translator_id: Optional[int]
    iframe_url: Optional[str]
    trailer_token: Optional[str]
    trailer_iframe_url: Optional[str]
    seasons_count: Optional[int]
    episodes_count: Optional[int]
    category: Optional[str]
    block: Optional[Block]
    season_episodes_count: Optional[List[SeasonEpisodesCount]]
    material_data: Optional[MaterialData]

    @staticmethod
    def from_dict(obj: Any) -> 'Serials':
        assert isinstance(obj, dict)
        title_ru = from_union([from_str, from_none], obj.get("title_ru"))
        title_en = from_union([from_str, from_none], obj.get("title_en"))
        year = from_union([from_int, from_none], obj.get("year"))
        token = from_union([from_str, from_none], obj.get("token"))
        type = from_union([from_str, from_none], obj.get("type"))
        kinopoisk_id = from_union([from_int, from_none], obj.get("kinopoisk_id"))
        world_art_id = from_union([from_int, from_none], obj.get("world_art_id"))
        translator = from_union([from_str, from_none], obj.get("translator"))
        translator_id = from_union([from_int, from_none], obj.get("translator_id"))
        iframe_url = from_union([from_str, from_none], obj.get("iframe_url"))
        trailer_token = from_union([from_str, from_none], obj.get("trailer_token"))
        trailer_iframe_url = from_union([from_str, from_none], obj.get("trailer_iframe_url"))
        seasons_count = from_union([from_int, from_none], obj.get("seasons_count"))
        episodes_count = from_union([from_int, from_none], obj.get("episodes_count"))
        category = from_union([from_str, from_none], obj.get("category"))
        block = from_union([Block.from_dict, from_none], obj.get("block"))
        season_episodes_count = from_union([lambda x: from_list(SeasonEpisodesCount.from_dict, x), from_none], obj.get("season_episodes_count"))
        material_data = from_union([MaterialData.from_dict, from_none], obj.get("material_data"))
        return Serials(title_ru, title_en, year, token, type, kinopoisk_id, world_art_id, translator, translator_id, iframe_url, trailer_token, trailer_iframe_url, seasons_count, episodes_count, category, block, season_episodes_count, material_data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title_ru"] = from_union([from_str, from_none], self.title_ru)
        result["title_en"] = from_union([from_str, from_none], self.title_en)
        result["year"] = from_union([from_int, from_none], self.year)
        result["token"] = from_union([from_str, from_none], self.token)
        result["type"] = from_union([from_str, from_none], self.type)
        result["kinopoisk_id"] = from_union([from_int, from_none], self.kinopoisk_id)
        result["world_art_id"] = from_union([from_int, from_none], self.world_art_id)
        result["translator"] = from_union([from_str, from_none], self.translator)
        result["translator_id"] = from_union([from_int, from_none], self.translator_id)
        result["iframe_url"] = from_union([from_str, from_none], self.iframe_url)
        result["trailer_token"] = from_union([from_str, from_none], self.trailer_token)
        result["trailer_iframe_url"] = from_union([from_str, from_none], self.trailer_iframe_url)
        result["seasons_count"] = from_union([from_int, from_none], self.seasons_count)
        result["episodes_count"] = from_union([from_int, from_none], self.episodes_count)
        result["category"] = from_union([from_str, from_none], self.category)
        result["block"] = from_union([lambda x: to_class(Block, x), from_none], self.block)
        result["season_episodes_count"] = from_union([lambda x: from_list(lambda x: to_class(SeasonEpisodesCount, x), x), from_none], self.season_episodes_count)
        result["material_data"] = from_union([lambda x: to_class(MaterialData, x), from_none], self.material_data)
        return result


def movies_from_dict(s: Any) -> Movies:
    return Movies.from_dict(s)


def movies_to_dict(x: Movies) -> Any:
    return to_class(Movies, x)


def serials_from_dict(s: Any) -> Serials:
    return Serials.from_dict(s)


def serials_to_dict(x: Serials) -> Any:
    return to_class(Serials, x)
