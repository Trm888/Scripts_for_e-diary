from random import choice

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid, Subject)


def fix_marks(kid_name):  # Функция исправления плохих оценок ученика
    try:
        Mark.objects.filter(points__lte=3).select_related('schoolkid').filter(schoolkid__full_name__contains=kid_name).update(points=5)
    except Schoolkid.DoesNotExist:
        print('ФИО отсутствует в базе данных, попробуйте еще раз')
    except Schoolkid.MultipleObjectsReturned:
        print(
            'Вы ничего не ввели или под данным именем находится много людей,'
            ' попробуйте уточнить запрос и запустить скрипт еще раз')


def remove_chastisements(kid_name):  # Функция удаления всех замечаний ученика
    try:
        kid = Schoolkid.objects.get(full_name__contains=kid_name)
        chastisements_schoolkid = Chastisement.objects.filter(schoolkid=kid.pk)
        chastisements_schoolkid.delete()
    except Schoolkid.DoesNotExist:
        print('ФИО отсутствует в базе данных, попробуйте еще раз')
    except Schoolkid.MultipleObjectsReturned:
        print(
            'Вы ничего не ввели или под данным именем находится много людей,'
            ' попробуйте уточнить запрос и запустить скрипт еще раз')


def create_commendation(kid_name):  # Функция создания похвалы для ученика по случайному предмету
    try:
        options_praise = ["Просто блестяще", "А ты хорош",
                          "Молодец!", "Отлично!", "Хорошо!",
                          "Гораздо лучше, чем я ожидал!",
                          "Ты меня приятно удивил!",
                          "Великолепно!", "Прекрасно!"]
        subjects = Subject.objects.filter(year_of_study=6)
        subjects_names = [subject.title for subject in subjects]
        one_lesson = Lesson.objects.filter(year_of_study=6, group_letter='А',
                                           subject__title=choice(subjects_names)).first()
        kid = Schoolkid.objects.get(full_name__contains=kid_name)
        Commendation.objects.create(text=choice(options_praise),
                                    created=one_lesson.date,
                                    schoolkid=kid,
                                    subject=one_lesson.subject,
                                    teacher=one_lesson.teacher)
    except Schoolkid.DoesNotExist:
        print('ФИО отсутствует в базе данных, попробуйте еще раз')
    except Schoolkid.MultipleObjectsReturned:
        print(
            'Вы ничего не ввели или под данным именем находится много людей,'
            ' попробуйте уточнить запрос и запустить скрипт еще раз')
