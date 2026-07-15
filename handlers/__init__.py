""" Сбор всех роутеров бота-анкеты
В каждом файле папки handler оздается свой роутер
Здесь импортируем эти файлы и возвращаем роутеры одной функцией,
чтобы в main.py ожно было подключить одной строкой
"""

from aiogram import Router
from . import form, start # . обозначает что импортируется из текущей дириктории


def get_routers() -> tuple[Router, ...]:
    return (start.router, form.router)



