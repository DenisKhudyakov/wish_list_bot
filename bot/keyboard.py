from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Выбрать подарок"),
            KeyboardButton(text="Создать подарок"),
        ],
        [
            KeyboardButton(text="Вывести список подарков"),
            KeyboardButton(text="Время и место мероприятия"),
        ],
        [KeyboardButton(text="Инструкция")],
    ],
    resize_keyboard=True,
)


async def reserve_and_delete_keyboard(gift_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Зарезервировать подарок", callback_data=f"reserve_{gift_id}"
                ),
                InlineKeyboardButton(text="Удалить", callback_data=f"delete_{gift_id}"),
            ],
        ]
    )
    return keyboard


cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отмена")],
    ],
    resize_keyboard=True,
)


async def get_gifts(gifts):
    keyboard = InlineKeyboardBuilder()
    for gift in gifts:
        text = f"{gift.id}. {gift.name}\n {'Зарезервирован' if gift.reserved else 'Не зарезервирован'}"
        button = InlineKeyboardButton(text=text, callback_data=f"gift_{gift.id}")
        keyboard.add(button)
    return keyboard.adjust(1).as_markup()


place_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ссылка на заведение", url="https://vchudopark.ru/")]
    ]
)

cancel_place_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="cancel")]]
)
