# MoonWalk Parser

[![Build Status](https://travis-ci.org/nekko-ru/moonwalk-parser.svg?branch=master)](https://travis-ci.org/nekko-ru/moonwalk-parser)

Парсит списки аниме сериалов, фильмов в удобные для работы обьекты, а так же группирует переводы.

## Установка

Для начала нужно установить зависимости путем выполнения в консоли команды

```
$ pip install -r requirements.txt

Collecting requests==2.22.0 (from -r requirements.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/51/bd/23c926cd341ea6b7dd0b2a00aba99ae0f828be89d72b2190f27c11d4b7fb/requests-2.22.0-py2.py3-none-any.whl
Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 (from requests==2.22.0->-r requirements.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/e6/60/247f23a7121ae632d62811ba7f273d0e58972d75e58a94d329d51550a47d/urllib3-1.25.3-py2.py3-none-any.whl
Collecting certifi>=2017.4.17 (from requests==2.22.0->-r requirements.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/69/1b/b853c7a9d4f6a6d00749e94eb6f3a041e342a885b87340b79c1ef73e3a78/certifi-2019.6.16-py2.py3-none-any.whl
Collecting chardet<3.1.0,>=3.0.2 (from requests==2.22.0->-r requirements.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl
Collecting idna<2.9,>=2.5 (from requests==2.22.0->-r requirements.txt (line 1))
  Using cached https://files.pythonhosted.org/packages/14/2c/cd551d81dbe15200be1cf41cd03869a46fe7226e7450af7a6545bfc474c9/idna-2.8-py2.py3-none-any.whl
Installing collected packages: urllib3, certifi, chardet, idna, requests
Successfully installed certifi-2019.6.16 chardet-3.0.4 idna-2.8 requests-2.22.0 urllib3-1.25.3
```

## Пример работы

... **_some magic_** ...

```json5
{
	"title": "Психо-паспорт ТВ-1",
    "title_en": "Psycho-pass TV-1",
    "title_or": "original name",
    "annotation": "События аниме происходят в 2112 году. В этом будущем можно мгновенно измерить психическое состояние любого лица и вероятность совершения им преступлений устройством под названием «Психо-Паспорт», установленным на теле каждого гражданина.",
    "description": "События аниме происходят в 2112 году. В этом будущем можно мгновенно измерить психическое состояние любого лица и вероятность совершения им преступлений устройством под названием «Психо-Паспорт», установленным на теле каждого гражданина. Если индекс коэффициента преступности оказывается слишком высок, человек вынужден пройти принудительное лечение либо, при необходимости, подлежит уничтожению. Выполнением этой задачи занимаются специальные команды из Бюро общественной безопасности, состоящие из потенциальных преступников (так называемых «псов»), и инспекторов полиции, осуществляющих надзор над своими подопечными. Члены каждой команды получают особое оружие - Доминатор, способное открывать огонь только по тем, чей коэффициент преступности превышает допустимую норму. История повествует о Синье Когами, который должен раскрывать преступления в этом тёмном будущем.",
    "posters": ["https://st.kp.yandex.net/images/film_iphone/iphone360_707090.jpg"],
    "type": "serial",
    "genres": [
        "аниме",
        "мультфильм",
        "приключения",
        "фантастика"
    ],
    "translators": [
    	{
    		"id": 10,
    		"name": "AniLib",
    		"episodes": [
    		    "http://moonwalk.cc/serial/05637d0c8b3e7e2f23caaa4ab6ce0ee2/iframe?season=01&episode=01&nocontrols=1",
    		    "http://moonwalk.cc/serial/05637d0c8b3e7e2f23caaa4ab6ce0ee2/iframe?season=01&episode=02&nocontrols=1",
    		    "http://moonwalk.cc/serial/05637d0c8b3e7e2f23caaa4ab6ce0ee2/iframe?season=01&episode=03&nocontrols=1"
    		]
    	},
    	{
    		"id": 13,
    		"name": "AniDUB",
    		"episodes": [
    		    "http://moonwalk.cc/serial/05637d0c8b3e7e2f23caaa4ab6ce0ee2/iframe?season=01&episode=01&nocontrols=1",
    		    "http://moonwalk.cc/serial/05637d0c8b3e7e2f23caaa4ab6ce0ee2/iframe?season=01&episode=02&nocontrols=1",
    		    "http://moonwalk.cc/serial/05637d0c8b3e7e2f23caaa4ab6ce0ee2/iframe?season=01&episode=03&nocontrols=1&nocontrols_translations=1"
    		]
    	}		
    ],
    "status": "Вышло",
    "year": "2012",
    "world_art_id": "2220",
    "kinopoisk_id": "707090",
    "countries": [
        "Япония"
    ],
    "actors": [
        "Кана Ханадзава",
        "Роберт МакКолам",
        "Кейт Оксли",
        "Томокадзу Сэки",
        "Сидзука Ито",
        "Кэндзи Нодзима",
        "Лидия Маккей",
        "Терри Доти",
        "Брайан Мэсси",
        "Кинрю Аримото"
    ],
    "directors": [
        "Наоёси Сиотани",
        "Кацуюки Мотохиро",
        "Ицуро Кавасаки"
    ],
    "studios": [
        "Dentsu",
        "Fuji Television Network Inc.",
        "Index",
        "Kyoraku Sangyo",
        "Nitroplus",
        "Production I.G.",
        "Sony Music Entertainment",
        "Tatsunoko Productions Co. Ltd.",
        "Toho Company"
    ]
}
```
