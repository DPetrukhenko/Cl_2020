# задание 1
# какие из этих строк можно конкатенировать? Какие умножать? Какие вычитать?
a = 23
b = 34.02
c = "python is cool "
d = "you are cool, too "
print(c+d)
print(c*a)
print(d*a)
print(a*b)
print(a-b)
print(b-a)
print(a+b)

# задание 2
"""
Придумайте такую строку (на любом знакомом Вам языке),чтобы она состояла из трех других (повторы строки разрешены).
Напишите код. Если вы можете сделать это более, чем одним способом, напишите все способы
"""
phrase = "Help "*3
print(phrase)
one = "Help "
two = "i need somebody "
phrase2 = one + two*2
print(phrase2)
three = "not just anybody"
phrase3 = one + two + three
print(phrase3)
print(one, two, three)

# задание 3
"""
Как из слова "апельсин" сделать слово "спаниель" ?
Подсказка: вам помогут срезы и операции с индексами
"""
word = "апельсин"
part1 = word[5]
print(part1)
part2 = word[1::-1]
print(part2)
part3 = word[:5:-1]
print(part3)
part4 = word[2:5]
print(part4)
word2 = part1 + part2 + part3 + part4
print(word2)
# меньше команд
word2 = word[5] + word[1::-1] + word[:5:-1] + word[2:5]
print(word2)

# задание 4 (выполняется по желанию)
"элементы в переменной text преобразуйте в нижний регистр, а затем запишите наоборот, с последнего элемента по первый"
text = "WOW,NOEL SEES LEON"
text = text.lower()
print(text)
print(text[::-1])
