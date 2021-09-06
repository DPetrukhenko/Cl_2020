from typing import List
from pandas.core.frame import DataFrame
import telebot
from config import TOKEN
import requests as rq
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import sqlite3
from collections import Counter


data = pd.read_csv('rec.csv')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: str) -> None:
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_links(
        id INTEGER, link TEXT
        )''')
    connect.commit()

    user_id = message.from_user.id
    cursor.execute(f'SELECT id FROM user_links WHERE id = {user_id}')
    user_data = cursor.fetchone()
    if user_data is None:
        bot.send_message(message.from_user.id,
                         f'Привет, {message.from_user.first_name}!\n'
                         f'Я бот, который знает много игр.'
                         f'Пожалуйста, пришли ссылку на свой профиль в Steam, '
                         f'а я тебе что-нибудь порекомендую.')
    else:
        bot.send_message(message.from_user.id,
                         f'Привет, {message.from_user.first_name}!'
                         f'Рад тебя видеть! Хочешь во что-нибудь поиграть?\n'
                         f'Выбирай:\n'
                         f'/free - если хочешь какую-нибудь бесплатную игру,\n'
                         f'/paid - если подумываешь купить что-нибудь новенькое.')


def get_link(message: str) -> bool:
    if re.search(r'https://steamcommunity', message.text):
        return True
    else:
        return False


@bot.message_handler(func=get_link, content_types=['text'])
def write_link(message: str) -> None:
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    user_id = message.from_user.id
    cursor.execute(f'SELECT id FROM user_links WHERE id = {user_id}')
    user_data = cursor.fetchone()
    if user_data is None:
        url = f'{message.text}/games/?tab=all'
        cursor.execute(
            'INSERT INTO user_links VALUES(?,?);', [user_id, url]
            )
        connect.commit()
        bot.send_message(message.from_user.id,
                         'Отлично! Будем знакомы :) Выбирай:\n'
                         '/free - если хочешь какую-нибудь бесплатную игру,\n'
                         '/paid - если подумываешь купить что-нибудь новенькое.')
    else:
        bot.send_message(message.from_user.id, 'Давно не виделись!')


@bot.message_handler(commands=['delete'])
def delete(message: str) -> None:
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    user_id = message.from_user.id
    cursor.execute(f'DELETE FROM user_links WHERE id = {user_id}')
    connect.commit()


def get_games(link: str) -> List[str]:
    page = rq.get(link)
    soup = bs(page.content, 'html.parser')
    text = str(soup.find('script', {'language': 'javascript'}).prettify())
    games = re.findall(r'(?<="name":").+?(?=")', text)
    # hours = re.findall(r'(?<="hours_forever":").+?(?=")', text)
    games = [' '.join(re.findall('[A-z0-9]+', elem)) for elem in games]
    games = [re.sub(r'\\u\w{4}|\\', '', i) for i in games]
    # games = list(zip(games, hours))
    # print(games)
    return games


def get_clusters(games: List[str], cluster: str, loc_data: DataFrame) -> List[int]:
    clusters = loc_data[
        [x in games[:100] for x in loc_data['Title_clean']]
        ][cluster]
    top_clusters = Counter(clusters).most_common(3)
    return top_clusters


def get_recs(games: list, cluster: str, top_cluster: int, loc_data: DataFrame) -> DataFrame:
    game = loc_data[
        ([x not in games for x in loc_data['Title_clean']]) &
        (loc_data[cluster] == top_cluster)
        ].sort_values(
            ['Scores Count', 'Mean score'],
            ascending=False)[
                ['Title', 'URL', 'Description']
                ].head(1)
    return game


@bot.message_handler(commands=['free'])
def recommend_free(message: str) -> None:
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    user_id = message.from_user.id
    cursor.execute(f'SELECT link FROM user_links WHERE id = {user_id}')
    user_url = cursor.fetchone()[0]

    games = get_games(user_url)
    if len(games) == 0:
        bot.send_message(message.from_user.id,
                         'Кажется, у тебя приватный аккаунт. '
                         'Проверь, видны ли другим людям твои игры'
                         'и есть ли у теб игры, и попробуй снова.')
    else:
        loc_data = data
        use = get_clusters(games, 'use_cluster', loc_data)

        loc_data = loc_data[loc_data['isFree'] == 'Free']
        loc_data.reset_index(drop=True, inplace=True)

        recs_use1 = get_recs(games, 'use_cluster', use[0][0], loc_data)
        recs_use2 = get_recs(games, 'use_cluster', use[1][0], loc_data)
        recs_use3 = get_recs(games, 'use_cluster', use[2][0], loc_data)

        bot.send_message(message.from_user.id,
                         f'Тебе может понравиться:\n'
                         f'1. [{recs_use1["Title"].to_list()[0]}]'
                         f'({recs_use1["URL"].to_list()[0]})\n'
                         f'{recs_use1["Description"].to_list()[0].strip()}\n'
                         f'2. [{recs_use2["Title"].to_list()[0]}]'
                         f'({recs_use2["URL"].to_list()[0]})\n'
                         f'{recs_use2["Description"].to_list()[0].strip()}\n'
                         f'3. [{recs_use3["Title"].to_list()[0]}]'
                         f'({recs_use3["URL"].to_list()[0]})\n'
                         f'{recs_use3["Description"].to_list()[0].strip()}\n',
                         parse_mode="markdown"
                         )


@bot.message_handler(commands=['paid'])
def recommend_paid(message: str) -> None:
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    user_id = message.from_user.id
    cursor.execute(f'SELECT link FROM user_links WHERE id = {user_id}')
    user_url = cursor.fetchone()[0]

    games = get_games(user_url)
    if len(games) == 0:
        bot.send_message(message.from_user.id,
                         'Кажется, у тебя приватный аккаунт. '
                         'Проверь, видны ли другим людям твои игры'
                         'и есть ли у теб игры, и попробуй снова.')
    else:
        loc_data = data
        use = get_clusters(games, 'use_cluster', loc_data)

        loc_data = loc_data[loc_data['isFree'] == 'payed']
        loc_data.reset_index(drop=True, inplace=True)

        recs_use1 = get_recs(games, 'use_cluster', use[0][0], loc_data)
        recs_use2 = get_recs(games, 'use_cluster', use[1][0], loc_data)
        recs_use3 = get_recs(games, 'use_cluster', use[2][0], loc_data)

        bot.send_message(message.from_user.id,
                         f'Тебе может понравиться:\n'
                         f'1. [{recs_use1["Title"].to_list()[0]}]'
                         f'({recs_use1["URL"].to_list()[0]})\n'
                         f'{recs_use1["Description"].to_list()[0].strip()}\n'
                         f'2. [{recs_use2["Title"].to_list()[0]}]'
                         f'({recs_use2["URL"].to_list()[0]})\n'
                         f'{recs_use2["Description"].to_list()[0].strip()}\n'
                         f'3. [{recs_use3["Title"].to_list()[0]}]'
                         f'({recs_use3["URL"].to_list()[0]})\n'
                         f'{recs_use3["Description"].to_list()[0].strip()}\n',
                         parse_mode="markdown"
                         )


bot.polling(none_stop=True)
