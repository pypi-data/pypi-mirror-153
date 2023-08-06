REST-сервис на django-rest-framework для доступа к базе ГАР
------------------------------------------------------------

Этот сервис - результат объединения разработок:

* django-rest-framework <http://www.django-rest-framework.org/>
* m3-gar

Формат сервиса
--------------

Список адресных объектов
========================

::

    GET /gar/v1/addrobj/

:Параметры:

:level:
    Тип: число или список чисел через запятую.

    Фильтрация по уровню адресного объекта.

:parent:
    Тип: `hierarchy:objectid`
        `hierarchy` - Вид иерархии - `all`, `mun` или `adm`

        `objectid` - `objectid` родительского объекта

    Фильтрация по родительскому адресному объекту.
:region_code:
    Тип: число или список чисел через запятую.

    Фильтрация по коду региона.
:name:
    Тип: строка символов.

    Поиск адресного объекта по содержанию строки в наименовании.

:page:
    Тип: число.

    Страница вывода результатов.

----

:Результат:
    Тип: application/json.

    Результаты выводятся по страницам согласно настройкам DRF.

----

:Примеры:

::

    GET /gar/v1/addrobj/?name=Шамбалыгский&level=8&parent=adm:210893

    {
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": 250006,
          "params": [
            {
              "id": 3197562,
              "typeid": {
                "id": 5,
                "name": "Почтовый индекс",
                "code": "PostIndex",
                "desc": "Информация о почтовом индексе",
                "updatedate": "2018-06-15",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 207679,
              "changeid": 533863,
              "changeidend": 0,
              "value": "667901",
              "updatedate": "2017-11-16",
              "startdate": "1900-01-01",
              "enddate": "2079-06-06"
            }
          ],
          "objectguid": "7effc9de-7888-440b-b2a0-cc5432bc09a5",
          "changeid": 533888,
          "name": "Шамбалыгский",
          "typename": "пер",
          "level": "8",
          "previd": 249989,
          "nextid": 0,
          "updatedate": "2019-12-13",
          "startdate": "1900-01-01",
          "enddate": "2079-06-06",
          "isactual": true,
          "isactive": true,
          "opertypeid": 1,
          "objectid": 207679
        }
      ]
    }


Адресный объект
===============
::

    GET /gar/v1/addrobj/:objectid:/

:Параметры:

:objectid:
    Тип: число.

    Идентификатор адресного объекта


----

:Результат:
    Тип: application/json.

----

:Примеры:

::

    GET /gar/v1/addrobj/207679/

    {
      "id": 250006,
      "params": [
        {
          "id": 3197562,
          "typeid": {
            "id": 5,
            "name": "Почтовый индекс",
            "code": "PostIndex",
            "desc": "Информация о почтовом индексе",
            "updatedate": "2018-06-15",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 207679,
          "changeid": 533863,
          "changeidend": 0,
          "value": "667901",
          "updatedate": "2017-11-16",
          "startdate": "1900-01-01",
          "enddate": "2079-06-06"
        }
      ],
      "objectguid": "7effc9de-7888-440b-b2a0-cc5432bc09a5",
      "changeid": 533888,
      "name": "Шамбалыгский",
      "typename": "пер",
      "level": "8",
      "previd": 249989,
      "nextid": 0,
      "updatedate": "2019-12-13",
      "startdate": "1900-01-01",
      "enddate": "2079-06-06",
      "isactual": true,
      "isactive": true,
      "opertypeid": 1,
      "objectid": 207679
    }

Список домов
============

::

    GET /gar/v1/houses/


:Параметры:

:parent:
    Тип: `hierarchy:objectid`
        `hierarchy` - Вид иерархии - `all`, `mun` или `adm`

        `objectid` - `objectid` родительского объекта

    Фильтрация по родительскому адресному объекту.

:housenum:
    Тип: строка символов.

    Поиск дома по содержанию строки в номере.

:page:
    Тип: число. Страница вывода результатов.

----

:Результат:
    Тип: application/json.

    Результаты выводятся по страницам согласно настройкам DRF.

----

:Примеры:

::

    GET /gar/v1/houses/?parent=adm:210826&name=5

    {
      "count": 65,
      "next": "http://127.0.0.1:8000/gar/v1/houses/?name=5&page=2&parent=adm%3A210826",
      "previous": null,
      "results": [
        {
          "id": 52384730,
          "params": [
            {
              "id": 197175620,
              "typeid": {
                "id": 3,
                "name": "ИНН ФЛ ТЕР УЧ",
                "code": "territorialifnsflcode",
                "desc": "Территориальный участок ИФНС ЮЛ",
                "updatedate": "2018-06-15",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 51296115,
              "changeidend": 158819227,
              "value": "1717",
              "updatedate": "2020-11-21",
              "startdate": "1900-01-01",
              "enddate": "2020-11-21"
            },
            {
              "id": 197175630,
              "typeid": {
                "id": 6,
                "name": "ОКАТО",
                "code": "OKATO",
                "desc": "ОКАТО",
                "updatedate": "2018-06-19",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 51296115,
              "changeidend": 0,
              "value": "93243825001",
              "updatedate": "2019-12-14",
              "startdate": "1900-01-01",
              "enddate": "2079-06-06"
            },
            {
              "id": 197175631,
              "typeid": {
                "id": 5,
                "name": "Почтовый индекс",
                "code": "PostIndex",
                "desc": "Информация о почтовом индексе",
                "updatedate": "2018-06-15",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 51296115,
              "changeidend": 0,
              "value": "667903",
              "updatedate": "2019-12-14",
              "startdate": "1900-01-01",
              "enddate": "2079-06-06"
            },
            {
              "id": 197175643,
              "typeid": {
                "id": 14,
                "name": "Признак присвоения адреса",
                "code": "DivisionType",
                "desc": "Признак в каком делении присвоен адрес, муниципальном/административном",
                "updatedate": "2018-12-14",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 51296115,
              "changeidend": 0,
              "value": "0",
              "updatedate": "2019-12-14",
              "startdate": "1900-01-01",
              "enddate": "2079-06-06"
            },
            {
              "id": 197175692,
              "typeid": {
                "id": 15,
                "name": "Порядковый номер",
                "code": "Counter",
                "desc": "Порядковый номер обьекта в рамках родителя",
                "updatedate": "2018-12-14",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 51296115,
              "changeidend": 0,
              "value": "18",
              "updatedate": "2019-12-14",
              "startdate": "1900-01-01",
              "enddate": "2079-06-06"
            },
            {
              "id": 197175626,
              "typeid": {
                "id": 7,
                "name": "OKTMO",
                "code": "OKTMO",
                "desc": "OKTMO",
                "updatedate": "2018-06-19",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 51296115,
              "changeidend": 51296790,
              "value": "93643425",
              "updatedate": "2019-12-14",
              "startdate": "1900-01-01",
              "enddate": "2019-12-13"
            },
            {
              "id": 197175728,
              "typeid": {
                "id": 7,
                "name": "OKTMO",
                "code": "OKTMO",
                "desc": "OKTMO",
                "updatedate": "2018-06-19",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 51296790,
              "changeidend": 0,
              "value": "93643425101",
              "updatedate": "2019-12-14",
              "startdate": "2019-12-13",
              "enddate": "2079-06-06"
            },
            {
              "id": 197175636,
              "typeid": {
                "id": 13,
                "name": "Реестровый номер",
                "code": "ReestrNum",
                "desc": "Реестровый номер адресного объекта",
                "updatedate": "2018-11-12",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 51296115,
              "changeidend": 51296790,
              "value": "936434251010000000220018000000005",
              "updatedate": "2019-12-14",
              "startdate": "1900-01-01",
              "enddate": "2019-12-13"
            },
            {
              "id": 197176157,
              "typeid": {
                "id": 13,
                "name": "Реестровый номер",
                "code": "ReestrNum",
                "desc": "Реестровый номер адресного объекта",
                "updatedate": "2018-11-12",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 51296790,
              "changeidend": 0,
              "value": "936434251010000000220018000000000",
              "updatedate": "2019-12-14",
              "startdate": "2019-12-13",
              "enddate": "2079-06-06"
            },
            {
              "id": 197173900,
              "typeid": {
                "id": 1,
                "name": "ИФНС ФЛ",
                "code": "IFNSFL",
                "desc": "ИФНС ФЛ",
                "updatedate": "2018-06-15",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 51296115,
              "changeidend": 158819227,
              "value": "1720",
              "updatedate": "2020-11-21",
              "startdate": "1900-01-01",
              "enddate": "2020-11-21"
            },
            {
              "id": 679599960,
              "typeid": {
                "id": 1,
                "name": "ИФНС ФЛ",
                "code": "IFNSFL",
                "desc": "ИФНС ФЛ",
                "updatedate": "2018-06-15",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 158819227,
              "changeidend": 0,
              "value": "1700",
              "updatedate": "2020-11-21",
              "startdate": "2020-11-21",
              "enddate": "2079-06-06"
            },
            {
              "id": 679666370,
              "typeid": {
                "id": 2,
                "name": "ИФНС ЮЛ",
                "code": "IFNSUL",
                "desc": "ИФНС ЮЛ",
                "updatedate": "2018-06-15",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 158819227,
              "changeidend": 0,
              "value": "1700",
              "updatedate": "2020-11-21",
              "startdate": "2020-11-21",
              "enddate": "2079-06-06"
            },
            {
              "id": 197175624,
              "typeid": {
                "id": 4,
                "name": "ИФНС ЮЛ ТЕР УЧ",
                "code": "territorialifnsulcode",
                "desc": "Территориальный участок ИФНС ФЛ",
                "updatedate": "2018-06-15",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 51296115,
              "changeidend": 158819227,
              "value": "1717",
              "updatedate": "2020-11-21",
              "startdate": "1900-01-01",
              "enddate": "2020-11-21"
            },
            {
              "id": 197175616,
              "typeid": {
                "id": 2,
                "name": "ИФНС ЮЛ",
                "code": "IFNSUL",
                "desc": "ИФНС ЮЛ",
                "updatedate": "2018-06-15",
                "startdate": "2011-11-01",
                "enddate": "2079-06-06",
                "isactive": true
              },
              "objectid": 33665495,
              "changeid": 51296115,
              "changeidend": 158819227,
              "value": "1720",
              "updatedate": "2020-11-21",
              "startdate": "1900-01-01",
              "enddate": "2020-11-21"
            }
          ],
          "housetype": {
            "id": 3,
            "name": "Домовладение",
            "shortname": "двлд.",
            "desc": "Домовладение",
            "updatedate": "1900-01-01",
            "startdate": "1900-01-01",
            "enddate": "2015-11-05",
            "isactive": false
          },
          "addtype1": null,
          "addtype2": null,
          "objectguid": "0e27bfa6-d3e2-4160-967a-5f14d43fbc98",
          "changeid": 51296790,
          "housenum": "18",
          "addnum1": null,
          "addnum2": null,
          "previd": 20010713,
          "nextid": 0,
          "updatedate": "2019-12-14",
          "startdate": "2019-12-13",
          "enddate": "2079-06-06",
          "isactual": true,
          "isactive": true,
          "opertypeid": 20,
          "objectid": 33665495
        }
      ]
    }


Информация о доме
=================
::

    GET /gar/v1/houses/:objectid:/

:Параметры:

:objectid:
    Тип: число.

    Идентификатор дома


----

:Результат:
    Тип: application/json.

----

:Примеры:

::

    GET /gar/v1/houses/33663074/

    {
      "id": 60865585,
      "params": [
        {
          "id": 197161766,
          "typeid": {
            "id": 1,
            "name": "ИФНС ФЛ",
            "code": "IFNSFL",
            "desc": "ИФНС ФЛ",
            "updatedate": "2018-06-15",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 51292720,
          "changeidend": 158819225,
          "value": "1720",
          "updatedate": "2020-11-21",
          "startdate": "1900-01-01",
          "enddate": "2020-11-21"
        },
        {
          "id": 197163461,
          "typeid": {
            "id": 13,
            "name": "Реестровый номер",
            "code": "ReestrNum",
            "desc": "Реестровый номер адресного объекта",
            "updatedate": "2018-11-12",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 51293350,
          "changeidend": 0,
          "value": "936434251010000000220012000000000",
          "updatedate": "2019-12-14",
          "startdate": "2019-12-13",
          "enddate": "2079-06-06"
        },
        {
          "id": 197163411,
          "typeid": {
            "id": 6,
            "name": "ОКАТО",
            "code": "OKATO",
            "desc": "ОКАТО",
            "updatedate": "2018-06-19",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 51292720,
          "changeidend": 0,
          "value": "93243825001",
          "updatedate": "2019-12-14",
          "startdate": "1900-01-01",
          "enddate": "2079-06-06"
        },
        {
          "id": 197163416,
          "typeid": {
            "id": 5,
            "name": "Почтовый индекс",
            "code": "PostIndex",
            "desc": "Информация о почтовом индексе",
            "updatedate": "2018-06-15",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 51292720,
          "changeidend": 0,
          "value": "667903",
          "updatedate": "2019-12-14",
          "startdate": "1900-01-01",
          "enddate": "2079-06-06"
        },
        {
          "id": 197163430,
          "typeid": {
            "id": 14,
            "name": "Признак присвоения адреса",
            "code": "DivisionType",
            "desc": "Признак в каком делении присвоен адрес, муниципальном/административном",
            "updatedate": "2018-12-14",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 51292720,
          "changeidend": 0,
          "value": "0",
          "updatedate": "2019-12-14",
          "startdate": "1900-01-01",
          "enddate": "2079-06-06"
        },
        {
          "id": 197163432,
          "typeid": {
            "id": 15,
            "name": "Порядковый номер",
            "code": "Counter",
            "desc": "Порядковый номер обьекта в рамках родителя",
            "updatedate": "2018-12-14",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 51292720,
          "changeidend": 0,
          "value": "12",
          "updatedate": "2019-12-14",
          "startdate": "1900-01-01",
          "enddate": "2079-06-06"
        },
        {
          "id": 197163408,
          "typeid": {
            "id": 7,
            "name": "OKTMO",
            "code": "OKTMO",
            "desc": "OKTMO",
            "updatedate": "2018-06-19",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 51292720,
          "changeidend": 51293350,
          "value": "93643425",
          "updatedate": "2019-12-14",
          "startdate": "1900-01-01",
          "enddate": "2019-12-13"
        },
        {
          "id": 197163454,
          "typeid": {
            "id": 7,
            "name": "OKTMO",
            "code": "OKTMO",
            "desc": "OKTMO",
            "updatedate": "2018-06-19",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 51293350,
          "changeidend": 0,
          "value": "93643425101",
          "updatedate": "2019-12-14",
          "startdate": "2019-12-13",
          "enddate": "2079-06-06"
        },
        {
          "id": 197163423,
          "typeid": {
            "id": 13,
            "name": "Реестровый номер",
            "code": "ReestrNum",
            "desc": "Реестровый номер адресного объекта",
            "updatedate": "2018-11-12",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 51292720,
          "changeidend": 51293350,
          "value": "936434251010000000220012000000005",
          "updatedate": "2019-12-14",
          "startdate": "1900-01-01",
          "enddate": "2019-12-13"
        },
        {
          "id": 197163397,
          "typeid": {
            "id": 3,
            "name": "ИНН ФЛ ТЕР УЧ",
            "code": "territorialifnsflcode",
            "desc": "Территориальный участок ИФНС ЮЛ",
            "updatedate": "2018-06-15",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 51292720,
          "changeidend": 158819225,
          "value": "1717",
          "updatedate": "2020-11-21",
          "startdate": "1900-01-01",
          "enddate": "2020-11-21"
        },
        {
          "id": 679599958,
          "typeid": {
            "id": 1,
            "name": "ИФНС ФЛ",
            "code": "IFNSFL",
            "desc": "ИФНС ФЛ",
            "updatedate": "2018-06-15",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 158819225,
          "changeidend": 0,
          "value": "1700",
          "updatedate": "2020-11-21",
          "startdate": "2020-11-21",
          "enddate": "2079-06-06"
        },
        {
          "id": 197163402,
          "typeid": {
            "id": 4,
            "name": "ИФНС ЮЛ ТЕР УЧ",
            "code": "territorialifnsulcode",
            "desc": "Территориальный участок ИФНС ФЛ",
            "updatedate": "2018-06-15",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 51292720,
          "changeidend": 158819225,
          "value": "1717",
          "updatedate": "2020-11-21",
          "startdate": "1900-01-01",
          "enddate": "2020-11-21"
        },
        {
          "id": 197161768,
          "typeid": {
            "id": 2,
            "name": "ИФНС ЮЛ",
            "code": "IFNSUL",
            "desc": "ИФНС ЮЛ",
            "updatedate": "2018-06-15",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 51292720,
          "changeidend": 158819225,
          "value": "1720",
          "updatedate": "2020-11-21",
          "startdate": "1900-01-01",
          "enddate": "2020-11-21"
        },
        {
          "id": 679666368,
          "typeid": {
            "id": 2,
            "name": "ИФНС ЮЛ",
            "code": "IFNSUL",
            "desc": "ИФНС ЮЛ",
            "updatedate": "2018-06-15",
            "startdate": "2011-11-01",
            "enddate": "2079-06-06",
            "isactive": true
          },
          "objectid": 33663074,
          "changeid": 158819225,
          "changeidend": 0,
          "value": "1700",
          "updatedate": "2020-11-21",
          "startdate": "2020-11-21",
          "enddate": "2079-06-06"
        }
      ],
      "housetype": {
        "id": 3,
        "name": "Домовладение",
        "shortname": "двлд.",
        "desc": "Домовладение",
        "updatedate": "1900-01-01",
        "startdate": "1900-01-01",
        "enddate": "2015-11-05",
        "isactive": false
      },
      "addtype1": null,
      "addtype2": null,
      "objectguid": "85e4ae37-bd1a-42ec-ad27-5c4343d53adf",
      "changeid": 51293350,
      "housenum": "12",
      "addnum1": null,
      "addnum2": null,
      "previd": 20009203,
      "nextid": 0,
      "updatedate": "2019-12-14",
      "startdate": "2019-12-13",
      "enddate": "2079-06-06",
      "isactual": true,
      "isactive": true,
      "opertypeid": 20,
      "objectid": 33663074
    }



Установка
---------

1. Установите `m3-rest-gar`::

    pip install m3-rest-gar

2. Добавьте `rest_framework, `django_filters`, `m3_gar`, `m3_rest_gar`
в `INSTALLED_APPS` и установите `DjangoFilterBackend`

::

    INSTALLED_APPS = [
        ...,
        'rest_framework',
        'django_filters',
        'm3_gar',
        'm3_rest_gar',
    ]

    REST_FRAMEWORK = {
        ...,
        'DEFAULT_FILTER_BACKENDS': [
            'django_filters.rest_framework.DjangoFilterBackend',
        ],
    }

3. Настройте `m3_gar` и импортируйте данные

4. Добавьте urlpatterns m3_rest_gar

::

    urlpatterns = [
        ...,
        path('gar/', include('m3_rest_gar.urls')),
    ]


Настройка аутентификации OAuth2
-------------------------------

Установить пакет OAuth2

::

    pip install django-oauth-toolkit


Настроить приложение (settings.py)

::

    INSTALLED_APPS = [
        ...
        'oauth2_provider',
    ]

    MIDDLEWARE = [
        ...,
        'oauth2_provider.middleware.OAuth2TokenMiddleware',
    ]

    AUTHENTICATION_BACKENDS = [
        'oauth2_provider.backends.OAuth2Backend',
        # Если нужен доступ в /admin:
        # 'django.contrib.auth.backends.ModelBackend',
    ]

    REST_FRAMEWORK = {
        ...,
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
    }

Добавить urlpatterns (urls.py)

::

    urlpatterns = patterns('',
        ...
        path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    )


Выполнить миграцию базы

::

    python manage.py migrate


Регистрация клиентского приложения
==================================

Заходим в django-admin /admin

В разделе Users создаем пользователя от имени которого будут выполняться запросы.
(Можно всех клиентов привязать к одному пользователю, они всё-равно будут отличаться номером клиента)

В разделе Applications создаем клиента,
* выбираем пользователя
* `Client type` указываем *Confidencial*
* `Authorization grant type` указываем *Resource owner password-based*
* сохраняем клиента


Обращение к сервису из клиентского приложения
=============================================

1. Получение токена

Для получения токена нужно выполнить POST-запрос:

  POST /oauth2/token/

:Параметры:

:client_id:
    Тип: строка символов. Идентификатор клиентского приложения

:client_secret:
    Тип: строка символов. Секретный ключ клиентского приложения

:grant_type:
    Тип: строка символов. Тип идентификации клиента. Доступные значения: *password*

:username:
    Тип: строка символов. Имя пользователя, которому выдается токен

:password:
    Тип: строка символов. Пароль пользователя

----

:Результат:
    Тип: application/json.

::

    {
        "access_token": токен для доступа к сервису,
        "token_type": "Bearer",
        "expires_in": время жизни токена в секундах,
        "refresh_token": токен для обновления,
        "scope": "read"
    }


2. Запрос данных

После получения токена его нужно указать в заголовке запроса к сервису:

::
    Authorization: Bearer <токен>


Локальное развертывание сервиса с использованием PyCharm (для разработчиков)
============================================================================

1. Создать отдельный Django-проект с виртуальным окружением (по умолчанию PROJECT_DIR/venv). Здесь и далее PROJECT_DIR - директория PyCharm проекта.

2. Установить пакеты в виртуальное окружение::

    pip install --src PROJECT_DIR -e git+ssh://git@stash.bars-open.ru:7999/m3/m3-gar.git@master#egg=m3_gar
    pip install --src PROJECT_DIR -e git+ssh://git@stash.bars-open.ru:7999/m3/m3-rest-gar.git@master#egg=m3_rest_gar

3. Отметить следующие директории как директории с исходниками (Mark as Sources Root)::

    PROJECT_DIR/m3-gar/m3_gar
    PROJECT_DIR/m3-rest-gar/m3_rest_gar

4. Создать в директории PROJECT_DIR/m3-rest-gar/test_project/test_project файл local_settings.py, скопировать в него содержимое dev_settings.py, подменить настройки, если потребуется.

5. Актуализировать настройки PyCharm. File->Settings->Languages & Frameworks->Django::

    Django project root: PROJECT_DIR/m3-rest-gar/test_project
    Settings: PROJECT_DIR/m3-rest-gar/test_project/test_project/local_settings.py.

6. Запустить Django сервер.

7. В клиентском приложении, которое будет использовать локально развернутый m3-rest-gar, необходимо подменить URL сервиса ГАР на локальный.
