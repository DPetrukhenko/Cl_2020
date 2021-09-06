import re
import string
from gensim.utils import tokenize
from gensim.summarization.textcleaner import split_sentences

with open(r'python_for_CL\files and system\city_smells.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# функция для записи в текстовый файл
def writing(target_file, opening_mode, information):
    with open(target_file, opening_mode, encoding='utf-8') as text_file:
        return text_file.write(information)

# 1. Делаем переменную с подготовленным текстом и смотрим среднюю длину слова:
# вариант 1
string.punctuation += '—«»'
text_normalized = text.lower().translate(str.maketrans('', '', string.punctuation)).split()
# вариант 2
text_tokenized = list(tokenize(text, lowercase=True))
# переменная, в которую будем складывать длину каждого слова
total_length = 0
# цикл, в котором считаем длину каждого отдельного слова для нахождения среднего значения
for word in text_normalized:
    total_length += len(word)
# записываем результат
writing('Статистика по тексту.txt', 'w', '\t\tСтатистические данные по тексту "city-smells".\n\n1. Средняя длина '
                                         'слова в тексте: '
        + str(round(total_length / len(text_normalized))) + ' символов;'
        )

# 2. Смотрим среднюю длину предложения в тексте (я взяла функцию из модуля gensim):
sentence_list = list(split_sentences(text))
# из предыдущего задания знаем общее количество слов:
writing('Статистика по тексту.txt', 'a', '\n2. Средняя длина предложения в тексте: ' +
        str(round(len(text_tokenized) / len(sentence_list))) + ' слов;')

# 3. Во сколько раз самое длинное предложение длиннее самого короткого:
# по символам:
sentence_sizes = []
for sentence in sentence_list:
    sentence_sizes.append(len(sentence))
writing('Статистика по тексту.txt', 'a', '\n3. Cамое длинное предложение длиннее самого (по символам) короткого '
                                         'предложения в ' +
        str(max(sentence_sizes) // min(sentence_sizes)) + ' раз;')
# по словам:
sentence_sizes2 = []
for sent in sentence_list:
    sentence_sizes2.append(len(list(tokenize(sent, lowercase=True))))
writing('Статистика по тексту.txt', 'a', '\n4. Cамое длинное предложение длиннее самого (по словам) короткого '
                                         'предложения в ' +
        str(max(sentence_sizes2) // min(sentence_sizes2)) + ' раз;')

# Во сколько раз самое длинное слово длиннее самого короткого:
word_list = []
for word in text_tokenized:
    word_list.append(len(word))
writing('Статистика по тексту.txt', 'a', '\n5. Cамое длинное слово длиннее самого короткого '
                                         'слова в ' +
        str(max(word_list) // min(word_list)) + ' раз;')

# 4. Среднее количество пунктуационных знаков в предложении:

punctuation_total = len(re.findall(r'[!"#$%&\'()*+,\-./:;<=>?@\[\]^_`{|}~—«»]', text))
writing('Статистика по тексту.txt', 'a', '\n6. Среднее количество пунктуационных знаков в тексте: ' +
        str(round(punctuation_total / len(sentence_list))) + ';')

# 5. Количество уникальных слов и пропорция общему количеству слов в тексте:
# пока так ¯\_(ツ)_/¯
unique_words = set(text_normalized)
writing('Статистика по тексту.txt', 'a', '\n7. Количество уникальных слов в тексте: ' + str(len(unique_words))
        + '; пропорция общему количеству слов в тексте: ' + str(len(unique_words)) + ' к '
        + str(len(text_normalized)) + '.')
