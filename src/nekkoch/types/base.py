#     result = anime_from_dict(json.loads(json_string))
#     result = anime_to_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, List, Any, TypeVar, Callable, Type, cast

from src.moonwalk.types.base import from_float, to_float

T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    return x or '-'


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


@dataclass
class Translator:
    id: Optional[int]
    name: Optional[str]
    episodes: Optional[List[str]]

    @staticmethod
    def from_dict(obj: Any) -> 'Translator':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        episodes = from_union([lambda x: from_list(from_str, x), from_none], obj.get("episodes"))
        return Translator(id, name, episodes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["name"] = from_union([from_str, from_none], self.name)
        result["episodes"] = from_union([lambda x: from_list(from_str, x), from_none], self.episodes)
        return result


@dataclass
class Anime:
    id: Optional[int]
    title: Optional[str]
    title_en: Optional[str]
    title_or: Optional[str]
    annotation: Optional[str]
    description: Optional[str]
    posters: Optional[List[str]]
    type: Optional[str]
    genres: Optional[List[str]]
    translators: Optional[List[Translator]]
    status: Optional[str]
    year: Optional[int]
    world_art_id: Optional[int]
    kinopoisk_id: Optional[int]
    rating: Optional[float]
    votes: Optional[int]
    countries: Optional[List[str]]
    actors: Optional[List[str]]
    directors: Optional[List[str]]
    studios: Optional[List[str]]

    @staticmethod
    def from_dict(obj: Any) -> 'Anime':
        assert isinstance(obj, dict)
        id_ = from_union([from_int, from_none], obj.get("id"))
        title = from_union([from_str, from_none], obj.get("title"))
        title_en = from_union([from_str, from_none], obj.get("title_en"))
        title_or = from_union([from_str, from_none], obj.get("title_or"))
        annotation = from_union([from_str, from_none], obj.get("annotation"))
        description = from_union([from_str, from_none], obj.get("description", "-"))
        posters = from_union([lambda x: from_list(from_str, x), from_none], obj.get("posters"))
        type = from_union([from_str, from_none], obj.get("type"))
        genres = from_union([lambda x: from_list(from_str, x), from_none], obj.get("genres"))
        translators = from_union([lambda x: from_list(Translator.from_dict, x), from_none], obj.get("translators"))
        status = from_union([from_str, from_none], obj.get("status"))
        year = from_union([from_none, lambda x: int(from_str(x))], obj.get("year"))
        world_art_id = from_union([from_str, from_none], obj.get("world_art_id"))
        kinopoisk_id = from_union([from_str, from_none], obj.get("kinopoisk_id"))
        rating = from_union([from_float, from_none], obj.get("rating"))
        votes = from_union([from_int, from_none], obj.get("votes"))
        countries = from_union([lambda x: from_list(from_str, x), from_none], obj.get("countries"))
        actors = from_union([lambda x: from_list(from_str, x), from_none], obj.get("actors"))
        directors = from_union([lambda x: from_list(from_str, x), from_none], obj.get("directors"))
        studios = from_union([lambda x: from_list(from_str, x), from_none], obj.get("studios"))
        return Anime(id_, title, title_en, title_or, annotation, description, posters, type, genres, translators, status, year, world_art_id, kinopoisk_id, rating, votes, countries, actors, directors, studios)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["title"] = from_union([from_str, from_none], self.title)
        result["title_en"] = from_union([from_str, from_none], self.title_en)
        result["title_or"] = from_union([from_str, from_none], self.title_or)
        result["annotation"] = from_union([from_str, from_none], self.annotation)
        result["description"] = from_union([from_str, from_none], self.description)
        result["posters"] = from_union([lambda x: from_list(from_str, x), from_none], self.posters)
        result["type"] = from_union([from_str, from_none], self.type)
        result["genres"] = from_union([lambda x: from_list(from_str, x), from_none], self.genres)
        result["translators"] = from_union([lambda x: from_list(lambda x: to_class(Translator, x), x), from_none], self.translators)
        result["status"] = from_union([from_str, from_none], self.status)
        result["year"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.year)
        result["world_art_id"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.world_art_id)
        result["kinopoisk_id"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.kinopoisk_id)
        result["rating"] = from_union([to_float, from_none], self.rating)
        result["votes"] = from_union([from_int, from_none], self.votes)
        result["countries"] = from_union([lambda x: from_list(from_str, x), from_none], self.countries)
        result["actors"] = from_union([lambda x: from_list(from_str, x), from_none], self.actors)
        result["directors"] = from_union([lambda x: from_list(from_str, x), from_none], self.directors)
        result["studios"] = from_union([lambda x: from_list(from_str, x), from_none], self.studios)
        return result


def anime_from_dict(s: Any) -> Anime:
    return Anime.from_dict(s)


def anime_to_dict(x: Anime) -> Any:
    return to_class(Anime, x)
