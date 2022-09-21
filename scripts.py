from random import choice

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid, Subject)


def fix_marks(kid_name):  # Функция исправления плохих оценок ученика
    try:
        kid = Schoolkid.objects.get(full_name__contains=kid_name)
    except Schoolkid.DoesNotExist:
        print('ФИО отсутствует в базе данных, попробуйте еще раз')
    except Schoolkid.MultipleObjectsReturned:
        print(
            'Вы ничего не ввели или под данным именем находится много людей,'
            ' попробуйте уточнить запрос и запустить скрипт еще раз')
    Mark.objects.filter(schoolkid=kid.pk, points__lte=3).update(points=5)


def remove_chastisements(kid_name):  # Функция удаления всех замечаний ученика
    try:
        kid = Schoolkid.objects.get(full_name__contains=kid_name)
    except Schoolkid.DoesNotExist:
        print('ФИО отсутствует в базе данных, попробуйте еще раз')
    except Schoolkid.MultipleObjectsReturned:
        print('Вы ничего не ввели или под данным именем находится много людей,'
              ' попробуйте уточнить запрос и запустить скрипт еще раз')
    Chastisement.objects.filter(schoolkid=kid.pk).delete()

def create_commendation(kid_name, year_of_study, group_letter):  # Функция создания похвалы для ученика по случайному предмету
    try:
        kid = Schoolkid.objects.get(full_name__contains=kid_name)
    except Schoolkid.DoesNotExist:
        print('ФИО отсутствует в базе данных, попробуйте еще раз')
    except Schoolkid.MultipleObjectsReturned:
        print('Вы ничего не ввели или под данным именем находится много людей,'
              ' попробуйте уточнить запрос и запустить скрипт еще раз')
    commendations = ["Просто блестяще", "А ты хорош",
                     "Молодец!", "Отлично!", "Хорошо!",
                     "Гораздо лучше, чем я ожидал!",
                     "Ты меня приятно удивил!",
                     "Великолепно!", "Прекрасно!"]
    subjects = Subject.objects.filter(year_of_study=year_of_study)
    subjects_names = [subject.title for subject in subjects]
    one_lesson = Lesson.objects.filter(year_of_study=year_of_study, group_letter=group_letter,
                                        subject__title=choice(subjects_names)).first()
    Commendation.objects.create(text=choice(commendations),
                                created=one_lesson.date,
                                schoolkid=kid,
                                subject=one_lesson.subject,
                                teacher=one_lesson.teacher)

