#!/usr/bin/env python3
import requests
from loguru import logger as log
from src.moonwalk.api import MoonwalkAPI
from src.transform import Transformer

log.info('Получение списка всех сериалов')
data = MoonwalkAPI().get_serials()

tr = Transformer(data[:10])
log.debug(f'После преобразования {len(tr.storage)}')

for serial in tr.storage.values():
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "fc050eed-d719-431c-a486-2a3e78ef32c5"
    }
    url = "http://localhost:8084/anime.create"

    querystring = {
        "access_token": "T4VJeTrD_ZqLmqFx3wknxPTLr-tgiyy0ovNpfQ97nRHg4orAFtGYsq1NoO9DyT1vBpFIMHHrra35VkDw3_vZtq3znKXFuruQaiA5FkQ01fJy2euW_1tD1wmyRrhN8Dg1-zyEuq_-gSqG0HPFrigGcbY4HLt3-TDkP_ROJX9IQjs="}

    res = requests.request("POST", url, json=serial.to_dict(), headers=headers, params=querystring)
