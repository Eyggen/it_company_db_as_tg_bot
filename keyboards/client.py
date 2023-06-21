from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

b_delete = InlineKeyboardButton(text = 'Видалити🗑️', callback_data="Видалити")
b_insert = InlineKeyboardButton(text = 'Додати🖊️', callback_data="Додати")
b_update = InlineKeyboardButton(text = 'Оновити📋', callback_data="Оновити")
b_choose = InlineKeyboardButton(text = 'Обрати запит📚', callback_data="Обрати")

b_help_delete = InlineKeyboardButton(text = 'Видалити🗑️', callback_data="hВидалити")
b_help_insert = InlineKeyboardButton(text = 'Додати🖊️', callback_data="hДодати")
b_help_update = InlineKeyboardButton(text = 'Оновити📋', callback_data="hОновити")
b_help_choose = InlineKeyboardButton(text = 'Обрати запит📚', callback_data="hОбрати")

b_help_delete


b_zap1 = InlineKeyboardButton(text = '1️⃣', callback_data="zap1")
b_zap2 = InlineKeyboardButton(text = '2️⃣', callback_data="zap2")
b_zap3 = InlineKeyboardButton(text = '3️⃣', callback_data="zap3")
b_zap4 = InlineKeyboardButton(text = '4️⃣', callback_data="zap4")
b_zap5 = InlineKeyboardButton(text = '5️⃣', callback_data="zap5")
b_zap6 = InlineKeyboardButton(text = '6️⃣', callback_data="zap6")
b_zap7 = InlineKeyboardButton(text = '7️⃣', callback_data="zap7")
b_zap8 = InlineKeyboardButton(text = '8️⃣', callback_data="zap8")
b_zap9 = InlineKeyboardButton(text = '9️⃣', callback_data="zap9")
b_back = InlineKeyboardButton(text = 'Повернутись назад', callback_data="Назад")

start_kb_client = InlineKeyboardMarkup(row_width=2)
help_kb_client = InlineKeyboardMarkup(row_width=2)
out_kb_client =InlineKeyboardMarkup(row_width=4)

start_kb_client.add(b_choose, b_insert, b_update, b_delete)
help_kb_client.add(b_help_choose, b_help_insert, b_help_update, b_help_delete)
out_kb_client.add(b_zap1, b_zap2, b_zap3, b_zap4, b_zap5, b_zap6, b_zap7, b_zap8, b_zap9, b_back)