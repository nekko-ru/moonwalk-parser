#!/usr/bin/env python3
import requests
from loguru import logger as log

# setup logger
log.add("moonwalk_update_{time}.log", retention="1 week", compression="zip", enqueue=True, serialize=True) 

from src.moonwalk.api import MoonwalkAPI
from src.transform import CreateNew, Update

import src.models.AnimeModel

log.info('Получение списка обновлений для сериалов')
data = MoonwalkAPI().updates_serials()

log.debug('Начинаем обновление аниме')
upd = Update(data[::-1]).updated
log.info(f'Обновлено успешно {len(upd)}')
