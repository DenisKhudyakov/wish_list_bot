import os
import re

from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile

from bd.crud import (add_gift, delete_gift, get_all_gifts, get_id_gift,
                     reserve_gift)
from bot.keyboard import (cancel_keyboard, get_gifts, main_keyboard,
                          place_keyboard, reserve_and_delete_keyboard)
from config.config import DEFAULT_COMMANDS

router = Router()


@router.message(CommandStart())
async def start(message: types.Message):
    """
    Функция для обработки команды /start
    :param message:
    :return:
    """
    photo_file = FSInputFile(
        path=os.path.join("image", "P1010408-fotor-20241006112425.jpg")
    )
    await message.answer_photo(
        photo=photo_file,
        caption=f"""
    Привет, {message.from_user.full_name}
    Вы приглашены на день рождения Артемия - 02.11.2024
    Бот поможет Вам выбрать подарок или создать его самостоятельно
    Нажмите необходимую команду на клавиатуре чата
    """,
        reply_markup=main_keyboard,
    )


@router.message(F.text == "Инструкция")
async def help(message: types.Message):
    """
    Функция для обработки команды "Инструкция"
    :param message:
    :return:
    """
    text = [f"{commands} - {desk}\n" for commands, desk in DEFAULT_COMMANDS]
    await message.answer("Список команд:" + "\n".join(text))


@router.message(F.text == "Выбрать подарок")
async def get_gift_list(message: types.Message):
    """
    Хендлер с выпадающим списком в виде кнопок
    :param message:
    :return:
    """
    gifts = await get_all_gifts()
    if not gifts:
        await message.answer("Список подарков пуст, добавьте подарки")
    else:
        keyboard = await get_gifts(gifts)
        await message.answer(
            "Выберите подарок для бронирования, "
            "если вы добавили и передумали, то можно удалить",
            reply_markup=keyboard,
        )


class GiftStates(StatesGroup):
    """
    Класс для обработки состояний
    """
    waiting_for_name = State()
    waiting_for_link = State()


@router.message(F.text == "Создать подарок")
async def add_gift_handler(message: types.Message, state: FSMContext):
    """
    Функция для обработки создания подарка
    :param message:
    :param state:
    :return:
    """
    await state.set_state(GiftStates.waiting_for_name)
    await message.answer(
        "Введите название подарка или нажмите 'Отмена' для отмены действия:",
        reply_markup=cancel_keyboard,
    )


@router.message(F.text, GiftStates.waiting_for_name)
async def enter_name(message: types.Message, state: FSMContext):
    """
    Функция для обработки ввода названия подарка
    :param message:
    :param state:
    :return:
    """
    await state.update_data(name=message.text)
    await state.set_state(GiftStates.waiting_for_link)
    await message.answer(
        "Введите ссылку на подарок или нажмите 'Отмена' для отмены действия:",
        reply_markup=cancel_keyboard,
    )


@router.message(F.text, GiftStates.waiting_for_link)
async def enter_link(message: types.Message, state: FSMContext):
    """
    Функция для обработки ввода ссылки на подарок
    :param message:
    :param state:
    :return:
    """
    link = message.text
    pattern = r"^https?:\/\/(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\/\S*)?$"
    if not re.match(pattern, link):
        await message.answer("Некорректная ссылка, повторите попытку")
        return
    user_data = await state.get_data()
    name = user_data["name"]
    await add_gift(name=name, link=link)
    await state.clear()
    await message.answer("Подарок добавлен", reply_markup=main_keyboard)


@router.message(F.text == "Отмена")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Функция для обработки отмены действия
    :param message:
    :param state:
    :return:
    """
    await state.clear()
    await message.answer("Действие отменено", reply_markup=main_keyboard)


@router.callback_query(lambda c: c.data and c.data.startswith("gift_"))
async def process_callback_query(callback_query: types.CallbackQuery):
    """
    После выбора подарка, функция выводит выбор зарезервировать или удалить подарок
    :param callback_query:
    :return:
    """
    gift_id = int(callback_query.data.split("_")[1])
    result = await get_id_gift(gift_id)
    await callback_query.message.edit_text(
        text=f"Желаете удалить или зарезервировать подарок\n{result.link}?",
        reply_markup=await reserve_and_delete_keyboard(gift_id),
    )


@router.callback_query(lambda c: c.data and c.data.startswith("delete_"))
async def delete_gift_handler(callback_query: types.CallbackQuery):
    """
    Функция для обработки удаления подарка
    :param callback_query:
    :return:
    """
    gift_id = int(callback_query.data.split("_")[1])
    await delete_gift(gift_id)
    await callback_query.message.delete()
    await callback_query.message.answer(text="Подарок удален")


@router.callback_query(lambda c: c.data and c.data.startswith("reserve_"))
async def reserve_gift_handler(callback_query: types.CallbackQuery):
    """
    Функция для обработки зарезервирования подарка
    :param callback_query:
    :return:
    """
    gift_id = int(callback_query.data.split("_")[1])
    await reserve_gift(gift_id)
    await callback_query.message.delete()
    await callback_query.message.answer(text="Подарок зарезервирован")


@router.message(F.text == "Время и место мероприятия")
async def time_and_place(message: types.Message):
    """
    Функция для вывода времени и места мероприятия
    :param message:
    :return:
    """
    await message.answer(
        "Мероприятие состоится 02.11.2024 в 16:00, в ТК 'Кольцо'\n 'Всюду чудо парк'",
        reply_markup=place_keyboard,
    )


@router.message(F.text == "Вывести список подарков")
async def get_gift_list(message: types.Message):
    """
    функция для вывода списка подарков
    :param message:
    :return:
    """
    gifts = await get_all_gifts()
    if not gifts:
        await message.answer("Список подарков пуст, добавьте подарки")
    else:
        gifts_list = "\n".join(
            [f"{gift.name} - {gift.link} Статус: {'Зарезервирован' if gift.reserved else 'Свободен для выбора'}" for gift in gifts]
        )
        await message.answer(
            "Список подарков:\n" + gifts_list,
            reply_markup=main_keyboard,
        )
