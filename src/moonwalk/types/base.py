from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class Base:
    @dataclass
    class Block:
        blocked_at: str
        block_ru: bool
        block_ua: bool

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

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'Base':
        """
        Создает на основе json заполненый класс
        :param data: Валиднйы JSON из ответа MoonWalk
        :returns:
        """
        pass
