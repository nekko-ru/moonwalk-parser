#     result = movies_from_dict(json.loads(json_string))
#     result = serials_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


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
    block_ru: bool
    block_ua: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Block':
        assert isinstance(obj, dict)
        blocked_at = from_none(obj.get("blocked_at"))
        block_ru = from_bool(obj.get("block_ru"))
        block_ua = from_bool(obj.get("block_ua"))
        return Block(blocked_at, block_ru, block_ua)

    def to_dict(self) -> dict:
        result: dict = {}
        result["blocked_at"] = from_none(self.blocked_at)
        result["block_ru"] = from_bool(self.block_ru)
        result["block_ua"] = from_bool(self.block_ua)
        return result


@dataclass
class Duration:
    seconds: int
    human: str

    @staticmethod
    def from_dict(obj: Any) -> 'Duration':
        assert isinstance(obj, dict)
        seconds = from_int(obj.get("seconds"))
        human = from_str(obj.get("human"))
        return Duration(seconds, human)

    def to_dict(self) -> dict:
        result: dict = {}
        result["seconds"] = from_int(self.seconds)
        result["human"] = from_str(self.human)
        return result


@dataclass
class MaterialData:
    updated_at: datetime
    poster: str
    year: int
    tagline: str
    description: str
    age: Optional[int]
    countries: List[str]
    genres: List[str]
    actors: List[str]
    directors: Optional[List[str]]
    studios: List[str]
    kinopoisk_rating: float
    kinopoisk_votes: Optional[int]
    imdb_rating: float
    imdb_votes: int
    mpaa_rating: None
    mpaa_votes: None

    @staticmethod
    def from_dict(obj: Any) -> 'MaterialData':
        assert isinstance(obj, dict)
        updated_at = from_datetime(obj.get("updated_at"))
        poster = from_str(obj.get("poster"))
        year = from_int(obj.get("year"))
        tagline = from_str(obj.get("tagline"))
        description = from_str(obj.get("description"))
        age = from_union([from_int, from_none], obj.get("age"))
        countries = from_list(from_str, obj.get("countries"))
        genres = from_list(from_str, obj.get("genres"))
        actors = from_list(from_str, obj.get("actors"))
        directors = from_union([from_none, lambda x: from_list(from_str, x)], obj.get("directors"))
        studios = from_list(from_str, obj.get("studios"))
        kinopoisk_rating = from_float(obj.get("kinopoisk_rating"))
        kinopoisk_votes = from_union([from_int, from_none], obj.get("kinopoisk_votes"))
        imdb_rating = from_float(obj.get("imdb_rating"))
        imdb_votes = from_int(obj.get("imdb_votes"))
        mpaa_rating = from_none(obj.get("mpaa_rating"))
        mpaa_votes = from_none(obj.get("mpaa_votes"))
        return MaterialData(updated_at, poster, year, tagline, description, age, countries, genres, actors, directors, studios, kinopoisk_rating, kinopoisk_votes, imdb_rating, imdb_votes, mpaa_rating, mpaa_votes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["updated_at"] = self.updated_at.isoformat()
        result["poster"] = from_str(self.poster)
        result["year"] = from_int(self.year)
        result["tagline"] = from_str(self.tagline)
        result["description"] = from_str(self.description)
        result["age"] = from_union([from_int, from_none], self.age)
        result["countries"] = from_list(from_str, self.countries)
        result["genres"] = from_list(from_str, self.genres)
        result["actors"] = from_list(from_str, self.actors)
        result["directors"] = from_union([from_none, lambda x: from_list(from_str, x)], self.directors)
        result["studios"] = from_list(from_str, self.studios)
        result["kinopoisk_rating"] = to_float(self.kinopoisk_rating)
        result["kinopoisk_votes"] = from_union([from_int, from_none], self.kinopoisk_votes)
        result["imdb_rating"] = to_float(self.imdb_rating)
        result["imdb_votes"] = from_int(self.imdb_votes)
        result["mpaa_rating"] = from_none(self.mpaa_rating)
        result["mpaa_votes"] = from_none(self.mpaa_votes)
        return result


@dataclass
class Movies:
    title_ru: str
    title_en: str
    year: int
    duration: Duration
    kinopoisk_id: int
    world_art_id: int
    pornolab_id: None
    token: str
    type: str
    camrip: bool
    source_type: None
    source_quality_type: None
    instream_ads: bool
    directors_version: bool
    iframe_url: str
    trailer_token: None
    trailer_iframe_url: None
    translator: str
    translator_id: int
    added_at: datetime
    category: str
    block: Block
    material_data: MaterialData

    @staticmethod
    def from_dict(obj: Any) -> 'Movies':
        assert isinstance(obj, dict)
        title_ru = from_str(obj.get("title_ru"))
        title_en = from_str(obj.get("title_en"))
        year = from_int(obj.get("year"))
        duration = Duration.from_dict(obj.get("duration"))
        kinopoisk_id = from_int(obj.get("kinopoisk_id"))
        world_art_id = from_int(obj.get("world_art_id"))
        pornolab_id = from_none(obj.get("pornolab_id"))
        token = from_str(obj.get("token"))
        type = from_str(obj.get("type"))
        camrip = from_bool(obj.get("camrip"))
        source_type = from_none(obj.get("source_type"))
        source_quality_type = from_none(obj.get("source_quality_type"))
        instream_ads = from_bool(obj.get("instream_ads"))
        directors_version = from_bool(obj.get("directors_version"))
        iframe_url = from_str(obj.get("iframe_url"))
        trailer_token = from_none(obj.get("trailer_token"))
        trailer_iframe_url = from_none(obj.get("trailer_iframe_url"))
        translator = from_str(obj.get("translator"))
        translator_id = from_int(obj.get("translator_id"))
        added_at = from_datetime(obj.get("added_at"))
        category = from_str(obj.get("category"))
        block = Block.from_dict(obj.get("block"))
        material_data = MaterialData.from_dict(obj.get("material_data"))
        return Movies(title_ru, title_en, year, duration, kinopoisk_id, world_art_id, pornolab_id, token, type, camrip, source_type, source_quality_type, instream_ads, directors_version, iframe_url, trailer_token, trailer_iframe_url, translator, translator_id, added_at, category, block, material_data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title_ru"] = from_str(self.title_ru)
        result["title_en"] = from_str(self.title_en)
        result["year"] = from_int(self.year)
        result["duration"] = to_class(Duration, self.duration)
        result["kinopoisk_id"] = from_int(self.kinopoisk_id)
        result["world_art_id"] = from_int(self.world_art_id)
        result["pornolab_id"] = from_none(self.pornolab_id)
        result["token"] = from_str(self.token)
        result["type"] = from_str(self.type)
        result["camrip"] = from_bool(self.camrip)
        result["source_type"] = from_none(self.source_type)
        result["source_quality_type"] = from_none(self.source_quality_type)
        result["instream_ads"] = from_bool(self.instream_ads)
        result["directors_version"] = from_bool(self.directors_version)
        result["iframe_url"] = from_str(self.iframe_url)
        result["trailer_token"] = from_none(self.trailer_token)
        result["trailer_iframe_url"] = from_none(self.trailer_iframe_url)
        result["translator"] = from_str(self.translator)
        result["translator_id"] = from_int(self.translator_id)
        result["added_at"] = self.added_at.isoformat()
        result["category"] = from_str(self.category)
        result["block"] = to_class(Block, self.block)
        result["material_data"] = to_class(MaterialData, self.material_data)
        return result


@dataclass
class SeasonEpisodesCount:
    season_number: int
    episodes_count: int
    episodes: List[int]

    @staticmethod
    def from_dict(obj: Any) -> 'SeasonEpisodesCount':
        assert isinstance(obj, dict)
        season_number = from_int(obj.get("season_number"))
        episodes_count = from_int(obj.get("episodes_count"))
        episodes = from_list(from_int, obj.get("episodes"))
        return SeasonEpisodesCount(season_number, episodes_count, episodes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["season_number"] = from_int(self.season_number)
        result["episodes_count"] = from_int(self.episodes_count)
        result["episodes"] = from_list(from_int, self.episodes)
        return result


@dataclass
class Serials:
    title_ru: str
    title_en: str
    year: int
    token: str
    type: str
    kinopoisk_id: int
    world_art_id: int
    translator: str
    translator_id: int
    iframe_url: str
    trailer_token: str
    trailer_iframe_url: str
    seasons_count: int
    episodes_count: int
    category: str
    block: Block
    season_episodes_count: List[SeasonEpisodesCount]
    material_data: MaterialData

    @staticmethod
    def from_dict(obj: Any) -> 'Serials':
        assert isinstance(obj, dict)
        title_ru = from_str(obj.get("title_ru"))
        title_en = from_str(obj.get("title_en"))
        year = from_int(obj.get("year"))
        token = from_str(obj.get("token"))
        type = from_str(obj.get("type"))
        kinopoisk_id = from_int(obj.get("kinopoisk_id"))
        world_art_id = from_int(obj.get("world_art_id"))
        translator = from_str(obj.get("translator"))
        translator_id = from_int(obj.get("translator_id"))
        iframe_url = from_str(obj.get("iframe_url"))
        trailer_token = from_str(obj.get("trailer_token"))
        trailer_iframe_url = from_str(obj.get("trailer_iframe_url"))
        seasons_count = from_int(obj.get("seasons_count"))
        episodes_count = from_int(obj.get("episodes_count"))
        category = from_str(obj.get("category"))
        block = Block.from_dict(obj.get("block"))
        season_episodes_count = from_list(SeasonEpisodesCount.from_dict, obj.get("season_episodes_count"))
        material_data = MaterialData.from_dict(obj.get("material_data"))
        return Serials(title_ru, title_en, year, token, type, kinopoisk_id, world_art_id, translator, translator_id, iframe_url, trailer_token, trailer_iframe_url, seasons_count, episodes_count, category, block, season_episodes_count, material_data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title_ru"] = from_str(self.title_ru)
        result["title_en"] = from_str(self.title_en)
        result["year"] = from_int(self.year)
        result["token"] = from_str(self.token)
        result["type"] = from_str(self.type)
        result["kinopoisk_id"] = from_int(self.kinopoisk_id)
        result["world_art_id"] = from_int(self.world_art_id)
        result["translator"] = from_str(self.translator)
        result["translator_id"] = from_int(self.translator_id)
        result["iframe_url"] = from_str(self.iframe_url)
        result["trailer_token"] = from_str(self.trailer_token)
        result["trailer_iframe_url"] = from_str(self.trailer_iframe_url)
        result["seasons_count"] = from_int(self.seasons_count)
        result["episodes_count"] = from_int(self.episodes_count)
        result["category"] = from_str(self.category)
        result["block"] = to_class(Block, self.block)
        result["season_episodes_count"] = from_list(lambda x: to_class(SeasonEpisodesCount, x), self.season_episodes_count)
        result["material_data"] = to_class(MaterialData, self.material_data)
        return result


def movies_from_dict(s: Any) -> Movies:
    return Movies.from_dict(s)


def movies_to_dict(x: Movies) -> Any:
    return to_class(Movies, x)


def serials_from_dict(s: Any) -> Serials:
    return Serials.from_dict(s)


def serials_to_dict(x: Serials) -> Any:
    return to_class(Serials, x)
