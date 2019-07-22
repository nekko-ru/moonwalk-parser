#!/usr/bin/env python3
from loguru import logger as log
from src.moonwalk.api import MoonwalkAPI


log.info('Получение списка всех сериалов')
_ = MoonwalkAPI().get_serials()
