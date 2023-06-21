from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from data_base import sql_db
from keyboards import start_kb_client, out_kb_client, help_kb_client
from datetime import datetime, timedelta

class FSMClient1(StatesGroup):
    first_criter = State()
    second_criter = State()

class FSMClient2(StatesGroup):
    first_criter = State()
    second_criter = State()

class FSMClient3(StatesGroup):
    first_criter = State()
    second_criter = State()

class FSMClient4(StatesGroup):
    first_criter = State()
    second_criter = State()

class FSMClient5(StatesGroup):
    first_criter = State()
    second_criter = State()

class FSMClient6(StatesGroup):
    first_criter = State()
    second_criter = State()

class FSMClient7(StatesGroup):
    first_criter = State()
    second_criter = State()

class FSMClient8(StatesGroup):
    first_criter = State()
    second_criter = State()

class FSMClient9(StatesGroup):
    first_criter = State()
    second_criter = State()

class FSMInsert(StatesGroup):
    table = State()
    criter = State()

class FSMDelete(StatesGroup):
    table = State()
    condition = State()

class FSMUpdate(StatesGroup):
    table = State()
    set_param = State()
    condition = State()

table = {
    "R1":["Назва компанії","Рік заснування","Директор","Кількість працівників","Кількість офісів", "Тип компанії"],
    "R2":["№_Офісу","Адреса офісу","Кількість персоналу","Дата відкриття","Команда"],
    "R3":["ПІБ працівника","Дата народження","Посада"," Заробітня плата","Проект"],
    "R4":["Назва проекту","Бюджет","Замовник","Дата початку роботи"],
    "R5":["Назва вакансії","Орис","Запропонована плата","Тип зайнятості","Працівник"],
    "R6":["Номер команди","Кількість учасників","Виділений бюджет","Вакансія","Кількість виконаних проектів"],
    "R7":["ПІБ директора","Стаж роботи","Відсоток акцій","Офіс"],
    "R8":["ПІБ компанії","Email","Дата першого замовлення","Кількість замовлень","Країна розташування"]
}

async def comands_start(message : types.Message):
    await bot.send_message(message.from_user.id, 'Початок роботи.', reply_markup=start_kb_client)

async def comand_help(message : types.Message):
    await bot.send_message(message.from_user.id, 'Оберіть довідник.', reply_markup=help_kb_client)

async def help_delete(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(f"При натискані на кнопку <Видалити> вам запропонують обрати відношення для видалення.")
    await callback_query.message.answer(f"Потім у вас запитають що видаляти")
    await callback_query.message.answer(f"Прикладом є відповідь <Назва проекту = RealMan>")

async def help_choose(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(f"При натискані на кнопку <Обрати запит> вам запропонують обрати запит для виведення.")
    await callback_query.message.answer(f"Потім у вас запитають критерії пошуку для запита.")

async def help_insert(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(f"При натискані на кнопку <Додати> вам запропонують обрати відношення для введення в нього нової інформації.")
    await callback_query.message.answer(f"Прикладом є відповідь <RealMan|19023|BlueLake|2023-03-12>")

async def help_update(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(f"При натискані на кнопку <Оновити> вам запропонують обрати відношення для оновлення.")
    await callback_query.message.answer(f"Потім у вас запитають який атрибут оновити та за якими критеріями його відібрати.")
    await callback_query.message.answer(f"Прикладом є відповідь <RealMan|19023|BlueLake|2023-03-12>")


async def choose_for_output(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text='Оберіть запит: ', reply_markup=out_kb_client)

async def choose_for_back(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text='Початок роботи.', reply_markup=start_kb_client)  

async def insert_1(callback_query: types.CallbackQuery):
    await FSMInsert.table.set()
    #await callback_query.message.delete()
    await callback_query.message.answer("Уведіть таблицю для видалення:\nR1-Компанія\nR2-Офіс\nR3-Працівник\nR4-Проект\nR5-Вакансія\nR6-Команда\nR7-Директор\nR8-Замовник")

async def insert_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['table'] = message.text
    await FSMInsert.next()
    await message.answer(f"Відношення: {table[message.text]}")
    await message.answer("Уведіть рядок формату <Перший атрибут|Другий атрибут|Третій атрибут...>, ігноруйте лапки")

async def insert_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['criter'] = message.text
    await FSMInsert.next()
    await sql_db.insert(message, data['table'], data['criter'].split("|"))
    await message.answer("Дані успішно надійшли на сервер")
    await message.answer("Що робимо далі?", reply_markup=start_kb_client)
    await state.finish()

async def delete_1(callback_query: types.CallbackQuery):
    await FSMDelete.table.set()
    #await callback_query.message.delete()
    await callback_query.message.answer("Уведіть таблицю для вставки:\nR1-Компанія\nR2-Офіс\nR3-Працівник\nR4-Проект\nR5-Вакансія\nR6-Команда\nR7-Директор\nR8-Замовник")

async def delete_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['table'] = message.text
    await FSMDelete.next()
    await message.answer(f"Відношення: {table[message.text]}")
    await sql_db.select(message, message.text)
    await message.answer("Уведіть положення для вибору рядка для видалення у форматі <Назва стовпця = Екземпляр>, ігноруйте лапки")
    

async def delete_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['condition'] = message.text
    await FSMDelete.next()
    await sql_db.delete(message, data['table'], data['condition'].split(" = "))
    await message.answer("Дані успішно видалені з серверу")
    await message.answer("Що робимо далі?", reply_markup=start_kb_client)
    await state.finish()


async def update_1(callback_query: types.CallbackQuery):
    await FSMUpdate.table.set()
    #await callback_query.message.delete()
    await callback_query.message.answer("Уведіть таблицю для вставки:\nR1-Компанія\nR2-Офіс\nR3-Працівник\nR4-Проект\nR5-Вакансія\nR6-Команда\nR7-Директор\nR8-Замовник")

async def update_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['table'] = message.text
    await FSMUpdate.next()
    await message.answer(f"Відношення: {table[message.text]}")
    await sql_db.select(message, message.text)
    await message.answer("Уведіть нові значення екземпляру у форматі <Назва стовпця = Екземпляр>, ігноруйте лапки")

async def update_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['set_param'] = message.text
    await FSMUpdate.next()
    await message.answer("Уведіть положення для вибору рядка для оновлення у форматі <Назва стовпця = Екземпляр>, ігноруйте лапки")
    
async def update_4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['condition'] = message.text
    await FSMUpdate.next()
    await sql_db.update(message, data['table'], data['set_param'].split(" = "), data['condition'].split(" = "))
    await message.answer("Дані успішно оновлені на сервері")
    await message.answer("Що робимо далі?", reply_markup=start_kb_client)
    await state.finish()


async def zap1(callback_query: types.CallbackQuery):
    await FSMClient1.first_criter.set()
   # await callback_query.message.delete()
    await sql_db.select(callback_query.message, "R1")
    await callback_query.message.answer("Визначити Компанію (Назва компанії, Рік заснування, Кількість працівників, Кількість офісів) яка має певного директора та певний тип компанії.")
    await callback_query.message.answer("Уведть перший критерій:")

async def load_first1(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_criter'] = message.text
    await FSMClient1.next()
    await message.answer("Уведіть другий критерій")

async def load_second1(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_criter'] = message.text
    await FSMClient1.next()
    try:
        await sql_db.zap1(message, first=data["first_criter"], second=data["second_criter"])
        await message.answer('Що робимо далі?', reply_markup=start_kb_client)
    except:
        await message.answer('Щось пішло не так при загрузі ваших даних на сервер.')
    await state.finish()


async def zap2(callback_query: types.CallbackQuery):
    await FSMClient2.first_criter.set()
    #await callback_query.message.delete()
    await sql_db.select(callback_query.message, "R2")
    await callback_query.message.answer("Визначити Офіс (№ Офісу, Адреса офісу, Кількість персоналу), що був відкритий після певної дати та в якому працює певна команда.")
    await callback_query.message.answer("Уведть перший критерій:")

async def load_first2(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_criter'] = message.text
    await FSMClient2.next()
    await message.answer("Уведіть другий критерій")

async def load_second2(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_criter'] = message.text
    await FSMClient2.next()
    print("da")
    try:
        await sql_db.zap2(message, first=data["first_criter"], second=data["second_criter"])
        await message.answer('Що робимо далі?', reply_markup=start_kb_client)
    except:
        await message.answer('Щось пішло не так при загрузі ваших даних на сервер.')
    await state.finish()

async def zap3(callback_query: types.CallbackQuery):
    await FSMClient3.first_criter.set()
    #await callback_query.message.delete()
    await sql_db.select(callback_query.message, "R3")
    await callback_query.message.answer("Визначити Працівника (ПІБ працівника, Дата народження, Посада), що має певну зарплату та працює над певним проектом.")
    await callback_query.message.answer("Уведть перший критерій:")

async def load_first3(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_criter'] = message.text
    await FSMClient3.next()
    await message.answer("Уведіть другий критерій")

async def load_second3(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_criter'] = message.text
    await FSMClient3.next()
    try:
        await sql_db.zap3(message, first=data["first_criter"], second=data["second_criter"])
        await message.answer('Що робимо далі?', reply_markup=start_kb_client)
    except:
        await message.answer('Щось пішло не так при загрузі ваших даних на сервер.')
    await state.finish()

async def zap4(callback_query: types.CallbackQuery):
    await FSMClient4.first_criter.set()
    #await callback_query.message.delete()
    await sql_db.select(callback_query.message, "R4")
    await callback_query.message.answer("Визначити Проект (Назва проекту, Кількість працівників, Бюджет), що має певного замовника, та робота над яким почалась після певної дати. ")
    await callback_query.message.answer("Уведть перший критерій:")

async def load_first4(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_criter'] = message.text
    await FSMClient4.next()
    await message.answer("Уведіть другий критерій")

async def load_second4(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_criter'] = message.text
    await FSMClient4.next()
    try:
        await sql_db.zap4(message, first=data["first_criter"], second=data["second_criter"])
        await message.answer('Що робимо далі?', reply_markup=start_kb_client)
    except:
        await message.answer('Щось пішло не так при загрузі ваших даних на сервер.')
    await state.finish()

async def zap5(callback_query: types.CallbackQuery):
    await FSMClient5.first_criter.set()
    #await callback_query.message.delete()
    await sql_db.select(callback_query.message, "R5")
    await callback_query.message.answer("Визначити Вакансію (Назва вакансії, Опис, Запропонована зарплата, Тип зайнятості) на яку відгукнувся певний працівник, з певним рангом шуканого спеціаліста.")
    await callback_query.message.answer("Уведть перший критерій:")

async def load_first5(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_criter'] = message.text
    await FSMClient5.next()
    await message.answer("Уведіть другий критерій")

async def load_second5(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_criter'] = message.text
    await FSMClient5.next()
    try:
        await sql_db.zap5(message, first=data["first_criter"], second=data["second_criter"])
        await message.answer('Що робимо далі?', reply_markup=start_kb_client)
    except:
        await message.answer('Щось пішло не так при загрузі ваших даних на сервер.')
    await state.finish()

async def zap6(callback_query: types.CallbackQuery):
    await FSMClient6.first_criter.set()
    #await callback_query.message.delete()
    await sql_db.select(callback_query.message, "R6")
    await callback_query.message.answer("Визначити Команду (Номер команди, Кількість учасників, виділений бюджет), що створила певну вакансію та кількість виконаних проектів.")
    await callback_query.message.answer("Уведть перший критерій:")

async def load_first6(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_criter'] = message.text
    await FSMClient6.next()
    await message.answer("Уведіть другий критерій")

async def load_second6(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_criter'] = message.text
    await FSMClient6.next()
    try:
        await sql_db.zap6(message, first=data["first_criter"], second=data["second_criter"])
        await message.answer('Що робимо далі?', reply_markup=start_kb_client)
    except:
        await message.answer('Щось пішло не так при загрузі ваших даних на сервер.')
    await state.finish()


async def zap7(callback_query: types.CallbackQuery):
    await FSMClient7.first_criter.set()
    await callback_query.message.delete()
    await sql_db.select(callback_query.message, "R7")
    await callback_query.message.answer("Визначити Директора (ПІБ директора, Заробітня плата, Стаж роботи), що має певний Відсоток акцій, та працює в певному офісі.")
    await callback_query.message.answer("Уведть перший критерій:")

async def load_first7(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_criter'] = message.text
    await FSMClient7.next()
    await message.answer("Уведіть другий критерій")

async def load_second7(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_criter'] = message.text
    await FSMClient7.next()
    try:
        await sql_db.zap7(message, first=data["first_criter"], second=data["second_criter"])
        await message.answer('Що робимо далі?', reply_markup=start_kb_client)
    except:
        await message.answer('Щось пішло не так при загрузі ваших даних на сервер.')
    await state.finish()

async def zap8(callback_query: types.CallbackQuery):
    await FSMClient8.first_criter.set()
    #await callback_query.message.delete()
    await sql_db.select(callback_query.message, "R8")
    await callback_query.message.answer("Визначити Замовника (ПІБ замовника, Email, Дата першого замовлення), що має певну кількість замовлень та певну країну розташування.")
    await callback_query.message.answer("Уведть перший критерій:")

async def load_first8(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_criter'] = message.text
    await FSMClient8.next()
    await message.answer("Уведіть другий критерій")

async def load_second8(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_criter'] = message.text
    await FSMClient8.next()
    try:
        await sql_db.zap8(message, first=data["first_criter"], second=data["second_criter"])
        await message.answer('Що робимо далі?', reply_markup=start_kb_client)
    except:
        await message.answer('Щось пішло не так при загрузі ваших даних на сервер.')
    await state.finish()

async def zap9(callback_query: types.CallbackQuery):
    await FSMClient9.first_criter.set()
    #await callback_query.message.delete()
    await callback_query.message.answer("R3")
    await sql_db.select(callback_query.message, "R3")
    await callback_query.message.answer("R6")
    await sql_db.select(callback_query.message, "R6")
    await callback_query.message.answer("Визначити Вакансію (Назва вакансії, Опис, Запропонована плата, Тип занятості), певної команди, при виконані заданого проекту.")
    await callback_query.message.answer("Уведть номер команди:")

async def load_first9(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_criter'] = message.text
    await FSMClient9.next()
    await message.answer("Уведіть назву проекту")

async def load_second9(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_criter'] = message.text
    await FSMClient9.next()
    try:
        await sql_db.zap9(message, first=data["first_criter"], second=data["second_criter"])
        await message.answer('Що робимо далі?', reply_markup=start_kb_client)
    except:
        await message.answer('Щось пішло не так при загрузі ваших даних на сервер.')
    await state.finish()



async def cancel_hand(message : types.Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state is None:
        return 
    await state.finish()
    await message.reply('OK')



def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(comands_start, commands=['start'])
    dp.register_message_handler(comand_help, commands=['help'])

    dp.register_callback_query_handler(choose_for_output, text="Обрати")
    dp.register_callback_query_handler(choose_for_back, text="Назад")

    dp.register_callback_query_handler(help_choose, text="hОбрати")
    dp.register_callback_query_handler(help_delete, text="hВидалити")
    dp.register_callback_query_handler(help_insert, text="hДодати")
    dp.register_callback_query_handler(help_update, text="hОновити")


    #1
    dp.register_callback_query_handler(zap1, text="zap1", state=None)
    dp.register_message_handler(load_first1, state=FSMClient1.first_criter)
    dp.register_message_handler(load_second1, state=FSMClient1.second_criter)

    #2
    dp.register_callback_query_handler(zap2, text="zap2", state=None)
    dp.register_message_handler(load_first2, state=FSMClient2.first_criter)
    dp.register_message_handler(load_second2, state=FSMClient2.second_criter)
    
    #3
    dp.register_callback_query_handler(zap3, text="zap3", state=None)
    dp.register_message_handler(load_first3, state=FSMClient3.first_criter)
    dp.register_message_handler(load_second3, state=FSMClient3.second_criter)

    #4
    dp.register_callback_query_handler(zap4, text="zap4", state=None)
    dp.register_message_handler(load_first4, state=FSMClient4.first_criter)
    dp.register_message_handler(load_second4, state=FSMClient4.second_criter)

    #5
    dp.register_callback_query_handler(zap5, text="zap5", state=None)
    dp.register_message_handler(load_first5, state=FSMClient5.first_criter)
    dp.register_message_handler(load_second5, state=FSMClient5.second_criter)

    #6
    dp.register_callback_query_handler(zap6, text="zap6", state=None)
    dp.register_message_handler(load_first6, state=FSMClient6.first_criter)
    dp.register_message_handler(load_second6, state=FSMClient6.second_criter)

    #7
    dp.register_callback_query_handler(zap7, text="zap7", state=None)
    dp.register_message_handler(load_first7, state=FSMClient7.first_criter)
    dp.register_message_handler(load_second7, state=FSMClient7.second_criter)
    
    #8
    dp.register_callback_query_handler(zap8, text="zap8", state=None)
    dp.register_message_handler(load_first8, state=FSMClient8.first_criter)
    dp.register_message_handler(load_second8, state=FSMClient8.second_criter)

    #9
    dp.register_callback_query_handler(zap9, text="zap9", state=None)
    dp.register_message_handler(load_first9, state=FSMClient9.first_criter)
    dp.register_message_handler(load_second9, state=FSMClient9.second_criter)

    #insert
    dp.register_callback_query_handler(insert_1, text="Додати", state=None)
    dp.register_message_handler(insert_2, state=FSMInsert.table)
    dp.register_message_handler(insert_3, state=FSMInsert.criter)

    #delete
    dp.register_callback_query_handler(delete_1, text="Видалити", state=None)
    dp.register_message_handler(delete_2, state=FSMDelete.table)
    dp.register_message_handler(delete_3, state=FSMDelete.condition)

    #update
    dp.register_callback_query_handler(update_1, text="Оновити", state=None)
    dp.register_message_handler(update_2, state=FSMUpdate.table)
    dp.register_message_handler(update_3, state=FSMUpdate.set_param)
    dp.register_message_handler(update_4, state=FSMUpdate.condition)
    

    dp.register_message_handler(cancel_hand, state="*", commands='відміна')
    dp.register_message_handler(cancel_hand, Text(equals='відміна', ignore_case='True'), state='*')