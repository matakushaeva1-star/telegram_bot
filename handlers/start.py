"""
команды для бота-анкеты
/start - начинает заполнение анкеты
/cancel - отменяет активный диалог
/help - показывает справочную информацию
"""
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from states import ProfileForm

router = Router(name=__name__)

@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    """
    Запускает анкету по команде /start
    ***перед этим очищаем старые данные машины состояний FSM
    """
    await state.clear()
    await state.set_state(ProfileForm.last_name)
    await message.answer("Привет! Заполни небольшую анкетую \n\nВведите фамилию:", reply_markup=ReplyKeyboardRemove())

@router.message(Command("cancel"))
async def command_cancel(message: Message, state: FSMContext):
    """
    Отменяет заполнение анкеты по команда /cancel"""
    # Получаем текушее состояние пользователя
    # Если состояния нет, значит пользователь не заполнил анкету
    current_state = await state.get_state()
    if current_state is None:
        await  message.answer("Сейчас нет активной анкеты! Нажмите /start чтобы начать")
        return
    await state.clear()
    await message.answer("Анкета отменена! Нажмите /start чтобы начать заново", reply_markup=ReplyKeyboardRemove())

@router.message(Command("help"))
async def command_help(message: Message):
    """
    Показывает справочную информацию по команде /help
    Без сброса текущего состояния FSM
        (без state: FSMContext в аргументах функции только тогда,
        когда собираемся совершить действие с памятью бота
        т.е. записать данные, изменить шаг или очистить всё.
        Для простого ответа текстом этот инструмент не нужен.)
    """
    help_text = (
        "<b> Справочное сообщение:</b>\n\n"
        "/start — Начать заполнение анкеты с самого начала (старые данные сотрутся)\n"
        "/cancel — Полностью отменить заполнение текущей анкеты\n"
        "/help — Показать справочное сообщение\n\n"
        "Вернитесь к заполнению анкеты, для этого отправьте ответ на последний вопрос, на котором Вы остановились."
    )
    await message.answer(help_text)
