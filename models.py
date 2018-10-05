from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=64, verbose_name="player name")
    nickname = models.CharField(max_length=35, null=True, verbose_name="nickname")

    def __str__(self):
        return self.name

MENTAL_STATE = [
    (1, "Zombie"),
    (2, "Snięta ryba"),
    (3, "Nie za wesoło, jakoś tak pffff"),
    (4, "Jako tako, można by rzec, nieźle"),
    (5, "Zacnie. jak sama nazwa wskazuje"),
    (6, "Żyleta. Idziesz zdobywać świat"),
]

SLEEP_STATE = [
    (1, "Totalny brak snu"),
    (2, "Poważny niedobór snu"),
    (3, "Lekki niedobór snu"),
    (4, "W sam raz snu"),
    (5, "Więcej niż w sam raz"),
    (6, "Max snu")
]

KNOWLEDGE_STATE = [
    (1, "Nieogar total"),
    (2, "Coś tam się wie, aczkolwiek niewiele"),
    (3, "Lekki niedobór wiedzy"),
    (4, "Ogarnia się już trochę"),
    (5, "Się dobrze ogarnia"),
    (6, "Max wiedzy")
]
class PlayerStats(models.Model):
    sleep_state = models.IntegerField(choices=SLEEP_STATE, default=3, verbose_name="Stan wyspania")
    mental_state = models.IntegerField(choices=MENTAL_STATE, default=3, verbose_name="Stan umysłu")
    knowledge_state = models.IntegerField(choices=KNOWLEDGE_STATE, default=3, verbose_name="Stan wiedzy")
    stats = models.OneToOneField(Player, on_delete=models.CASCADE)


PARTS = [
    (1, "ranek dnia pierwszego, Kukurykuuu!!"), (2, "popołudnie dnia pierwszego"), (3, "piękny wtorkowy poranek"),
    (4, "spoko wtorkowy przedwieczór"), (5, "ranek we środę"),(6, "wieczór we środę"), (7, "czwartek rano trochę łooo"),
    (8, "czwartek wieczór. Co, stresik?A może to strach?"), (9, """Dzień 5, poranek. Judgement day: Egzamin z 
    Podstaw Pajthona"""), (10, "evening_day 5"), (11, "morning day 6"),
    (12, "evening_day 6"), (13, "morning day 7"), (14, "evening_day 7"), (15, "morning day 8"), (16, "evening_day 8"), (17, "morning day 9"),
    (18, "evening_day 9"), (19, "morning day 10"), (20, "evening_day 10"), (21, "morning day 11"), (22, "evening_day 11"), (23, "morning day 12"),
    (24, "evening_day 12"), (25, "morning day 13"), (26, "evening_day 13"), (27, "morning day 14"), (28, "evening_day 14"), (29, "morning day 15"),
    (30, "evening_day 15"), (31, "morning day 16"), (32, "evening_day 16"), (33, "morning day 17"), (34, "evening_day 17"), (35, "morning day 18"),
    (36, "evening_day 18"), (37, "morning day 19"), (38, "evening_day 19"), (39, "morning day 20"), (40, "evening_day 20"), (41, "morning day 21"),
    (42, "evening_day 21"),
]
class CourseProgress(models.Model):
    day_of_course = models.IntegerField(choices=PARTS, default=1, verbose_name="Data:")
    related_to = models.OneToOneField(Player, on_delete=models.CASCADE, verbose_name="Przypisane do gracza: ")


EXAMS = [
    (1, "Podstawy pajtona."),
    (2, "Obiektówka i bazy danych."),
    (3, "Django."),
    (4, "JavaScript."),
    (5, "Zaawansowane Django.")
]

RESULT = [
    (1, "Totalne zero - do poprawki. Mentor płakał, jak sprawdzał."),
    (2, "5 punktów - do poprawki, nie przejmuj się."),
    (3, "9,5 punkta - prawie się udało. Poprawka to będzie formalność. Chyba..."),
    (4, "12 punktów - Udało Ci się! Na krawędzi, ale do przodu. Jest nad czym popracować."),
    (5, "15 punktów - Nieźle. Pewniak wzięty. Kilka detali."),
    (6, "18 punktów - Nieźle! Jakby tylko Ci się wtedy nie wykrzaczyło tam na końcu..."),
    (7, "20 punktów - Maksimum punktów. Wszystko cacy. Gratulacje!"),
]
class Exams(models.Model):
    exam = models.IntegerField(choices=EXAMS, default=1, verbose_name="Nazwa egzaminu:")
    relation = models.ForeignKey(to=Player, on_delete=models.CASCADE, verbose_name="Przypisz egzamin do:")

class ExamResult(models.Model):
    result = models.IntegerField(choices=RESULT, default=1)
    related_to = models.OneToOneField(Player, on_delete=models.CASCADE)