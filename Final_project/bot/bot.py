import telebot
from telebot import types
import requests as rq
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import sqlite3
from collections import Counter


data = pd.read_csv('/Users/darapetruhnenko/учеба/python/CL_2020/Final_Project/rec.csv')

bot = telebot.TeleBot('1816879772:AAEvkIyRABgyu4QD3eCPkZm7nx0EpbOVznI')


@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
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
        bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!\n'
                                               f'Пожалуйста, пришли ссылку на свой профиль в Steam, '
                                               f'а я тебе что-нибудь порекомендую.')
    else:
        bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!'
                                               f'Рад тебя видеть! Хочешь во что-нибудь поиграть?\n'
                                               f'Выбирай:\n'
                                               f'/free - если хочешь какую-нибудь бесплатную игру,\n'
                                               f'/payed - если подумываешь купить что-нибудь новенькое.')


def get_link(message):
    if re.search(r'https://steamcommunity', message.text):
        return True
    else:
        return False


@bot.message_handler(func = get_link, content_types = ['text'])
def write_link(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    user_id = message.from_user.id
    cursor.execute(f'SELECT id FROM user_links WHERE id = {user_id}')
    user_data = cursor.fetchone()
    if user_data is None:
        url = f'{message.text}/games/?tab=all'
        cursor.execute('INSERT INTO user_links VALUES(?,?);', [user_id, url])
        connect.commit()
        bot.send_message(message.from_user.id, 'Отлично! Будем знакомы :) Выбирай:\n'
                                               '/free - если хочешь какую-нибудь бесплатную игру,\n'
                                               '/payed - если подумываешь купить что-нибудь новенькое.')
    else:
        bot.send_message(message.from_user.id, 'Давно не виделись!')


@bot.message_handler(commands = ['delete'])
def delete(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    user_id = message.from_user.id
    cursor.execute(f'DELETE FROM user_links WHERE id = {user_id}')
    connect.commit()


def get_games(link):
    page = rq.get(link)
    soup = bs(page.content, 'html.parser')
    text = str(soup.find('script', {'language': 'javascript'}).prettify())
    games = re.findall('(?<="name":").+?(?=")', text)[:50]
    return games


@bot.message_handler(commands = ['free'])
def recommend_free(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    user_id = message.from_user.id
    cursor.execute(f'SELECT link FROM user_links WHERE id = {user_id}')
    user_url = cursor.fetchone()[0]

    games = get_games(user_url)
    loc_data = data
    clusters_use = []
    clusters_tf_idf = []
    clusters_bert = []
    clusters_umap = []

    for i in games:
        clusters_use.extend(loc_data[loc_data['Title'] == i]['use_cluster'].to_list())
        clusters_tf_idf.extend(loc_data[loc_data['Title'] == i]['Tf-Idf cluster'].to_list())
        clusters_bert.extend(loc_data[loc_data['Title'] == i]['bert_cluster'].to_list())
        clusters_umap.extend(loc_data[loc_data['Title'] == i]['Umap cluster'].to_list())

    use = Counter(clusters_use).most_common(1)[0][0]
    tf_idf = Counter(clusters_tf_idf).most_common(1)[0][0]
    umap = Counter(clusters_umap).most_common(1)[0][0]
    bert = Counter(clusters_bert).most_common(1)[0][0]
    loc_data = loc_data[loc_data['isFree'] == 'Free']
    loc_data.reset_index(drop = True, inplace = True)
    recs_use = []
    recs_tf_idf = []
    recs_bert = []
    recs_umap = []
    indexes = loc_data.index
    for elem in loc_data[loc_data['use_cluster'] == use]['Title'][:10]:
        if elem not in games:
            index = indexes[loc_data['Title'] == elem].to_list()[0]
            recs_use.append((loc_data.iloc[index]['Title'],
                             loc_data.iloc[index]['URL']))

    for elem in loc_data[loc_data['Tf-Idf cluster'] == tf_idf]['Title'][:10]:
        if elem not in games:
            index = indexes[loc_data['Title'] == elem].to_list()[0]
            recs_tf_idf.append((loc_data.iloc[index]['Title'],
                                loc_data.iloc[index]['URL']))

    for elem in loc_data[loc_data['bert_cluster'] == bert]['Title'][:10]:
        if elem not in games:
            index = indexes[loc_data['Title'] == elem].to_list()[0]
            recs_bert.append((loc_data.iloc[index]['Title'],
                             loc_data.iloc[index]['URL']))

    for elem in loc_data[loc_data['Umap cluster'] == umap]['Title'][:10]:
        if elem not in games:
            index = indexes[loc_data['Title'] == elem].to_list()[0]
            recs_umap.append((loc_data.iloc[index]['Title'],
                             loc_data.iloc[index]['URL']))

    bot.send_message(message.from_user.id, f'USE предлагает поиграть в:\n'
                                           f'{recs_use[0][0]}\n'
                                           f'{recs_use[0][1]}\n'
                                           f'{recs_use[1][0]}\n'
                                           f'{recs_use[1][1]}\n'
                                           f'{recs_use[2][0]}\n'
                                           f'{recs_use[2][1]}\n'
                                           f'BERT предлагает поиграть в:\n'
                                           f'{recs_bert[0][0]}\n'
                                           f'{recs_bert[0][1]}\n'
                                           f'{recs_bert[1][0]}\n'
                                           f'{recs_bert[1][1]}\n'
                                           f'{recs_bert[2][0]}\n'
                                           f'{recs_bert[2][1]}\n'
                                           f'TF-IDF + NMF предлагает поиграть в:\n'
                                           f'{recs_tf_idf[0][0]}\n'
                                           f'{recs_tf_idf[0][1]}\n'
                                           f'{recs_tf_idf[1][0]}\n'
                                           f'{recs_tf_idf[1][1]}\n'
                                           f'{recs_tf_idf[2][0]}\n'
                                           f'{recs_tf_idf[2][1]}\n'
                                           f'TF-IDF + UMAP предлагает поиграть в:\n'
                                           f'{recs_umap[0][0]}\n'
                                           f'{recs_umap[0][1]}\n'
                                           f'{recs_umap[1][0]}\n'
                                           f'{recs_umap[1][1]}\n'
                                           f'{recs_umap[2][0]}\n'
                                           f'{recs_umap[2][1]}')


@bot.message_handler(commands = ['payed'])
def recommend_free(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    user_id = message.from_user.id
    cursor.execute(f'SELECT link FROM user_links WHERE id = {user_id}')
    user_url = cursor.fetchone()[0]

    games = get_games(user_url)
    loc_data = data
    clusters_use = []
    clusters_tf_idf = []
    clusters_bert = []
    clusters_umap = []

    for i in games:
        clusters_use.extend(loc_data[loc_data['Title'] == i]['use_cluster'].to_list())
        clusters_tf_idf.extend(loc_data[loc_data['Title'] == i]['Tf-Idf cluster'].to_list())
        clusters_bert.extend(loc_data[loc_data['Title'] == i]['bert_cluster'].to_list())
        clusters_umap.extend(loc_data[loc_data['Title'] == i]['Umap cluster'].to_list())

    use = Counter(clusters_use).most_common(1)[0][0]
    tf_idf = Counter(clusters_tf_idf).most_common(1)[0][0]
    umap = Counter(clusters_umap).most_common(1)[0][0]
    bert = Counter(clusters_bert).most_common(1)[0][0]
    loc_data = loc_data[loc_data['isFree'] == 'payed']
    loc_data.reset_index(drop = True, inplace = True)
    recs_use = []
    recs_tf_idf = []
    recs_bert = []
    recs_umap = []
    indexes = loc_data.index
    for elem in loc_data[loc_data['use_cluster'] == use]['Title'][:10]:
        if elem not in games:
            index = indexes[loc_data['Title'] == elem].to_list()[0]
            recs_use.append((loc_data.iloc[index]['Title'],
                             loc_data.iloc[index]['URL']))

    for elem in loc_data[loc_data['Tf-Idf cluster'] == tf_idf]['Title'][:10]:
        if elem not in games:
            index = indexes[loc_data['Title'] == elem].to_list()[0]
            recs_tf_idf.append((loc_data.iloc[index]['Title'],
                                loc_data.iloc[index]['URL']))

    for elem in loc_data[loc_data['bert_cluster'] == bert]['Title'][:10]:
        if elem not in games:
            index = indexes[loc_data['Title'] == elem].to_list()[0]
            recs_bert.append((loc_data.iloc[index]['Title'],
                             loc_data.iloc[index]['URL']))

    for elem in loc_data[loc_data['Umap cluster'] == umap]['Title'][:10]:
        if elem not in games:
            index = indexes[loc_data['Title'] == elem].to_list()[0]
            recs_umap.append((loc_data.iloc[index]['Title'],
                             loc_data.iloc[index]['URL']))

    bot.send_message(message.from_user.id, f'USE предлагает поиграть в:\n'
                                           f'{recs_use[0][0]}\n'
                                           f'{recs_use[0][1]}\n'
                                           f'{recs_use[1][0]}\n'
                                           f'{recs_use[1][1]}\n'
                                           f'{recs_use[2][0]}\n'
                                           f'{recs_use[2][1]}\n'
                                           f'BERT предлагает поиграть в:\n'
                                           f'{recs_bert[0][0]}\n'
                                           f'{recs_bert[0][1]}\n'
                                           f'{recs_bert[1][0]}\n'
                                           f'{recs_bert[1][1]}\n'
                                           f'{recs_bert[2][0]}\n'
                                           f'{recs_bert[2][1]}\n'
                                           f'TF-IDF + NMF предлагает поиграть в:\n'
                                           f'{recs_tf_idf[0][0]}\n'
                                           f'{recs_tf_idf[0][1]}\n'
                                           f'{recs_tf_idf[1][0]}\n'
                                           f'{recs_tf_idf[1][1]}\n'
                                           f'{recs_tf_idf[2][0]}\n'
                                           f'{recs_tf_idf[2][1]}\n'
                                           f'TF-IDF + UMAP предлагает поиграть в:\n'
                                           f'{recs_umap[0][0]}\n'
                                           f'{recs_umap[0][1]}\n'
                                           f'{recs_umap[1][0]}\n'
                                           f'{recs_umap[1][1]}\n'
                                           f'{recs_umap[2][0]}\n'
                                           f'{recs_umap[2][1]}')


bot.polling(none_stop = True)
