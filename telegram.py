import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from api import flparcer
from datetime import datetime

stop_flag = False

logging.basicConfig(level=logging.INFO)
bot = Bot(token="7030498889:AAE_Y_mAWaNO9tPXi1KwQn10uCsvW6dZoCg", parse_mode="HTML")
dp = Dispatcher()

def telemain():
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer("Добро пожаловать в парсер для FL\n" "Для начало работы введите:\n\n" "/getweb - для парсинга заказов по веб верстки\n" "/getparser - для парсинга заказов по парсингу\n" "/stop - для остановки парсинга\n" "Автор: @lavr_nix")

    @dp.message(Command("stop"))
    async def stop(message: types.Message):
        global stop_flag
        stop_flag = True
        print("Status: stop" + str(datetime.now()))
        await message.answer("Сканирование остановлено!")


    @dp.message(Command("getweb"))
    async def web(message: types.Message):
        await message.answer("Начинаю сканирование в веб""\nОжидайте ответа...")
        global stop_flag
        stop_flag = False
        while not stop_flag:
            print("Status: Accepted Web: " + str(datetime.now()))
            
            if datetime.now().month < 10:
                date_current = "0" + str(datetime.now().month) 
            else:
                date_current = str(datetime.now().month)
            if datetime.now().day < 10:
                date_current = date_current  + "0" + str(datetime.now().day) + str(datetime.now().year)
            else:
                date_current = date_current  + str(datetime.now().day) + str(datetime.now().year)
            if datetime.now().hour < 10:
                date_current = date_current + "0" + str(datetime.now().hour)
            else:
                date_current = date_current + str(datetime.now().hour)
            if datetime.now().minute < 10:
                date_current = date_current + "0" + str(datetime.now().minute)
            else:
                date_current = date_current + str(datetime.now().minute)
            
            await asyncio.sleep(1)
            print("Status: parsing Web: " + str(datetime.now()))
            a = flparcer("https://www.fl.ru/search/?action=search&type=projects&search_string=%D0%B2%D0%B5%D1%80%D1%81%D1%82%D0%BA%D0%B0%20%D1%81%D0%B0%D0%B9%D1%82%D0%B0&search_hint=%D0%BE%D0%B1%D0%B7%D0%BE%D1%80%D1%8B%20%D0%B8%D0%B3%D1%80")
            for el in a.getfllist():
                if int(el['dateall']) >= int(date_current):
                    await message.answer(f"<b>Из темы веб верстка </b> \n\n"
                                        f"<b>Название:</b> { el['name'] } \n"
                                        f"<b>Отплата: { el['price']}</b> \n"
                                        f"<b>Дата опубликования:</b> {el['date']} \n \n"
                                        f"<b>Описание:</b> \n{el['overview']} \n \n"
                                        f"<b>Cсылка: </b>{el['url']}\n"
                                        f"Время заказа: {el['dateall']}, Текущие время: {date_current}"
                    )
                else:
                    print("Status: No orders Web: " + str(datetime.now()))
    @dp.message(Command("getparser"))
    async def parser(message: types.Message):
            await message.answer("Начинаю сканирование в парсинг""\nОжидайте ответа...")
            global stop_flag
            stop_flag = False
            while not stop_flag:
                print("Status: Accepted Parser: " + str(datetime.now())) 
                if datetime.now().month < 10:
                    date_current = "0" + str(datetime.now().month) 
                else:
                    date_current = str(datetime.now().month)
                if datetime.now().day < 10:
                    date_current = date_current  + "0" + str(datetime.now().day) + str(datetime.now().year)
                else:
                    date_current = date_current  + str(datetime.now().day) + str(datetime.now().year)
                if datetime.now().hour < 10:
                    date_current = date_current + "0" + str(datetime.now().hour)
                else:
                    date_current = date_current + str(datetime.now().hour)
                if datetime.now().minute < 10:
                    date_current = date_current + "0" + str(datetime.now().minute)
                else:
                    date_current = date_current + str(datetime.now().minute)
                await asyncio.sleep(1)
                a = flparcer("https://www.fl.ru/search/?action=search&type=projects&search_string=%D0%BF%D0%B0%D1%80%D1%81%D0%B8%D1%82%D1%8C&search_hint=%D1%88%D0%BE%D0%BF%D0%BF%D0%B8%D0%BD%D0%B3")
                for el in a.getfllist():
                    if int(el['dateall']) <= int(date_current):
                        await message.answer(f"<b>Из темы Парсинг </b> \n\n"
                                            f"<b>Название:</b> { el['name'] } \n"
                                            f"<b>Отплата: { el['price']}</b> \n"
                                            f"<b>Дата опубликования:</b> {el['date']} \n \n"
                                            f"<b>Описание:</b> \n{el['overview']} \n \n"
                                            f"<b>Cсылка: </b>{el['url']}\n"
                                            f"Время заказа: {el['dateall']}, Текущие время: {date_current}"

                    )
                    else:
                        print("Status: No orders Parser: " + str(datetime.now()))

    async def main():
        await dp.start_polling(bot)
        loop = asyncio.get_event_loop()
        t = web()
        p = parser()
        loop.run_until_complete(t.init())
        loop.run_until_complete(p.init())
    asyncio.run(main())

    