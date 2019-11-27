#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')

import time
import pyowm
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from datetime import datetime
import random

token = "55cf82ed684ed26c46b847650666c3806ca044ef51fcd21abdbb3d463e178b8b6a379aab729eac80dab99"
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

owm = pyowm.OWM('7f03f55b7ba3837ebc3a345e3f57fb4b', language = "RU")

russian = 'Русский язык'
algebra = 'Алгебра'
chemistry = 'Химия'
proect = 'Проектная деятельность'
literature = 'Литературное чтение'
biology = 'Биология'
kuban = 'Кубановедение'
phys_ra = 'Физическая культура'
geometry = 'Геометрия'
informat = 'Информатика'
obj = 'ОБЖ'
myz = 'Музыка'
physic = 'Физика'
first_in_dz = "Записывайте домашку, по-братски\n\n" # Первое сообщение при отправке домашнего задания
final_in_dz = 'Дуйте выполнять, иначе можно и двойбас получить0)'  # Последнее сообщение после отправки домашнего задания
techno = 'Технология'
english = 'Английский язык'
history = 'История'
geografy = 'География'

# Создаём главную клавиатуру.
def create_keyboard(response):
    keyboard = VkKeyboard(one_time=False)
    
    if response == 'привет' or 'новая возможность':

        # Создание кнопок
        #keyboard.add_button('Домашнее задание', color=VkKeyboardColor.NEGATIVE)
        
        #keyboard.add_line()
        keyboard.add_button('Будет ли завтра дождь?', color=VkKeyboardColor.PRIMARY)

        #keyboard.add_line()
        #keyboard.add_button('Какой сегодня первый урок?', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Какой урок будет первым в...?', color=VkKeyboardColor.POSITIVE)

        #keyboard.add_line()
        #keyboard.add_button('Какой следующий урок?', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Погода', color=VkKeyboardColor.DEFAULT)
        #keyboard.add_button('ФИО учителей', color=VkKeyboardColor.DEFAULT)
        #keyboard.add_button('ГДЗ', color=VkKeyboardColor.NEGATIVE)
        
        #keyboard.add_line()
        #keyboard.add_button('Правила по русскому языку', color=VkKeyboardColor.DEFAULT)

    keyboard = keyboard.get_keyboard()
    return keyboard

# Создаём клавиатуру для запроса "Какой урок будет первым в...?" из главной клавиатуры
def create_keyboard_for_which_yrok(response):
    keyboard = VkKeyboard(one_time=False)
    
    if response == 'какой урок будет первым в...?':

        # Создание кнопок
        keyboard.add_button('Понедельник', color=VkKeyboardColor.POSITIVE)
        
        keyboard.add_line()
        keyboard.add_button('Вторник', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Среда', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Четверг', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Пятница', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Назад', color=VkKeyboardColor.NEGATIVE)

    elif response == 'закрыть':
        print('закрываем клаву')
        return keyboard.get_empty_keyboard()

    keyboard = keyboard.get_keyboard()
    return keyboard

# Отправка сообщений ботом
def send_message(vk_session, id_type, id, message=None, attachment=None, keyboard=None):
    vk_session.method('messages.send',{id_type: id, 'message': message, 'random_id': random.randint(-2147483648, +2147483648), "attachment": attachment, 'keyboard': keyboard})

# Получение событий.
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print('Сообщение пришло в: ' + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
        print('Текст сообщения: ' + str(event.text))
        print(event.user_id)
        response = event.text.lower()
        keyboard = create_keyboard(response)
        second_keyboard = create_keyboard_for_which_yrok(response)
        if event.from_user and not event.from_me:
            
            # Возможности бота
            if response == "привет":
                send_message(vk_session, 'user_id', event.user_id, message='Привет!\nНажимай на нужные тебе появившиеся кнопки.',keyboard=keyboard)
            
            elif response == "новая возможность":
                send_message(vk_session, 'user_id', event.user_id, message='Удачи C:',keyboard=keyboard)
            
            #elif response == 'домашнее задание':
                #homework = """{} - ничего\n{} - номер 215 и 216\n{} - группа Е.В: страница 34, номер 6; группа С.Г: номер 9\n{} - параграф 4\n{} - параграфы 20 и 22
                #{} - ТПО страница 84, работа над ошибками\n\n{}""".format(techno, algebra, english, history, physic, russian, final_in_dz)
                #send_message(vk_session, 'user_id', event.user_id, message=homework,keyboard=keyboard)
            
            elif response == 'погода':
                observation = owm.weather_at_place("Sochi")
                w = observation.get_weather()
                detailed_status = w.get_detailed_status()
                temperature = w.get_temperature('celsius')["temp"]
                if temperature <= 16:
                    send_message(vk_session, 'user_id', event.user_id, message="В Сочи сейчас " + str(temperature) + ' градусов, ' + detailed_status + ". Одевайтесь теплее, а то можно и отморозить себе чо-нибудь ;)")
                else:
                    send_message(vk_session, 'user_id', event.user_id, message="В Сочи сейчас " + str(temperature) + ' градусов, ' + detailed_status + ".")
            
            elif response == 'будет ли завтра дождь?':
                time_user = '2019-11-28 09:00:00+00'
                fc =  owm.three_hours_forecast('Sochi')
                f = fc.will_be_rainy_at(time_user)
                if f == False:
                    time_user = '2019-11-28 12:00:00+00'
                    fc =  owm.three_hours_forecast('Sochi')
                    f = fc.will_be_rainy_at(time_user)
                    if f == False:
                        time_user = '2019-11-28 18:00:00+00'
                        fc =  owm.three_hours_forecast('Sochi')
                        f = fc.will_be_rainy_at(time_user)
                        if f == False:
                            send_message(vk_session, 'user_id', event.user_id, message="По прогнозам дождя завтра не будет.")
                        else:
                            send_message(vk_session, 'user_id', event.user_id, message="По прогнозу дождь будет(в 18:00)")
                    else:
                        send_message(vk_session, 'user_id', event.user_id, message="По прогнозу дождь будет(в 12:00)")
                else:
                    send_message(vk_session, 'user_id', event.user_id, message="По прогнозу дождь будет(в 9:00).")
            
            elif response == 'какой следующий урок?':
                # Понедельник
                if time.strftime("%w", time.localtime()) == '1':
                    if time.strftime("%H", time.localtime()) == '08' and time.strftime("%M", time.localtime()) <= '50':
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет биология.')
                    elif (time.strftime("%H", time.localtime()) == '08' and time.strftime("%M", time.localtime()) > '50') or (time.strftime("%H", time.localtime()) == '9' and time.strftime("%M", time.localtime()) <= '45'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет алгебра.')
                    elif (time.strftime("%H", time.localtime()) == '09' and time.strftime("%M", time.localtime()) > '45') or (time.strftime("%H", time.localtime()) == '10' and time.strftime("%M", time.localtime()) <= '25'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет английсий язык.')
                    elif (time.strftime("%H", time.localtime()) == '10' and time.strftime("%M", time.localtime()) > '40') or (time.strftime("%H", time.localtime()) == '11' and time.strftime("%M", time.localtime()) <= '30'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет химия.')
                    elif (time.strftime("%H", time.localtime()) == '11' and time.strftime("%M", time.localtime()) > '30') or (time.strftime("%H", time.localtime()) == '12' and time.strftime("%M", time.localtime()) <= '20'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет русский язык.')
                    elif (time.strftime("%H", time.localtime()) == '12' and time.strftime("%M", time.localtime()) > '20') or (time.strftime("%H", time.localtime()) == '13' and time.strftime("%M", time.localtime()) <= '0'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет география. Это будет последний урок на сегодняшний день :)')
                    else:
                       send_message(vk_session, 'user_id', event.user_id, message='Эта функция начинает работать только в 8:00 и перестаёт работать в 13:00(если уроков 7) или 12:10(если уроков 6)') 
                # Вторник
                elif time.strftime("%w", time.localtime()) == '2':
                    if time.strftime("%H", time.localtime()) == '08' and time.strftime("%M", time.localtime()) <= '50':
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет биология.')
                    elif (time.strftime("%H", time.localtime()) == '08' and time.strftime("%M", time.localtime()) > '50') or (time.strftime("%H", time.localtime()) == '9' and time.strftime("%M", time.localtime()) <= '45'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет алгебра.')
                    elif (time.strftime("%H", time.localtime()) == '09' and time.strftime("%M", time.localtime()) > '45') or (time.strftime("%H", time.localtime()) == '10' and time.strftime("%M", time.localtime()) <= '25'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет кубановедение.')
                    elif (time.strftime("%H", time.localtime()) == '10' and time.strftime("%M", time.localtime()) > '40') or (time.strftime("%H", time.localtime()) == '11' and time.strftime("%M", time.localtime()) <= '30'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет химия.')
                    elif (time.strftime("%H", time.localtime()) == '11' and time.strftime("%M", time.localtime()) > '30') or (time.strftime("%H", time.localtime()) == '12' and time.strftime("%M", time.localtime()) <= '20'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет физическая культура.')
                    elif (time.strftime("%H", time.localtime()) == '12' and time.strftime("%M", time.localtime()) > '20') or (time.strftime("%H", time.localtime()) == '13' and time.strftime("%M", time.localtime()) <= '0'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет проектная деятельность. Это будет последний урок на сегодняшний день :)')
                    else:
                       send_message(vk_session, 'user_id', event.user_id, message='Эта функция начинает работать только в 8:00 и перестаёт работать в 13:00(если уроков 7) или 12:10(если уроков 6)') 
                # Среда
                elif time.strftime("%w", time.localtime()) == '3':
                    if time.strftime("%H", time.localtime()) == '08' and time.strftime("%M", time.localtime()) <= '50':
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет физика.')
                    elif (time.strftime("%H", time.localtime()) == '08' and time.strftime("%M", time.localtime()) > '50') or (time.strftime("%H", time.localtime()) == '9' and time.strftime("%M", time.localtime()) <= '45'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет литературное чтение.')
                    elif (time.strftime("%H", time.localtime()) == '09' and time.strftime("%M", time.localtime()) > '45') or (time.strftime("%H", time.localtime()) == '10' and time.strftime("%M", time.localtime()) <= '25'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет музыка.')
                    elif (time.strftime("%H", time.localtime()) == '10' and time.strftime("%M", time.localtime()) > '40') or (time.strftime("%H", time.localtime()) == '11' and time.strftime("%M", time.localtime()) <= '30'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет информатика.')
                    elif (time.strftime("%H", time.localtime()) == '11' and time.strftime("%M", time.localtime()) > '30') or (time.strftime("%H", time.localtime()) == '12' and time.strftime("%M", time.localtime()) <= '20'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет ОБЖ. Это будет последений урок на сегодняшний день :)\nДуй на перемене быстрее к кабинету, иначе можно пилюлей получить00))')
                    else:
                       send_message(vk_session, 'user_id', event.user_id, message='Эта функция начинает работать только в 8:00 и перестаёт работать в 13:00(если уроков 7) или 12:10(если уроков 6)') 
                # Четверг
                elif time.strftime("%w", time.localtime()) == '4':
                    if time.strftime("%H", time.localtime()) == '08' and time.strftime("%M", time.localtime()) <= '50':
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет английский язык.')
                    elif (time.strftime("%H", time.localtime()) == '08' and time.strftime("%M", time.localtime()) > '50') or (time.strftime("%H", time.localtime()) == '9' and time.strftime("%M", time.localtime()) <= '45'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет история.')
                    elif (time.strftime("%H", time.localtime()) == '09' and time.strftime("%M", time.localtime()) > '45') or (time.strftime("%H", time.localtime()) == '10' and time.strftime("%M", time.localtime()) <= '25'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет физика.')
                    elif (time.strftime("%H", time.localtime()) == '10' and time.strftime("%M", time.localtime()) > '40') or (time.strftime("%H", time.localtime()) == '11' and time.strftime("%M", time.localtime()) <= '30'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет русский язык.')
                    elif (time.strftime("%H", time.localtime()) == '11' and time.strftime("%M", time.localtime()) > '30') or (time.strftime("%H", time.localtime()) == '12' and time.strftime("%M", time.localtime()) <= '20'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет алгебра. Это будет последний урок на сегодяшний день :).')
                    else:
                       send_message(vk_session, 'user_id', event.user_id, message='Эта функция начинает работать только в 8:00 и перестаёт работать в 13:00(если уроков 7) или 12:10(если уроков 6)') 
                # Пятница
                elif time.strftime("%w", time.localtime()) == '5':
                    print('начнем')
                    if time.strftime("%H", time.localtime()) == '08' and time.strftime("%M", time.localtime()) <= '50':
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет геометрия.')
                    elif (time.strftime("%H", time.localtime()) == '08' and time.strftime("%M", time.localtime()) > '50') or (time.strftime("%H", time.localtime()) == '9' and time.strftime("%M", time.localtime()) <= '45'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет обществознание.')
                    elif (time.strftime("%H", time.localtime()) == '09' and time.strftime("%M", time.localtime()) > '45') or (time.strftime("%H", time.localtime()) == '10' and time.strftime("%M", time.localtime()) <= '25'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет русский язык.')
                    elif (time.strftime("%H", time.localtime()) == '10' and time.strftime("%M", time.localtime()) > '40') or (time.strftime("%H", time.localtime()) == '11' and time.strftime("%M", time.localtime()) <= '30'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет история.')
                    elif (time.strftime("%H", time.localtime()) == '11' and time.strftime("%M", time.localtime()) > '30') or (time.strftime("%H", time.localtime()) == '12' and time.strftime("%M", time.localtime()) <= '20'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет физическая культура.')
                    elif (time.strftime("%H", time.localtime()) == '12' and time.strftime("%M", time.localtime()) > '20') or (time.strftime("%H", time.localtime()) == '13' and time.strftime("%M", time.localtime()) <= '0'):
                        send_message(vk_session, 'user_id', event.user_id, message='Следующим уроком по расписанию будет география. Это будет последний урок на сегодняшний день :)')
                    else:
                        send_message(vk_session, 'user_id', event.user_id, message='Эта функция начинает работать только в 8:00 и перестаёт работать в 13:00(если уроков 7) или 12:10(если уроков 6)')
                else:
                    send_message(vk_session, 'user_id', event.user_id, message='Эта функция работает только с понедельника по пятницу.')
            
            #elif response == 'гдз':
                #send_message(vk_session, 'user_id', event.user_id, message='ГДЗ на вторник:\n\n' + \
                #literature + " - читай иди то, что задали\n" + \
                #biology + " - иди читай параграфы, чёрт побери\n" + \
                #algebra + " - номер 208 - https://clck.ru/K5KUL , номер 227 - https://clck.ru/K5KXD , номер 228 - https://clck.ru/K5KYC\n")
                #english + " - группа Е.В: - дуй учить диалог, ГДЗ не поможет; группа С.Г: https://www.euroki.org/gdz/ru/angliyskiy/8_klass/e_vaulina_d_duli_v_jevans_o_podoljanko_9_fgos/zadanie-str-47\np.s: 8 и 9 номера\n" + \
                #chemistry + " - если лень писать самому, то спиши чтоль у кого-нибудь\n" + \
                #russian + " - https://gdz.ru/class-8/russkii_yazik/shmelev/2-chapter-103/\n" + \
                #geografy + " - ничего не задали")

            # Для этого запроса используется вторая клавиатура - second_keyboard.
            elif response == 'какой урок будет первым в...?':
                send_message(vk_session, 'user_id', event.user_id, message='Выбирай нужную кнопочку. Нажав, например, на "Понедельник", я напишу тебе какой будет урок будет первым в этот день недели.\n\nКнопка "Назад" вернёт тебя в первое меню.',keyboard=second_keyboard)
            elif response == 'понедельник':
                send_message(vk_session, 'user_id', event.user_id, message="В понедельник первым уроком будет литературное чтение.")
            elif response == 'вторник':
                send_message(vk_session, 'user_id', event.user_id, message="Во вторник первым уроком будет русский язык.")
            elif response == 'среда':
                send_message(vk_session, 'user_id', event.user_id, message="В среду первым уроком будет геометрия.")
            elif response == 'четверг':
                send_message(vk_session, 'user_id', event.user_id, message="В четверг первым уроком будет технология.")
            elif response == 'пятница':
                send_message(vk_session, 'user_id', event.user_id, message="В пятницу первым уроком будет английский язык.")
            elif response == 'назад':
                send_message(vk_session, 'user_id', event.user_id, message="Возвращаю тебя в главное меню.",keyboard=keyboard)

        print('-' * 30)
