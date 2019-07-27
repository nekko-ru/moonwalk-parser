#!/usr/bin/env python3
import requests
from loguru import logger as log
from src.moonwalk.api import MoonwalkAPI
from src.transform import CreateNew

log.info('Получение списка всех сериалов')
data = MoonwalkAPI().get_serials()

tr = CreateNew(data)
log.debug(f'После преобразования {len(tr.storage)}')

log.debug(f'Создание сериалов на сервере')
for serial in tr.storage.values():
    # данные заголовки не обязательны
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "fc050eed-d719-431c-a486-2a3e78ef32c5"
    }
    # ссылка на api
    url = "http://localhost:8084/anime.create"

    querystring = {
        # хохохо, не бойтесь локальный токен, так еще и без refresh_token'а
        "access_token": "T4VJeTrD_ZqLmqFx3wknxPTLr-tgiyy0ovNpfQ97nRHg4orAFtGYsq1NoO9DyT1vBpFIMHHrra35VkDw3_vZtq3znKXFuruQaiA5FkQ01fJy2euW_1tD1wmyRrhN8Dg1-zyEuq_-gSqG0HPFrigGcbY4HLt3-TDkP_ROJX9IQjs="}

    # отправка запроса
    # WARNING: замените на свой способ отправки новой серии
    res = requests.request("POST", url, json=serial.to_dict(), headers=headers, params=querystring)
    if res.ok:
        log.debug(f' * создано {serial.title}')
    else:
        raise Exception(res.json()['data'])
