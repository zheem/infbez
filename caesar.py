import re
import copy

def cipher(text, key):
    if key > 33:
        key = key % 33
    out = ''
    for i in text:
        if ord(i) >= ord('а') and ord(i) <= ord('я'):
            if ord(i) + key > ord('я'):
                out = out + chr((ord(i) + key) - 33)
            else:
                out = out + chr(ord(i) + key)
        elif ord(i) >= ord('А') and ord(i) <= ord('Я'):
            if ord(i) + key > ord('Я'):
                out = out + chr((ord(i) + key) - 33)
            else:
                out = out + chr(ord(i) + key)
        else:
            out = out + i
    return out


def decipher(text, key):
    if key > 33:
        key = key % 33
    out = ''
    for i in text:
        if ord(i) >= ord('а') and ord(i) <= ord('я'):
            if ord(i) - key < ord('а'):
                out = out + chr((ord(i) - key) + 33)
            else:
                out = out + chr(ord(i) - key)
        elif ord(i) >= ord('А') and ord(i) <= ord('Я'):
            if ord(i) - key < ord('А'):
                out = out + chr((ord(i) - key) + 33)
            else:
                out = out + chr(ord(i) - key)
        else:
            out = out + i
    return out


def frequency_analysis(text):
    num = 0
    dictionary = {}
    text = text.lower()
    for i in text:
        if re.fullmatch(r'[а-я]', i):
            num += 1
            if i in dictionary:
                value = dictionary[i]
                dictionary[i] = value + 1
            else:
                dictionary[i] = 1
    for i in dictionary:
        dictionary[i] = dictionary[i] / num
    list_d = list(dictionary.items())
    list_d.sort(key=lambda i: i[1], reverse=True)
    print(list_d)
    return list_d

def frequency_pars(text):
    pars = []
    for i in range(len(alpha)):
        for j in range(len(alpha)):
            pars.append(alpha[i] + alpha[j])
    for i in range(len(pars)):
        pars[i] = ([pars[i], (text.count(pars[i]) / len(text))])
    return sorted(pars, key=lambda x: x[1])[::-1]


def search_assignment(str, dict, dict2, num_flag=False):
    num = 0
    out = ''
    for i in range(len(dict)):
        if str == dict[i][0]:
            num = i
            out = dict2[i]
            break
    if num_flag:
        return num, out[0]
    else:
        return out[0]


def frequency_single(text):
    single_char = list(alpha)
    rep = re.compile("[^а-яА-я]")
    text = rep.sub(" ", text)
    for i in range(len(single_char)):
        single_char[i] = ([single_char[i], (text.count(' '+single_char[i]+' '))])
    s = sum(row[1] for row in single_char)
    for i in range(len(single_char)):
        single_char[i][-1] = single_char[i][-1]/s
    return sorted(single_char, key=lambda x: x[1])[::-1]


alpha = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
f = open('books_part.txt', encoding='utf-8')
part = f.read()
f = open('books.txt', encoding='utf-8')
books = f.read()

print("Частотные словари изночальной главы и всех томов")
part_dict = frequency_analysis(part)
books_dict = frequency_analysis(books)

key = 1
caesar = cipher(part, key)
print('\nЗашифрованный текст\n________________________________________\n',caesar[:1000])
caesar_dict = frequency_analysis(caesar)

decipher_key = ord(caesar_dict[0][0]) - ord(part_dict[0][0])
decipher_by_key = decipher(caesar, decipher_key)
print('\nРасшифровка по ключу\n________________________________________\n',decipher_by_key[:1000])

decoded_by_frequency = ''
for i in caesar:
    upp = False
    decoded_by_frequency += i
    if re.fullmatch(r'[А-Я]', i):
        i = i.lower()
        upp = True
    for j in range(len(caesar_dict)):
        if caesar_dict[j][0] == i and upp == False:
            decoded_by_frequency = decoded_by_frequency[:-1] + books_dict[j][0]
            break
        if caesar_dict[j][0] == i and upp == True:
            decoded_by_frequency = decoded_by_frequency[:-1] + books_dict[j][0].upper()
            break

print('\nРасшифровка частотным анализом\n________________________________________\n',decoded_by_frequency[:1000])

books = books.lower()
caesar = caesar.lower()
pars_books = frequency_pars(books)
pars_caesar = frequency_pars(caesar)
print('\nЧастоты биграмм всей книги и главы:')
print(pars_books)
print(pars_caesar)
print('\nИсходный текст:\n_________________________________________________________________________________________\n', part[:1000].lower())
single_books = frequency_single(books)
single_caesar = frequency_single(caesar)
checking_caesar = copy.deepcopy(caesar)
caesar = list(caesar)
i = 0
while i<(len(caesar)-2):
    if re.fullmatch(r'[а-я]', caesar[i]) and re.fullmatch(r'[а-я]', caesar[i+1]) and re.fullmatch(r'[а-я]', caesar[i+2]):
        priority, pair = search_assignment(caesar[i]+caesar[i+1], pars_caesar, pars_books, True)
        priority2, pair2 = search_assignment(caesar[i+1] + caesar[i+2], pars_caesar, pars_books, True)
        if priority > priority2:
            caesar[i] = pair[0]
            caesar[i + 1] = pair[1]
            i += 3
            continue
        else:
            caesar[i+1] = pair2[0]
            caesar[i+2] = pair2[1]
            caesar[i] = search_assignment(caesar[i]+checking_caesar[i+1], pars_caesar, pars_books)[0]
            i += 4
            continue
    elif re.fullmatch(r'[а-я]', caesar[i]) and re.fullmatch(r'[а-я]', caesar[i+1]): # and not re.fullmatch(r'[а-я]', caesar[i-1]):
        pair = search_assignment(caesar[i]+caesar[i+1], pars_caesar, pars_books)
        caesar[i] = pair[0]
        caesar[i+1] = pair[1]
        i += 4
    elif i > 0 and re.fullmatch(r'[а-я]', caesar[i]) and re.fullmatch(r'[а-я]', caesar[i-1]):
        caesar[i] = search_assignment(checking_caesar[i-1]+caesar[i], pars_caesar, pars_books)[1]
        i += 2
        continue
    elif i > 0 and re.fullmatch(r'[а-я]', caesar[i]) and not re.fullmatch(r'[а-я]', caesar[i-1]):
        caesar[i] = search_assignment(caesar[i], single_caesar, single_books)
        i += 2
        continue
    else:
        i += 1
        continue
print('\nРасшифровка биграммой\n_________________________________________________________________________')
print(''.join(caesar[:1000]))
part = list(part.lower())
sum = 0
full_sum = 0
for i in range(len(caesar)):
    if re.fullmatch(r'[а-я]', caesar[i]):
        full_sum += 1
        if caesar[i] == part[i]:
            sum += 1
print('\nПроцент верных символов при расшифровке биграммами:', sum*100/full_sum)