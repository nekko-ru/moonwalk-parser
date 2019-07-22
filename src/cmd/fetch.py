#!/usr/bin/env python3
from loguru import logger as log
from src.moonwalk.api import MoonwalkAPI
from src.transform import Transformer

log.info('Получение списка всех сериалов')
data = MoonwalkAPI().get_serials()

tr = Transformer(data)
log.debug(f'После преобразования {len(tr.storage)}')
