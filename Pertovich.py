# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from petrovich.main import Petrovich
from petrovich.enums import Case, Gender

p = Petrovich()

print(p.lastname('Алексеев', Case.DATIVE, Gender.MALE))

print(p.lastname('Иванова', Case.GENITIVE, Gender.FEMALE))
#не работает

#https://github.com/petrovich/pytrovich
from pytrovich.enums import NamePart, Gender, Case
from pytrovich.maker import PetrovichDeclinationMaker

maker = PetrovichDeclinationMaker()
print(maker.make(NamePart.FIRSTNAME, Gender.MALE, Case.GENITIVE, "Иван"))  # Ивана
print(maker.make(NamePart.LASTNAME, Gender.MALE, Case.INSTRUMENTAL, "Иванов"))  # Ивановым
print(maker.make(NamePart.MIDDLENAME, Gender.FEMALE, Case.DATIVE, "Ивановна"))  # Ивановне

from pytrovich.detector import PetrovichGenderDetector

detector = PetrovichGenderDetector()
print(detector.detect(firstname="Иван"))  # Gender.MALE
print(detector.detect(firstname="Иван", middlename="Семёнович"))  # Gender.MALE
print(detector.detect(firstname="Арзу", middlename="Лутфияр кызы"))  # Gender.FEMALE

print(maker.make(NamePart.LASTNAME, Gender.MALE, Case.INSTRUMENTAL, "Мамун"))
print(maker.make(NamePart.LASTNAME, Gender.FEMALE, Case.INSTRUMENTAL, "Мамун"))