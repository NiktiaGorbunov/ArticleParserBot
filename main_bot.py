from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import asyncio
import json
import requests

import config
from parsers import rbc_parser, ria_parser, rambler_parser

from sqlighter import SQLighter


token = config.tokenTG
bot = Bot(token)
dp = Dispatcher(bot)


# работаем с командой start
@dp.message_handler(commands=['start'])
async def welcome_start(message: types.Message):
    # сообщение приветсвия
    f = open('welcome_message.txt', 'r', encoding="utf-8")
    try:
        await bot.send_message(message.chat.id, f.read(), parse_mode = 'HTML')
    except:
        await bot.send_message(message.chat.id, "Привет! Что-то пошло не так\U0001F614\nНе переживай! Просто сообщи в поддержку, что я приболел\U0001F915",
                               parse_mode = 'HTML')
    finally:
        f.close()
        
    await subscribe(message)  # вызываем фунцкию subscribe для подписки на новостную рассылку



async def rbc_check():
    """

    :return:
    """
    while True:
        await asyncio.sleep(40)

        with open('last_article/rbc_last_article.json') as json_file:
            old_article = json.load(json_file)

        last_article = rbc_parser.get_last_article()

        if old_article["url"] != last_article["url"]:

            await esg_check(bot, last_article)

            with open('last_article/rbc_last_article.json', 'w') as json_file:
                json.dump(last_article, json_file)



async def ria_check():
    while True:
        await asyncio.sleep(40)

        with open('last_article/ria_last_article.json') as json_file:
            old_article = json.load(json_file)

        last_article = ria_parser.get_last_article()

        if old_article["url"] != last_article["url"]:
            await esg_check(bot, last_article)

            with open('last_article/ria_last_article.json', 'w') as json_file:
                json.dump(last_article, json_file)


async def rambler_check():
    while True:
        await asyncio.sleep(40)

        with open('last_article/rambler_last_article.json') as json_file:
            old_article = json.load(json_file)

        last_article = rambler_parser.get_last_article()

        if old_article["url"] != last_article["url"]:

            await esg_check(bot, last_article)

            with open('last_article/rambler_last_article.json', 'w') as json_file:
                json.dump(last_article, json_file)


async def esg_check(bot, article):
    url = "http://5.39.220.103:5009/ask"

    data = {
        "messages": [
            {"role": "system", "content": f"Ты определяешь, является ли новость ESG новостью"
                                          f"Отвечай только на поставленный вопрос, не уходи от темы вопроса. "
                                          f"Ты можешь писать только да или нет"},
            {"role": "user", "content": f"Относиться ли данная статья к ESG? Статья: {article['text']}"}
        ]
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        response_data = response.json()
        if response_data['response'] == 'да':
            await send_message(bot, article)
    # else:
    #     return f"Error: {response.status_code}, {response.text}"


async def send_message(bot, article):
    """
    :param bot:
    :param article:
    title - заголовок статьи
    url - ссылка на статью
    text - текст статьи

    """
    db = SQLighter('db.db')
    all_subscribed_users = db.get_subcriptions(status="true")

    for i in all_subscribed_users:
        try:
            # для обработки текста отправить содержимое статьи в классификатор
            # ESG_classificator = article["text"]
            await bot.send_message(i[0], text='<strong>' + article["title"] + '</strong>' + '\n\n' +
                                              article["url"] + '\n\n' + article["text"], parse_mode='HTML')
        except:
            pass

    db.close()


#активизация подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    #инициализируем соединение с БД
    db = SQLighter('db.db')
    
    if(db.subscriber_exists(message.from_user.id) == False):
        #если пользователя нет в БД, то добавляем со статусом true
        db.add_subscriber(message.from_user.id)
    else:
        #если пользователь есть в БД, то обнавляем статус
        db.update_subcription(message.from_user.id, 'true')

    db.close()
    
    await bot.send_message(message.chat.id, 'Вы успешно подписались на рассылку новостей!\U0001F60C')


#отмена подписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    #инициализируем соединение с БД
    db = SQLighter('db.db')
    
    if(db.subscriber_exists(message.from_user.id) == False):
        #если пользователя нет в БД
        db.add_subscriber(message.from_user.id, 'false')
        await bot.send_message(message.chat.id, 'На данный момент, вы не были подписаны на новостную рассылку...')
    else:
        #если пользователь есть, то обнавляем статутс
        db.update_subcription(message.from_user.id, 'false')
        await bot.send_message(message.chat.id, 'Вы успешно отписались от новостной рассылки\U0001F612')

    db.close()


#команда help
@dp.message_handler(commands=['help'])
async def welcome_help(message: types.Message):
    await bot.send_message(message.chat.id, 'Если у Вас возникла ошибка, то я ошибся :(')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(rbc_check())
    loop.create_task(ria_check())
    loop.create_task(rambler_check())
    executor.start_polling(dp, skip_updates=True)
