import numpy as np
from aiogram.utils.keyboard import InlineKeyboardBuilder

DAYS = ["Monday (月)",
        "Tuesday (火)", 
        "Wednesday (水)", 
        "Thursday (木)", 
        "Friday (金)"]

PAIRS = ["1st Pair (8:45 - 10:15)", 
         "2nd Pair (10:30 - 12:00)", 
         "3rd Pair (13:15 - 14:45)", 
         "4th Pair (15:00 - 16:30)", 
         "5th Pair (16:45 - 18:15)"]

users_db = {}


def get_user_matrix(user_id: int) -> np.ndarray:
    if user_id not in users_db:
        users_db[user_id] = {
            "name": "Student",
            "matrix": np.zeros((5, 5), dtype=int)
        }
    return users_db[user_id]["matrix"]


def build_days_keyboard():
    builder = InlineKeyboardBuilder()
    for d_idx, day in enumerate(DAYS):
        builder.button(
            text=day, 
            callback_data=f"day_{d_idx}"
        )
    builder.adjust(1)
    return builder.as_markup()


def build_pairs_keyboard(user_id: int, d_idx: int):
    matrix = get_user_matrix(user_id)
    builder = InlineKeyboardBuilder()

    for p_idx, pair_time in enumerate(PAIRS):
        is_busy = matrix[d_idx, p_idx]
        status = "🔴" if is_busy == 1 else "🟢"

        btn_text = f"{pair_time} {status}"

        builder.button(
            text=btn_text,
            callback_data=f"toggle_{d_idx}_{p_idx}"
        )

    builder.button(text="⬅️ Back to days", callback_data="back_to_days")
    builder.adjust(1)
    return builder.as_markup()

