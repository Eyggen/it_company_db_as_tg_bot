import sqlite3 as sq
import re
from datetime import datetime
from create_bot import bot
import string

r = re.compile('[^a-zA-Z]')

def check(param):
    if re.search(r'\d{4}-\d{2}-\d{2}', param):
        #print(0)
        param = str(param)
    elif (re.search(r'[1-9]', param) or re.search(r'-[1-9]', param)) and not re.search(r'\d', param):
        #print(1)
        param = int(param)
    elif (re.search(r'[1-9]*[.]?[1-9]', param) or re.search(r'-[1-9]*[.]?[1-9]', param)) and not re.search(r'\d', param):
        #print(2)
        param = float(param)
    else:
        #print(3)
        param = str(param)
    return param

def sql_start():
    global r
    global base, cur
    try:
        base = sq.connect('It_company.db')
        cur = base.cursor()
        if base:
            print("Succsed")
    except Exception as ex:
        print("nadazdelac")
        print(ex)

async def sql_add_table():
    try:
        base.execute("CREATE TABLE IF NOT EXISTS R1([Назва компанії] TEXT, [Рік заснування] INTEGER, [Директор] TEXT, [Кількість працівників] INTEGER, [Кількість офісів] INTEGER, [Тип компанії] TEXT, PRIMARY KEY([Назва компанії],[Кількість офісів]));")
        base.execute("CREATE TABLE IF NOT EXISTS R2([№_Офісу] INTEGER,[Адреса офісу] TEXT,[Кількість персоналу] INTEGER,[Дата відкриття] TEXT,[Команда] INTEGER,PRIMARY KEY([№_Офісу],[Адреса офісу]));")
        base.execute("CREATE TABLE IF NOT EXISTS R3([ПІБ працівника] TEXT,[Дата народження] TEXT,[Посада] TEXT,[Заробітня плата] REAL,[Проект] TEXT,PRIMARY KEY([ПІБ працівника],[Дата народження]));")
        base.execute("CREATE TABLE IF NOT EXISTS R4([Назва проекту] TEXT,[Бюджет] REAL,[Замовник] TEXT,[Дата початку роботи] TEXT,PRIMARY KEY([Назва проекту],[Дата початку роботи]));")
        base.execute("CREATE TABLE IF NOT EXISTS R5([Назва вакансії] TEXT,[Опис] TEXT,[Запропонована плата] REAL,[Тип занятості] TEXT,[Працівник] TEXT,[Ранг шуканого спеціаліста] TEXT,PRIMARY KEY([Працівник],[Назва вакансії]));")
        base.execute("CREATE TABLE IF NOT EXISTS R6([Номер команди] INTEGER,[Кількість учасників] INTEGER,[Виділений бюджет] REAL,[Вакансія] TEXT,[Кількість виконаних проектів] INTEGER,PRIMARY KEY([Номер команди],[Виділений бюджет]));")
        base.execute("CREATE TABLE IF NOT EXISTS R7([ПІБ директора] TEXT,[Стаж роботи] INTEGER,[Відсоток акцій] REAL,[Офіс] INTEGER,PRIMARY KEY([ПІБ директора],[Відсоток акцій]));")
        base.execute("CREATE TABLE IF NOT EXISTS R8([ПІБ замовника] TEXT,[Email] TEXT,[Дата першого замовлення] TEXT,[Кількість замовлень] INTEGER,[Країна розташування] TEXT,PRIMARY KEY([ПІБ замовника],[Email]));")
        base.commit()
    except Exception as ex:
        print("nadazdelac")
        print(ex) 

async def sql_add_row(user, obj, price, description):
    try:
        now = datetime.now()
        dt_string_data = now.strftime("%Y-%m-%d")
        dt_string_time = now.strftime("%H:%M:%S")
        cur.execute('INSERT INTO ' + user + ' VALUES (?,?,?,?,?)', (obj,price,description,dt_string_time,dt_string_data))
        base.commit()
    except Exception as ex:
        print("nadazdelac v db")
        print(ex)


async def return_data_from_db_by_callback(callback, date):
    user = 'U'+str(callback.from_user.id)
    try:
        data = cur.execute("SELECT * FROM " + user + " WHERE data == '" + str(date) + "'").fetchall()
        if len(data) == 0:
            await callback.message.answer('У вас немає записів за цю дату')
        else:
            for row in data:
                await callback.message.answer(f'Object: {row[0]}\nPrice: {row[1]}\nDecription: {row[2]}\nTime: {row[3]}, Data: {row[4]}')
    except:
        await callback.answer('Шось пішло не так, перевірте правильність написання дати.')
            
async def return_data_from_db_by_message(message):
    user = 'U'+str(message.from_user.id)
    try:
        data = cur.execute("SELECT * FROM " + user + " WHERE data == '" + str(message.text) + "'").fetchall()
        if len(data) == 0:
            await bot.send_message(message.from_user.id, 'У вас немає записів за цю дату')
        else:
            for row in data:
                await bot.send_message(message.from_user.id, f'Object: {row[0]}\nPrice: {row[1]}\nDecription: {row[2]}\nTime: {row[3]}, Data: {row[4]}')
    except:
        await bot.send_message(message.from_user.id, 'Шось пішло не так, перевірте правильність написання дати.')

async def zap1(message, first, second):
    try:
        data = cur.execute(f"SELECT [Назва компанії],[Рік заснування],[Кількість працівників],[Кількість офісів] FROM R1 WHERE R1.Директор = ? AND R1.[Тип компанії] = ?", (first, second)).fetchall()
        print(data)
        print([first,second, "zap1"])
        if len(data) == 0:
            await bot.send_message(message.from_user.id, 'Немає таких записів')
        else:
            for row in data:
                await bot.send_message(message.from_user.id, f"Назва компанії: {row[0]}\nРік заснування: {row[1]}\nКількість працівників: {row[2]}\nКількість офісів: {row[3]}")
    except Exception as ex:
        await bot.send_message(message.from_user.id, f"{ex}")


async def zap2(message, first, second):
    try:
        data = cur.execute(f"SELECT [№_Офісу],[Адреса офісу],[Кількість персоналу] FROM R2 WHERE R2.[Команда] = ? AND R2.[Дата відкриття] = ?", (int(first), second)).fetchall()
        print(data)
        print([first,second, "zap2"])
        if len(data) == 0:
            await bot.send_message(message.from_user.id, 'Немає таких записів')
        else:
            for row in data:
                await bot.send_message(message.from_user.id, f"№_Офісу: {row[0]}\nАдреса офісу: {row[1]}\nКількість персоналу: {row[2]}")
    except Exception as ex:
        await bot.send_message(message.from_user.id, f"{ex}")

async def zap3(message, first, second):
    try:
        data = cur.execute(f"SELECT [ПІБ працівника],[Дата народження],[Посада] FROM R3 WHERE R3.[Заробітня плата] = ? AND R3.[Проект] = ?", (float(first), second)).fetchall()
        print(data)
        print([first,second, "zap3"])
        if len(data) == 0:
            await bot.send_message(message.from_user.id, 'Немає таких записів')
        else:
            for row in data:
                await bot.send_message(message.from_user.id, f"ПІБ працівника: {row[0]}\nДата народження: {row[1]}\nПосада: {row[2]}")
    except Exception as ex:
        await bot.send_message(message.from_user.id, f"{ex}")

async def zap4(message, first, second):
    try:
        data = cur.execute(f"SELECT [Назва проекту], [Кількість працівників], [Бюджет] FROM R4 LEFT JOIN R3 ON R4.[Назва проекту] = R3.[Проект] LEFT JOIN R5 ON R3.[ПІБ працівника] = R5.[Працівник] LEFT JOIN R6 ON R5.[Назва вакансії] = R6.[Вакансія] LEFT JOIN R2 ON R6.[Номер команди] = R2.[Команда] LEFT JOIN R7 ON R2.[№_Офісу] = R7.[Офіс] LEFT JOIN R1 ON R7.[ПІБ директора] = R1.[Директор] WHERE R4.[Замовник] = ? AND R4.[Дата початку роботи] = ?", (first, second)).fetchall()
        print(data)
        print([first,second, "zap4"])
        if len(data) == 0:
            await bot.send_message(message.from_user.id, 'Немає таких записів')
        else:
            for row in data:
                await bot.send_message(message.from_user.id, f"Назва проекту: {row[0]}\nКількість працівників: {row[1]}\nБюджет: {row[2]}")
    except Exception as ex:
        await bot.send_message(message.from_user.id, f"{ex}")

async def zap5(message, first, second):
    try:
        data = cur.execute(f"SELECT [Назва вакансії],[Опис],[Запропонована плата],[Тип занятості] FROM R5 WHERE R5.[Працівник] = ? AND R5.[Ранг шуканого спеціаліста] = ?", (first, second)).fetchall()
        print(data)
        print([first,second, "zap5"])
        if len(data) == 0:
            await bot.send_message(message.from_user.id, 'Немає таких записів')
        else:
            for row in data:
                await bot.send_message(message.from_user.id, f"Назва вакансії: {row[0]}\nОпис: {row[1]}\nЗапропонована плата: {row[2]}\nТип занятості: {row[3]}")
    except Exception as ex:
        await bot.send_message(message.from_user.id, f"{ex}")

async def zap6(message, first, second):
    try:
        data = cur.execute(f"SELECT [Номер команди],[Кількість учасників],[Виділений бюджет] FROM R6 WHERE R6.[Вакансія] = ? AND R6.[Кількість виконаних проектів] = ?", (first, int(second))).fetchall()
        print(data)
        print([first,second, "zap6"])
        if len(data) == 0:
            await bot.send_message(message.from_user.id, 'Немає таких записів')
        else:
            for row in data:
                await bot.send_message(message.from_user.id, f"Номер команди: {row[0]}\nКількість учасників: {row[1]}\nВиділений бюджет: {row[2]}")
    except Exception as ex:
        await bot.send_message(message.from_user.id, f"{ex}")

async def zap7(message, first, second):
    try:
        data = cur.execute(f"SELECT [ПІБ директора],[Заробітня плата],[Стаж роботи] FROM R7 LEFT JOIN R3 ON R7.[ПІБ директора] = R3.[ПІБ працівника] WHERE R7.[Відсоток акцій] = ? AND R7.[Офіс] = ?", (float(first), int(second))).fetchall()
        print(data)
        print([first,second, "zap7"])
        if len(data) == 0:
            await bot.send_message(message.from_user.id, 'Немає таких записів')
        else:
            for row in data:
                await bot.send_message(message.from_user.id, f"ПІБ директора: {row[0]}\nЗаробітня плата: {row[1]}\nСтаж роботи: {row[2]}")
    except Exception as ex:
        await bot.send_message(message.from_user.id, f"{ex}")

async def zap8(message, first, second):
    try:
        data = cur.execute(f"SELECT [ПІБ замовника],[Email],[Дата першого замовлення] FROM R8 WHERE R8.[Кількість замовлень] = ? AND R8.[Країна розташування] = ?", (int(first), second)).fetchall()
        print(data)
        print([first,second, "zap8"])
        if len(data) == 0:
            await bot.send_message(message.from_user.id, 'Немає таких записів')
        else:
            for row in data:
                await bot.send_message(message.from_user.id, f"ПІБ замовника: {row[0]}\nEmail: {row[1]}\nДата першого замовлення: {row[2]}")
    except Exception as ex:
        await bot.send_message(message.from_user.id, f"{ex}")


async def insert(message, table, criter):
    try:
        if table == "R1":
            cur.execute(f"INSERT INTO R1 VALUES(?,?,?,?,?,?)", (str(criter[0]), int(criter[1]), str(criter[2]), int(criter[3]), int(criter[4]), str(criter[5])))
            #await bot.send_message(message.from_user.id, f"Table: {table}\n1: {criter[0]}\n2: {criter[1]}\n3: {criter[2]}\n4: {criter[3]}\n5: {criter[4]}\n6: {criter[5]}") 
            base.commit()
        elif table == "R2":
            cur.execute(f"INSERT INTO R2 VALUES (?,?,?,?,?)", (int(criter[0]), str(criter[1]), int(criter[2]), str(criter[3]), int(criter[4])))
            #await bot.send_message(message.from_user.id, f"Table: {table}\n1: {criter[0]}\n2: {criter[1]}\n3: {criter[2]}\n4: {criter[3]}\n5: {criter[4]}")
            base.commit()
        elif table == "R3":
            cur.execute(f"INSERT INTO R3 VALUES (?,?,?,?,?)", (str(criter[0]), str(criter[1]), str(criter[2]), float(criter[3]), str(criter[4])))
            #await bot.send_message(message.from_user.id, f"Table: {table}\n1: {criter[0]}\n2: {criter[1]}\n3: {criter[2]}\n4: {criter[3]}\n5: {criter[4]}")
            base.commit()
        elif table == "R4":
            print(f"Table: {table}\n1: {criter[0]}\n2: {criter[1]}\n3: {criter[2]}\n4: {criter[3]}")
            cur.execute('INSERT INTO R4 VALUES (?,?,?,?)', (str(criter[0]), float(criter[1]), str(criter[2]), str(criter[3])))
            base.commit()
            #await bot.send_message(message.from_user.id, f"Table: {table}\n1: {criter[0]}\n2: {criter[1]}\n3: {criter[2]}\n4: {criter[3]}")
        elif table == "R5":
            cur.execute(f"INSERT INTO R5 VALUES (?,?,?,?,?,?)", (str(criter[0]), str(criter[1]), float(criter[2]), str(criter[3]), str(criter[4]), str(criter[5])))
            #await bot.send_message(message.from_user.id, f"Table: {table}\n1: {criter[0]}\n2: {criter[1]}\n3: {criter[2]}\n4: {criter[3]}\n5: {criter[4]}\n6: {criter[5]}")
            base.commit()
        elif table == "R6":
            cur.execute(f"INSERT INTO R6 VALUES (?,?,?,?,?)", (int(criter[0]), int(criter[1]), float(criter[2]), str(criter[3]), int(criter[4])))
            #await bot.send_message(message.from_user.id, f"Table: {table}\n1: {criter[0]}\n2: {criter[1]}\n3: {criter[2]}\n4: {criter[3]}\n5: {criter[4]}")
            base.commit()
        elif table == "R7":
            cur.execute(f"INSERT INTO R7 VALUES (?,?,?,?)", (str(criter[0]), int(criter[1]), float(criter[2]), int(criter[3])))
            #await bot.send_message(message.from_user.id, f"Table: {table}\n1: {criter[0]}\n2: {criter[1]}\n3: {criter[2]}\n4: {criter[3]}")
            base.commit()
        else:
            cur.execute(f"INSERT INTO R8 VALUES (?,?,?,?,?)", (str(criter[0]), str(criter[1]), str(criter[2]), int(criter[3]), str(criter[4])))
            #await bot.send_message(message.from_user.id, f"Table: {table}\n1: {criter[0]}\n2: {criter[1]}\n3: {criter[2]}\n4: {criter[3]}\n5: {criter[4]}")
            base.commit()
        
    except Exception as ex:
        await bot.send_message(message.from_user.id, ex)
    
async def delete(message, table, condition):
    try:
        #if re.search(r'[1-9]', condition[1]) or re.search(r'-[1-9]', condition[1]):
        #    print(1)
        #    condition[1] = int(condition[1])
        #elif re.search(r'[1-9]*[.]?[1-9]', condition[1]) or re.search(r'-[1-9]*[.]?[1-9]', condition[1]):
        #    print(2)
        #    condition[1] = float(condition[1])
        #else:
        #    print(3)
        #    condition[1] = str(condition[1])
        print("DELETE FROM " + table + " WHERE " + table + f".[{condition[0]}] = {condition[1]}")
        cur.execute("DELETE FROM " + table + " WHERE " + table + f".[{condition[0]}] = ?", (check(condition[1]),))
        base.commit()
    except Exception as ex:
        await bot.send_message(message.from_user.id, ex)



async def update(message, table, param, condition):
    try:
        print("UPDATE " + table +  " SET " + table + f".[{param[0]}] = {param[1]} WHERE " + table + f".[{condition[0]}] = {condition[1]}")
        cur.execute("UPDATE " + table +  " SET " + f"[{param[0]}] = ? WHERE " + table + f".[{condition[0]}] = ?", (check(param[1]), check(condition[1])))
        base.commit()
    except Exception as ex:
        await bot.send_message(message.from_user.id, ex)

async def select(message, table):
    table_rows = {
        "R1":["Назва компанії","Рік заснування","Директор","Кількість працівників","Кількість офісів", "Тип компанії"],
        "R2":["№_Офісу","Адреса офісу","Кількість персоналу","Дата відкриття","Команда"],
        "R3":["ПІБ працівника","Дата народження","Посада"," Заробітня плата","Проект"],
        "R4":["Назва проекту","Бюджет","Замовник","Дата початку роботи"],
        "R5":["Назва вакансії","Орис","Запропонована плата","Тип зайнятості","Працівник"],
        "R6":["Номер команди","Кількість учасників","Виділений бюджет","Вакансія","Кількість виконаних проектів"],
        "R7":["ПІБ директора","Стаж роботи","Відсоток акцій","Офіс"],
        "R8":["ПІБ компанії","Email","Дата першого замовлення","Кількість замовлень","Країна розташування"]
    }
    print(message, table)
    try:
        data = cur.execute("SELECT * FROM " + table).fetchall()
        lenght_of_data = len(data)
        if lenght_of_data == 0:
            await bot.send_message(message.from_user.id, 'Немає записів')
        else:
            i = 0
            lenght_of_row = len(data[0])
            if lenght_of_row == 4:
                for row in data:
                    await bot.send_message(message.from_user.id, f'{table_rows[table][0]}: {row[0]}\n{table_rows[table][1]}: {row[1]}\n{table_rows[table][2]}: {row[2]}\n{table_rows[table][3]}: {row[3]}')
            elif lenght_of_row == 5:
                for row in data:
                    await bot.send_message(message.from_user.id, f'{table_rows[table][0]}: {row[0]}\n{table_rows[table][1]}: {row[1]}\n{table_rows[table][2]}: {row[2]}\n{table_rows[table][3]}: {row[3]}\n{table_rows[table][4]}: {row[4]}')
            else:
                for row in data:
                    await bot.send_message(message.from_user.id, f'{table_rows[table][0]}: {row[0]}\n{table_rows[table][1]}: {row[1]}\n{table_rows[table][2]}: {row[2]}\n{table_rows[table][3]}: {row[3]}\n{table_rows[table][4]}: {row[4]}\n{table_rows[table][5]}: {row[5]}')
    except Exception as ex:
        await bot.send_message(message.from_user.id, ex)