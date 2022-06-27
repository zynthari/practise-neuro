# coding: utf8

import csv
from typing import Tuple, Any
from random import choice

import pytrovich

from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker
from pytrovich.detector import PetrovichGenderDetector

# читаем из файлов записи
#в базе как будто есть ошибки. Добавлю проверку количества элементов в записи, неподходящие буду отбрасывать
def makeLists(path):
    obj_array = []
    with open(path, encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        print('Headers: ', headers)
        err = 0
        for row in reader:
            obj = tuple(row[0].split(";"))
            if len(obj) == 6:
                obj_array.append(obj)
            else:
                err = err + 1
    return obj_array, err


# упорядочим по количеству людей с именем
def sortByPopularity(obj_array):
    return sorted(obj_array, reverse=True, key=lambda obj: int(obj[3]))

#запишем в файл для удобства
def writeSorted(obj_array, filename):
    f = open(filename, "w+")
    for obj in obj_array:
        f.write(f"{obj}\n")
    f.close()

#только имена
def extractNames(obj_array):
    names = []
    for obj in obj_array:
        names.append((obj[1], obj[2]))
    return names

#новые туплы
def formsOfNames(names):
    forms = []
    err = 0
    maker = PetrovichDeclinationMaker()
    detector = PetrovichGenderDetector()
    for name in names:
        if name[1] == "Ж":
            Gen = Gender.FEMALE
        else:
            Gen = Gender.MALE
        forms.append((name[0], maker.make(NamePart.FIRSTNAME, Gen,
                                       Case.GENITIVE, name[0])))
    return forms

#с фамилиями в файле определенного пола нет, попробую последовать правилу "если кончается на а, то женская,
# на в - мужская, остальное - унисекс
def surnameGenderDet(surnames):
    det_surnames = []
    for surname in surnames:
        if surname[0][len(surname[0])-1] == 'в' or surname[0][len(surname[0])-2:] == "ин" or surname[0][len(surname[0])-3:] == "кий" or surname[0][len(surname[0])-3:] == "ный" or surname[0][len(surname[0])-3:] == "цын" or surname[0][len(surname[0])-2:] == "ой" or surname[0][len(surname[0])-3:] == "вый" or surname[0][len(surname[0])-3:] == "ний":
            det_surnames.append((surname[0], "М"))
        elif surname[0][len(surname[0])-2:] == "ва" or surname[0][len(surname[0])-3:] == "ина" or surname[0][len(surname[0])-4:] == "цына" or surname[0][len(surname[0])-2:] == "ая" or surname[0][len(surname[0])-3:] == "няя":
            det_surnames.append((surname[0], "Ж"))
        else:
            det_surnames.append((surname[0], "У"))
    return det_surnames

#генерация имен
def randomName(count, names, surnames, patronyms):
    rand = []
    for i in range(count):
        rand_name = choice(names)
        while True:
            rand_patro = choice(patronyms)
            if rand_patro[1] == rand_name[1]:
                rand_surname = choice(surnames)
                if rand_surname[1] == "У" or rand_surname[1] == rand_name[1]:
                    break
        rand.append((rand_name[0],  rand_patro[0], rand_surname[0], rand_name[1]))
    return rand

#делаем массив отчеств. Пользуемся тем, что они упорядочены
def extractPatro(path):
    f = open(path)
    patro = []
    while True:
        line = f.readline()
        if not line:
            break
        comma = line.find(",")
        patro.append((line[1:comma], "М"))
        patro.append((line[comma+2:len(line)-2], "Ж"))
    f.close()
    return patro

#формируем файл с склонениями имен наконец-то
def formFile(path, names):
    f = open(path, 'w')
    maker = PetrovichDeclinationMaker()
    for name in names:
        line = "["
        if name[3] == "М":
            Gen = Gender.MALE
        else:
            Gen = Gender.FEMALE
        line += maker.make(NamePart.FIRSTNAME, Gen, Case.ACCUSATIVE, name[0]) + " "
        line += maker.make(NamePart.MIDDLENAME, Gen, Case.ACCUSATIVE, name[1]) + " "
        line += maker.make(NamePart.LASTNAME, Gen, Case.ACCUSATIVE, name[2]) + "]"
        line += "[" + name[0] + " " + name[1] + " " + name[2] + "]"
        f.write(line + "\n")
    f.close()

rus_names, names_err = makeLists(
    "C:\\Users\\vera\\Documents\\Практика\\База\\База данных имен и фамилий в формате CSV\\russian_names.csv")
rus_surnames, surnames_err = makeLists(
    "C:\\Users\\vera\\Documents\\Практика\\База\\База данных имен и фамилий в формате CSV\\russian_surnames.csv")

#чекнем ошибки:
print(names_err)
print(surnames_err)

#Вроде как отфильтровалось. Попробуем еще раз:
writeSorted(sortByPopularity(rus_names), "sorted_names.txt")
writeSorted(sortByPopularity(rus_surnames), "sorted_surnames.txt")

#это лишний шаг
sorted_names = sortByPopularity(rus_names)
sorted_surnames = sortByPopularity(rus_surnames)

extNames = extractNames(sorted_names)
extSurnames = extractNames(sorted_surnames)

#формируем новые кортежи с склонениями
rNames = formsOfNames(extNames)
#print(rNames)
#print(err)

#на определение пола положиться нельзя, будем брать из базы
#посмотрим, как хорошо мой кустарный метод определяет половую принадлежность фамилий
det_surnames = surnameGenderDet(extSurnames)
#print(det_surnames)

#слишком просто. Проработаем, исключив верно указанные фамилии
count = 0
for surname in det_surnames:
    if not surname[0][len(surname[0])-1] == "в" and not surname[0][len(surname[0])-2:] == "ва" \
            and not surname[0][len(surname[0])-2:] == "ин" and not surname[0][len(surname[0])-3:] == "ина" \
            and not surname[0][len(surname[0])-3:] == "кий" and not surname[0][len(surname[0])-3:] == "кая" \
            and not surname[0][len(surname[0])-3:] == "ный" and not surname[0][len(surname[0])-3:] == "ная" \
            and not surname[0][len(surname[0])-3:] == "цын" and not surname[0][len(surname[0])-4:] == "цына" \
            and not surname[0][len(surname[0])-4:] == "енко" and not surname[0][len(surname[0])-3:] == "чук" \
            and not surname[0][len(surname[0])-2:] == "ич" and not surname[0][len(surname[0])-2:] == "их" \
            and not surname[0][len(surname[0])-2:] == "юк" and not surname[0][len(surname[0])-2:] == "ук" \
            and not surname[0][len(surname[0])-2:] == "ко" and not surname[0][len(surname[0])-3:] == "арь" \
            and not surname[0][len(surname[0])-3:] == "ман" and not surname[0][len(surname[0])-2:] == "ян" \
            and not surname[0][len(surname[0])-2:] == "ли" and not surname[0][len(surname[0])-3:] == "вой" \
            and not surname[0][len(surname[0])-3:] == "вая" and not surname[0][len(surname[0])-3:] == "дзе" \
            and not surname[0][len(surname[0])-2:] == "ик" and not surname[0][len(surname[0])-2:] == "ых" \
            and not surname[0][len(surname[0])-3:] == "вый" and not surname[0][len(surname[0])-2:] == "ер" \
            and not surname[0][len(surname[0])-2:] == "ек" and not surname[0][len(surname[0])-2:] == "ак" \
            and not surname[0][len(surname[0])-2:] == "он" and not surname[0][len(surname[0])-2:] == "як" \
            and not surname[0][len(surname[0])-2:] == "те" and not surname[0][len(surname[0])-2:] == "ах" \
            and not surname[0][len(surname[0])-2:] == "те" and not surname[0][len(surname[0])-2:] == "ус" \
            and not surname[0][len(surname[0])-2:] == "ок" and not surname[0][len(surname[0])-3:] == "ейн" \
            and not surname[0][len(surname[0])-2:] == "нс" and not surname[0][len(surname[0])-2:] == "ас" \
            and not surname[0][len(surname[0])-2:] == "нц" and not surname[0][len(surname[0])-2:] == "иц" \
            and not surname[0][len(surname[0])-2:] == "ык" and not surname[0][len(surname[0])-2:] == "ерг" \
            and not surname[0][len(surname[0])-2:] == "юс" and not surname[0][len(surname[0])-3:] == "айх" \
            and not surname[0][len(surname[0])-2:] == "ун" and not surname[0][len(surname[0])-1:] == "ч" \
            and not surname[0][len(surname[0])-2:] == "ль" and not surname[0][len(surname[0])-2:] == "ло" \
            and not surname[0][len(surname[0])-2:] == "ух" and not surname[0][len(surname[0])-3:] == "ний" \
            and not surname[0][len(surname[0])-3:] == "няя" and not surname[0][len(surname[0])-2:] == "уз" \
            and not surname[0][len(surname[0])-2:] == "ос" and not surname[0][len(surname[0])-3:] == "инг" \
            and not surname[0][len(surname[0])-2:] == "ка" and not surname[0][len(surname[0])-2:] == "ец":
        #print(surname)
        count += 1
#print(count)
#подобным было выделено 92% фамилий. Зачем? Ради науки

#кажется, выделила все генденно определенные окончания. сгенерирую имя-фамилии, чтобы проверить
#some_names = randomName(10, extNames, det_surnames)
#print(some_names)

#обработаем файл с отчествами
with open("C:\\Users\\vera\\Documents\\Практика\\База\\База данных имен и фамилий в формате CSV\\patronyms.txt", encoding='utf-8') as patro_old, open("C:\\Users\\vera\\Documents\\Практика\\База\\База данных имен и фамилий в формате CSV\\patronyms_new.txt", 'w') as patro_new:
    while True:
        line = patro_old.readline()
        if not line:
            break
        b = line.find("(")
        if b == -1:
            continue
        e = line.rfind(")")
        line = line.replace(" и ", ")\n(")
        patro_new.write(line[b:e+1]+'\n')

#проверим отчества
patronyms = extractPatro("C:\\Users\\vera\\Documents\\Практика\\База\\База данных имен и фамилий в формате CSV\\patronyms_new.txt")
#print(patronyms)

#дополним генератор и проверим
some_names = randomName(10, extNames, det_surnames, patronyms)
#print(some_names)

#теперь склоняем
formFile("test.txt", some_names)

maker = PetrovichDeclinationMaker()
