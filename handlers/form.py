from aiogram import F, Router, html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import ProfileForm

router = Router(name=__name__)


# Получение и обработка фамилии

"""
Каждый хэндлер состоит из двух частей:
1. Декоратор (условие) — говорит боту, какое именно действие нужно поймать 
(например: «если пришел текст», «если нажали команду /help», «если мы ждем фамилию»).
2. Асинхронная функция (действие) — логика, которая выполняется, когда условие совпало 
(например: сохранить данные, отправить ответ).
"""

@router.message(ProfileForm.last_name, F.text) # 1. УСЛОВИЕ: Ловим текстовое сообщение, когда бот ждет ИМЯ
async def process_lastname(message: Message, state: FSMContext):# 2. ДЕЙСТВИЕ: Функция, которая обрабатывает это имя
    last_name = message.text
    if len(last_name) < 2:
        await message.answer("Фамилия слишком короткая. Введите фамилию еще раз")
        return
    # должны сохранить фамилию во временное хранилище FSM(хранится в оперативной памяти)
    await state.update_data(last_name=last_name)
    # переключить пользователя на следующий шаг ввод имени
    await state.set_state(ProfileForm.first_name)
    await message.answer("Введите имя: ")


# Получение и обработка имени
@router.message(ProfileForm.first_name, F.text)
async def process_first_name(message: Message, state: FSMContext):
    first_name = message.text
    if len(first_name) < 2:
        await message.answer("Имя слишком короткая. Введите имя еще раз")
        return
    # должны сохранить имя во временное хранилище FSM(хранится в оперативной памяти)
    await state.update_data(first_name=first_name)
    # переключить пользователя на следующий шаг ввод имени
    await state.set_state(ProfileForm.city)
    await message.answer("Введите город: ")


# Получение и обработка города
@router.message(ProfileForm.city, F.text)
async def process_city(message: Message, state: FSMContext):
    city = message.text
    if len(city) < 2:
        await message.answer("Название города слишком короткае. Введите город еще раз")
        return
    # должны сохранить имя во временное хранилище FSM(хранится в оперативной памяти)
    await state.update_data(city=city)
    # переключить пользователя на следующий шаг ввод телефона
    await state.set_state(ProfileForm.phone)
    await message.answer("Введите номер телефона: ")




# Получение и обработка номера телефона
@router.message(ProfileForm.phone, F.text)
async def process_phone(message: Message, state: FSMContext):
    phone = message.text
    if len(phone) < 11:
        await message.answer("Введите номер в формате +7-911-111-11-11")
        return
    # сохранить номер во временном хранилище
    data = await state.update_data(phone=phone)

    # очищение FSM (очистить машину состояния)
    await state.clear()

    profile_text = (
        "<b>Ваша анкета:</b>"
        f"<b>Фамилия:</b> {html.quote(data['last_name'])}\n"
        f"<b>Имя:</b> {html.quote(data['first_name'])}\n"
        f"<b>Город:</b> {html.quote(data['city'])}\n"
        f"<b>Телефон:</b> {html.quote(data['phone'])}\n"
        "Чтобы заполнить анкету заново - нажмите /start"
    )
    await message.answer(profile_text)


@router.message(ProfileForm.last_name)
@router.message(ProfileForm.first_name)
@router.message(ProfileForm.city)
@router.message(ProfileForm.phone)
async def process_not_text(message: Message):
    await message.answer("Пожалуйста, отправьте текст сообщения")



