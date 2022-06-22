# coding: utf8

import csv
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

rus_names, names_err = makeLists(
    "C:\\Users\\vera\\Documents\\Практика\\База\\База данных имен и фамилий в формате CSV\\russian_names.csv")
rus_surnames, surnames_err = makeLists(
    "C:\\Users\\vera\\Documents\\Практика\\База\\База данных имен и фамилий в формате CSV\\russian_surnames.csv")
for_names, _ = makeLists(
    "C:\\Users\\vera\\Documents\\Практика\\База\\База данных имен и фамилий в формате CSV\\foreign_names.csv")

#чекнем ошибки:
print(names_err)
print(surnames_err)

#Вроде как отфильтровалось. Попробуем еще раз:
writeSorted(sortByPopularity(rus_names), "sorted_names.txt")
writeSorted(sortByPopularity(rus_surnames), "sorted_surnames.txt")

#Настало время Петровича. Вычленю из файла только имена/фамилии, определение пола доверю вшитому детектору
#и просклоняю в родительный падеж

#это лишний шаг
sorted_names = sortByPopularity(rus_names)
sorted_surnames = sortByPopularity(rus_surnames)

extNames = extractNames(sorted_names)
extSurnames = extractNames(sorted_surnames)

#формируем новые кортежи с склонениями
rNames = formsOfNames(extNames)
print(rNames)
#print(err)

#посмотрим, как хорошо определяется пол
#detector = PetrovichGenderDetector()
#print(detector.detect("Иван"))
#print(detector.detect("Мария"))

#на определение пола положиться нельзя, возьмем его из базы