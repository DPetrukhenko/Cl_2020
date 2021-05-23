import re
with open(r'C:\Users\Антон\PycharmProjects\pythonProject\e-mails..txt', 'r', encoding='utf8') as file:
    text = file.read()

# регулярное выражение для поиска полных адресов

e_mails = re.findall(r'"? ?[\w.\-"!+]+@[\w.\-]*\w', text)
e_mails = set(e_mails)
print('Уникальных e-mail адресов в тексте найдено:', len(e_mails))

# регулярное выражение для поиска доменов

domains = re.findall(r'(?<=@)[\w\-.]*\w', text)
domains = set(domains)
print('Уникальных доменов в тексте найдено:', len(domains))
