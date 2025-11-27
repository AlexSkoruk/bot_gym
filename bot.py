import sqlite3
import telebot
from telebot import types
import time
from datetime import date
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
token = "5842386849:AAH2bNU6XS9u7VONZoI4gk7KMirf3oFYYGU"
IMG_PATH = "C:\\Users\\Aleks\\Desktop\\bot_gym\\IMG\\"

class Chat:
    def __init__(self, id):
        self.id = id

##class F_R:
##    def __init__(self, id):
##        self.id = id

class Mess:
    def __init__(self, id, text):
        self.chat = Chat(id)
        self.text = text
##        self.kek = 'lel'
##        self.from_user = F_R(id)
        self.content_type = text
        
def my_factory(col,b):
    cols = {}
    for i,name in enumerate(col.description):
        cols[name[0]] = b[i]
    return cols
class App:
    def __init__(self):
        self.bot = telebot.TeleBot(token)
        self.start()

    def gen_markup(self, step = 0, student=None, levels_but=None, targets_but=None, formats_but=None, cities=None, locations_but=None,
                   search=None, have_coach=None, previous_coach=False, qual=None):
        self.keyboard = InlineKeyboardMarkup()
        print(step)
        if step == 0:
            self.keyboard.add(InlineKeyboardButton('Начать', callback_data='start'))
        if step == 1 and student:
            self.keyboard.add(InlineKeyboardButton('Заполнить анкету', callback_data='student_form'))
        if step == -1:
            self.keyboard.add(InlineKeyboardButton('Тренер', callback_data='coach'))
            self.keyboard.add(InlineKeyboardButton('Спортсмен', callback_data='student'))
        if step == 3 and student:
            self.keyboard.add(InlineKeyboardButton ('Да', callback_data='give_contact_yes'))
            self.keyboard.add(InlineKeyboardButton ('Нет', callback_data='give_contact_no'))
        if step == 4 and student:
            self.keyboard.add(InlineKeyboardButton ('Мужчина', callback_data='man'))
            self.keyboard.add(InlineKeyboardButton ('Женщина', callback_data='woman'))
        if step == 5 and student:
            for level in levels_but:
                self.keyboard.add(InlineKeyboardButton(level[0]+1, callback_data='level_{0}'.format(level[1])))
        if step == 6 and student:
            for target in targets_but:
                self.keyboard.add(InlineKeyboardButton(target[0]+1, callback_data='target_student_{0}'.format(target[1])))
##        if step == 7 and student:
##            self.keyboard.add(InlineKeyboardButton('Онлайн', callback_data='training_format_1'))
##            self.keyboard.add(InlineKeyboardButton('Оффлайн', callback_data='training_format_-1'))
##            self.keyboard.add(InlineKeyboardButton('Не важно', callback_data='training_format_0'))
        if step == 8 and student:
            self.keyboard.add(InlineKeyboardButton('Да', callback_data='health_status_1'))
            self.keyboard.add(InlineKeyboardButton('Нет', callback_data='health_status_0'))
##        if (step == 9 or step == 'city') and student:
##            for city in cities:
##                self.keyboard.add(InlineKeyboardButton(city, callback_data='student_city_{0}'.format(city)))
##            self.keyboard.add(InlineKeyboardButton('Другой город', callback_data='student_city_any'))
        if step == 10 and student:
            for location in locations_but:
                self.keyboard.add(InlineKeyboardButton(location[0]+1, callback_data='location_student_{0}'.format(location[1])))

        #QQQQQQQQQQQQQQQQQQ
        if step == 12 and student:
##            if previous_coach:
##                self.keyboard.add(InlineKeyboardButton('Подходит', callback_data='old_match'))
##            else:
##                self.keyboard.add(InlineKeyboardButton('Подходит', callback_data='match'))
            self.keyboard.add(InlineKeyboardButton('Подходит', callback_data='match'))
            self.keyboard.add(InlineKeyboardButton('Не подходит, хочу другого', callback_data='research'))
        if step == 13 and student:
            self.keyboard.add(InlineKeyboardButton('Показать предыдущего тренера', callback_data='previous_coach'))
            self.keyboard.add(InlineKeyboardButton('Отстановить поиск', callback_data='search'))
        if step == 99:
            self.keyboard.add(InlineKeyboardButton('Назад', callback_data='back'))
        if step == 777:
            self.keyboard.add(InlineKeyboardButton('Подобрать тренера', callback_data='search'))
        if step == 999:
##            print(student, '=st')
##            print(search, '=search')
            if student:
                if not have_coach:
                    if not search:
                        self.keyboard.add(InlineKeyboardButton('Подобрать тренера', callback_data='search'))
                    else:
                        self.keyboard.add(InlineKeyboardButton('Отключить поиск', callback_data='search'))
                else:
                    self.keyboard.add(InlineKeyboardButton('Сменить тренера', callback_data='search_another'))
                    self.keyboard.add(InlineKeyboardButton('Мой тренер', callback_data='coach_info'))
                    self.keyboard.add(InlineKeyboardButton('Оказаться от тренера', callback_data='refuse_from_coach'))
                    
            if not student:
                if not search and qual:
                    self.keyboard.add(InlineKeyboardButton('Включить поиск спортсменов', callback_data='activate'))
                elif search:
                    self.keyboard.add(InlineKeyboardButton('Скрыть меня из поиска', callback_data='deactivate'))
                self.keyboard.add(InlineKeyboardButton('Мои спортсмены', callback_data='my_students'))
            self.keyboard.add(InlineKeyboardButton('Моя информация', callback_data='my_info'))
            self.keyboard.add(InlineKeyboardButton('Заполнить анкету заново', callback_data='start'))
            self.keyboard.add(InlineKeyboardButton('Справочник спортсмена', callback_data='reference_book'))

        if step == 100:
            self.keyboard.add(InlineKeyboardButton('Принципы питания', url='https://telegra.ph/Principy-pravilnogo-pitaniya-05-26-2'))
            self.keyboard.add(InlineKeyboardButton('Здоровый сон', url='https://telegra.ph/Zdorovyj-son-05-26'))
            self.keyboard.add(InlineKeyboardButton('Заминка', url='https://telegra.ph/Zaminka-05-27'))
            self.keyboard.add(InlineKeyboardButton('Растяжка и разминка перед тренировкой', url='https://telegra.ph/Rastyazhka-i-razminka-pered-trenirovkoj-05-26'))
            self.keyboard.add(InlineKeyboardButton('Оптимальная длительность тренировки', url='https://telegra.ph/Optimalnaya-dlitelnost-trenirovki-05-26'))
            self.keyboard.add(InlineKeyboardButton('Составление программы тренировок', url='https://telegra.ph/Sostavlenie-programmy-trenirovok-05-26'))
            self.keyboard.add(InlineKeyboardButton('Питание при наборе весе', url='https://telegra.ph/Pitanie-pri-nabore-vese-05-26'))
            self.keyboard.add(InlineKeyboardButton('Питание при похудении', url='https://telegra.ph/Pitanie-pri-pohudenii-05-27'))
            self.keyboard.add(InlineKeyboardButton('Советы начинающим', url='https://telegra.ph/Sovety-nachinayushchim-05-27'))
            self.keyboard.add(InlineKeyboardButton('Назад', callback_data='back'))

        ####coach
        if step == 1 and not student:
            self.keyboard.add(InlineKeyboardButton('Заполнить анкету', callback_data='coach_form'))
        if (step == 4 or step == 'self_photo') and not student:
            self.keyboard.add(InlineKeyboardButton('Не прикреплять фото', callback_data='skip_self_photo'))
        if (step == 5 or step == 'end_self_photo') and not student:
            self.keyboard.add(InlineKeyboardButton('Далее', callback_data='end_self_photo'))
        if (step == 6 or step == 'skip_self_link') and not student:
            self.keyboard.add(InlineKeyboardButton('Не указывать ссылку', callback_data='skip_self_link'))
        if (step == 7 or step == 'qual_photo') and not student:
            self.keyboard.add(InlineKeyboardButton('Не прикреплять фото', callback_data='skip_qual_photo'))
        if (step == 8 or step == 'end_qual_photo') and not student:
            self.keyboard.add(InlineKeyboardButton('Далее', callback_data='end_qual_photo'))
        if (step == 9 or step == 'targets') and not student:
            for target in targets_but:
                self.keyboard.add(InlineKeyboardButton(target[0]+1, callback_data='target_{0}'.format(2 ** target[1])))
            self.keyboard.add(InlineKeyboardButton('Далее', callback_data='target_next_step'))
        if (step == 10 or step == 'locations') and not student:
            for location in locations_but:
                self.keyboard.add(InlineKeyboardButton(location[0]+1, callback_data='location_{0}'.format(2 ** location[1])))
            self.keyboard.add(InlineKeyboardButton('Далее', callback_data='location_next_step'))
        if step == 11 and not student:
            self.keyboard.add(InlineKeyboardButton ('Да', callback_data='disability_1'))
            self.keyboard.add(InlineKeyboardButton ('Нет', callback_data='disability_2'))
        
        
        return self.keyboard
    
    def router(self):
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            print(call.data)
            self.bot.answer_callback_query(call.id, "")
            if call.data == 'start':
                return message_handler(call.message, call.message.chat.id, who=True)
            ###student
            elif call.data == 'student':
                return message_handler(call.message, call.message.chat.id, student=True)
            elif call.data == 'student_form':
                return message_handler(call.message, call.message.chat.id, student_form=True)
            elif call.data == 'give_contact_yes':
                return message_handler(call.message, call.message.chat.id, give_contact_yes=True)
            elif call.data == 'give_contact_no':
                return message_handler(call.message, call.message.chat.id, give_contact_no=True)
            elif call.data == 'man':
                return message_handler(call.message, call.message.chat.id, gender=1)
            elif call.data == 'woman':
                return message_handler(call.message, call.message.chat.id, gender=2)
            elif 'level_' in call.data:
                level = call.data[6:]
                return message_handler(call.message, call.message.chat.id, level=int(level))
            elif 'target_student_' in call.data:
                target = call.data[15:]
                #print(target, 'sdfg')
                return message_handler(call.message, call.message.chat.id, target=int(target))
##            elif 'training_format_' in call.data:
##                training_format = call.data[16:]
##                return message_handler(call.message, call.message.chat.id, training_format=training_format)
            elif 'health_status_' in call.data:
                health_status = call.data[14:]
                return message_handler(call.message, call.message.chat.id, health_status=health_status)
##            elif 'student_city_' in call.data:
##                city = call.data[13:]
##                return message_handler(call.message, call.message.chat.id, student_city=city)
            elif 'location_student_' in call.data:
                location = call.data[17:]
                #print(location, 'sdfg')
                return message_handler(call.message, call.message.chat.id, location=int(location))
            elif call.data == 'my_info':
                call.message.text = 'my_info'
                return message_handler(call.message, call.message.chat.id, my_info=True)
            elif call.data == 'back':
                call.message.text = 'back'
                return message_handler(call.message, call.message.chat.id)
            elif call.data == 'search':
                return message_handler(call.message, call.message.chat.id, search=True)
            elif call.data == 'research':
                return message_handler(call.message, call.message.chat.id, search=True, research=True)
            if call.data == 'match':
                return message_handler(call.message, call.message.chat.id, match=True)
            if call.data == 'coach_info':
                return message_handler(call.message, call.message.chat.id, coach_info=True)
            if call.data == 'search_another':
                return message_handler(call.message, call.message.chat.id, search=True, search_another=True)
##            if call.data == 'old_match':
##                return message_handler(call.message, call.message.chat.id, match=True, previous_coach=True)
            if call.data == 'previous_coach':
                return message_handler(call.message, call.message.chat.id, previous_coach=True)
            if call.data == 'refuse_from_coach':
                return message_handler(call.message, call.message.chat.id, refuse_from_coach=True)
            if call.data == 'reference_book':
                return message_handler(call.message, call.message.chat.id, reference_book=True)
            
            #####coach
            elif call.data == 'coach':
                return message_handler(call.message, call.message.chat.id, coach=True)
            elif call.data == 'coach_form':
                return message_handler(call.message, call.message.chat.id, coach_form=True)
            elif call.data == 'skip_self_photo':
                return message_handler(call.message, call.message.chat.id, skip_self_photo=True)
            elif call.data == 'end_self_photo':
                return message_handler(call.message, call.message.chat.id, end_self_photo=True)
            elif call.data == 'skip_self_link':
                return message_handler(call.message, call.message.chat.id, skip_self_link=True)
            elif call.data == 'skip_qual_photo':
                return message_handler(call.message, call.message.chat.id, skip_qual_photo=True)
            elif call.data == 'end_qual_photo':
                return message_handler(call.message, call.message.chat.id, end_qual_photo=True)
            elif 'target_' in call.data:
                #print(call.data)
                target = call.data[7:]
                if target == 'next_step':
                    return message_handler(call.message, call.message.chat.id, target_next_step=True)
                return message_handler(call.message, call.message.chat.id, target=int(target))
            elif 'location_' in call.data:
                #print(call.data)
                location = call.data[9:]
                if location == 'next_step':
                    return message_handler(call.message, call.message.chat.id, location_next_step=True)
                return message_handler(call.message, call.message.chat.id, location=int(location))
            elif 'disability_' in call.data:
                disability = call.data[11:]
                return message_handler(call.message, call.message.chat.id, disability=disability)
            elif call.data == 'activate':
                return message_handler(call.message, call.message.chat.id, activate=True)
            elif call.data == 'deactivate':
                return message_handler(call.message, call.message.chat.id, deactivate=True)
            elif call.data == 'my_students':
                return message_handler(call.message, call.message.chat.id, my_students=True)

            elif call.data == 'nutrition':
                return message_handler(call.message, call.message.chat.id, nutrition=True)


        @self.bot.message_handler(content_types=['text', 'photo', 'document'])
        def message_handler(message, user_id=None, who=False, coach=False, student=False, student_form=False, give_contact_yes=False,
                            give_contact_no=False, gender=0, level=None, target=None, location=None, training_format=None, health_status=None,
                            student_city=None, city=None, coach_form=False, skip_self_photo=False, end_self_photo=False,
                            skip_self_link=False, skip_qual_photo=False, end_qual_photo=False, target_next_step=False,
                            location_next_step=False, search=False, my_info=False, disability=None, match=False, coach_info=False,
                            search_another=False, previous_coach=False, research=False, refuse_from_coach=False, activate=False, deactivate=False,
                            my_students=False, reference_book=False, nutrition=False):
##            try:
                conn = sqlite3.connect('main.db')
                conn.row_factory = my_factory
                cur = conn.cursor()
                if not user_id:
                    user_id = message.chat.id
                cur.execute('SELECT * FROM students WHERE id = ?', [user_id, ])
                student_data = cur.fetchone()
                cur.execute('SELECT * FROM coaches WHERE id = ?', [user_id, ])
                coach_data = cur.fetchone()
                if coach_data:
                    user_data = coach_data
                    student = False
                elif student_data:
                    user_data = student_data
                    print('match = ', match)
                    student = True
                else:
                    user_data = False
##                if (not user_data and not student and not who):
##                    cur.execute('SELECT * FROM students WHERE id = ?', [user_id, ])
##                    user_data = cur.fetchone()
##                
                if message.text == '/start':
                    cur.execute('SELECT text FROM texts_students WHERE key = "start"')
                    text = cur.fetchone()['text']
                    conn.close()
                    return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup())
                    
                elif who:
                    if coach_data and coach_data == user_data:
    ##                        text += '\nТвой выбор: Тренер'
    ##                        again = 'coach'
                            text = 'Для повторного заполнения анкеты обратитесь к @alexsskoruk'
                            self.bot.send_message(message.chat.id, text)
                            return message_handler(message, user_id)
                    #elif student_data and student_data == user_data:
                    else:
                        cur.execute('SELECT text FROM texts_students WHERE key = "who_are_you"')
                        text = cur.fetchone()['text']
                        conn.close()
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=-1))
                elif coach:
                    today = date.today()
                    cur.execute("INSERT INTO coaches (id, tag, step, date) VALUES (?, ?, 'coach', ?)", [message.chat.id, message.chat.username, today.strftime('%d.%m.%Y'),])
                    conn.commit()
                    cur.execute('SELECT text FROM texts_coaches WHERE key = "coach"')
                    text = cur.fetchone()['text']
                    conn.close()    
                    return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=1, student=False))
                elif student and not user_data:
                    today = date.today()
                    cur.execute("INSERT INTO students (id, tag, step, date) VALUES (?, ?, 'student', ?)", [message.chat.id, message.chat.username, today.strftime('%d.%m.%Y'),])
                    conn.commit()
                    cur.execute('SELECT text FROM texts_students WHERE key = "student"')
                    text = cur.fetchone()['text']
                    conn.close()
                    return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=1, student=True))

                elif student_form:
                    cur.execute('SELECT text FROM texts_students WHERE key = "contact_student"')
                    text = cur.fetchone()['text']
                    cur.execute("""UPDATE students SET step = 'contact_student' WHERE id = ?""", [user_id, ])
                    conn.commit()
                    conn.close()
                    return self.bot.send_message(message.chat.id, text)
                elif coach_form:
                    cur.execute('SELECT text FROM texts_coaches WHERE key = "contact_coach"')
                    text = cur.fetchone()['text']
                    cur.execute("""UPDATE coaches SET step = 'contact_coach' WHERE id = ?""", [user_id, ])
                    conn.commit()
                    conn.close()
                    return self.bot.send_message(message.chat.id, text)

                if message.text:
                    ###coach
                    if user_data['step'] == 'contact_coach':
                        cur.execute('SELECT text FROM texts_coaches WHERE key = "fio"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE coaches SET step = 'fio' , contact = ? WHERE id = ?", [message.text, user_id])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text)
                    elif user_data['step'] == 'fio':
                        cur.execute('SELECT text FROM texts_coaches WHERE key = "birthday"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE coaches SET step = 'birthday' , fio = ? WHERE id = ?", [message.text, user_id])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text)
                    elif user_data['step'] == 'birthday':
                        try:
                            time.strptime(message.text, '%d.%m.%Y')
                        except ValueError:
                            text = "Укажите дату рождения в формате дд.мм.гггг"
                            conn.close()
                            return self.bot.send_message(message.chat.id, text)
                        else:
                            cur.execute('SELECT text FROM texts_coaches WHERE key = "about_you"')
                            text = cur.fetchone()['text']
                            cur.execute("UPDATE coaches SET step = 'about_you', birthday = ? WHERE id = ?", [message.text, user_id])
                            conn.commit()
                            conn.close()
                            return self.bot.send_message(message.chat.id, text)
                    elif user_data['step'] == 'about_you':
                        cur.execute('SELECT text FROM texts_coaches WHERE key = "need_self_photo"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE coaches SET step = 'self_photo', about_you = ? WHERE id = ?", [message.text, user_id])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=4))

                    elif end_self_photo or skip_self_photo:
                        cur.execute('SELECT text FROM texts_coaches WHERE key = "need_self_link"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE coaches SET step = 'self_link' WHERE id = ?", [user_id, ])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=6))
                    elif (message.from_user.id != self.bot.get_me().id and user_data['step'] == 'self_link') or skip_self_link:
                        if skip_self_link:
                            self_link = None
                        else:
                            self_link = message.text
                        cur.execute('SELECT text FROM texts_coaches WHERE key = "bio_text"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE coaches SET step = 'bio_text', self_link = ? WHERE id = ?", [self_link, user_id])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text)
                    elif end_qual_photo or skip_qual_photo:
                        cur.execute('SELECT text FROM texts_coaches WHERE key = "targets"')
                        text = cur.fetchone()['text']
                        cur.execute('SELECT id, text FROM targets')
                        targets = cur.fetchall()
                        targets_but = []
                        for i, target in enumerate(targets):
                            text += '\n{0}) {1}'.format(i+1, target['text'])
                            targets_but.append([i, target['id']])
                        cur.execute("UPDATE coaches SET step = 'targets' WHERE id = ?", [user_id, ])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=9, targets_but=targets_but))
                    elif (message.from_user.id != self.bot.get_me().id and user_data['step'] == 'self_link') or skip_self_link:
                        if skip_self_link:
                            self_link = None
                        else:
                            self_link = message.text
                        #cur.execute('SELECT text FROM texts WHERE key = "QQQQQ"')
                        #text = cur.fetchone()['text']
                        cur.execute("UPDATE coaches SET step = '', self_link = ? WHERE id = ?", [self_link, user_id])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup())
                    elif user_data['step'] == "bio_text":
                        print("F")
                        bio_text = message.text
                        cur.execute('SELECT text FROM texts_coaches WHERE key = "bio_photo"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE coaches SET step = 'bio_photo', bio_text = ? WHERE id = ?", [message.text, user_id])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=7))
                    elif user_data['step'] == 'targets' and not target_next_step:
                        print("target X")
                        cur.execute('SELECT text FROM texts_coaches WHERE key = "targets"')
                        text = cur.fetchone()['text']
                        targets_arr = []
                        targets = user_data['targets']
                        while targets != 0:
                            pw = 1
                            while 2 ** (pw + 1) <= targets:
                                pw += 1
                            if target == 2 ** pw:
                                conn.close()
                                return
                            targets -= 2 ** pw
                            targets_arr.append(2 ** pw)
                        if target:
                            targets_arr.append(target)
                            cur.execute("UPDATE coaches SET 'targets' = targets + ? WHERE id = ?", [target, user_id])
                            conn.commit()
                        cur.execute('SELECT id, text FROM targets')
                        targets = cur.fetchall()
                        conn.close()
                        targets_but = []
                        for i, target in enumerate(targets):
                            text += '\n{0}) {1}'.format(i+1, target['text'])
                            if 2 ** target['id'] in targets_arr:
                                text += '✅'
                            else:
                                targets_but.append([i, target['id']])
                        print(targets_but)

                        return self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text,
                                                          reply_markup=self.gen_markup(step=9, targets_but=targets_but))
                    
                    
                    elif user_data['step'] == 'targets' and target_next_step and user_data['targets'] > 0:
                        print("locations coach")
                        cur.execute('SELECT text FROM texts_coaches WHERE key = "location"')
                        text = cur.fetchone()['text']
                        cur.execute('SELECT id, text FROM locations')
                        locations = cur.fetchall()
                        locations_but = []
                        for i, locations in enumerate(locations):
                            text += '\n{0}) {1}'.format(i+1, locations['text'])
                            locations_but.append([i, locations['id']])
                        cur.execute("UPDATE coaches SET step = 'location' WHERE id = ?", [user_id, ])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=10, locations_but=locations_but))
                    
                    elif user_data['step'] == 'location' and not location_next_step:
                        print("target X")
                        cur.execute('SELECT text FROM texts_coaches WHERE key = "location"')
                        text = cur.fetchone()['text']
                        locations_arr = []
                        locations = user_data['locations']
                        print(locations)
                        while locations != 0:
                            pw = 1
                            while 2 ** (pw + 1) <= locations:
                                pw += 1
                            if location == 2 ** pw:
                                conn.close()
                                return
                            locations -= 2 ** pw
                            locations_arr.append(2 ** pw)
                        if location:
                            locations_arr.append(location)
                            cur.execute("UPDATE coaches SET 'locations' = locations + ? WHERE id = ?", [location, user_id])
                            conn.commit()
                        cur.execute('SELECT id, text FROM locations')
                        locations = cur.fetchall()
                        conn.close()
                        locations_but = []
                        for i, location in enumerate(locations):
                            text += '\n{0}) {1}'.format(i+1, location['text'])
                            if 2 ** location['id'] in locations_arr:
                                text += '✅'
                            else:
                                locations_but.append([i, location['id']])
                        print(locations_but)

                        return self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text,
                                                          reply_markup=self.gen_markup(step=10, locations_but=locations_but))
                    elif user_data['step'] == 'location' and location_next_step and user_data['locations'] > 0:
                        cur.execute('SELECT text FROM texts_coaches WHERE key = "disability"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE coaches SET step = 'disability' WHERE id = ?", [user_id, ])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=11, student=False))
                    elif user_data['step'] == 'disability':
                        cur.execute('SELECT text FROM texts_coaches WHERE key = "thx_for_info"')
                        text = cur.fetchone()['text']
                        if disability == "0":
                            disability_name = "Нет"
                        else:
                            disability_name = "Да"
                        cur.execute("UPDATE coaches SET step = '', disability = ? WHERE id = ?", [disability, user_id])
##                        self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
##                                                   text='Наличие ограничений по здоровью: {0}'.format(status_name))
                        conn.commit()
                        conn.close()
                        self.bot.send_message(message.chat.id, text)
                        user_data['step'] = ''
                        
##                    if user_data['step'] == '' and not my_info and not search and not student:
##                        print('coach')
##                        if user_data['approve_coach']:
##                            text = 'Квалификация: подтверждена\n'
##                            qual = True
##                        else:
##                            text = 'Квалификация: не подтверждена\n'
##                            qual = False
##                        if user_data['active_coach']:
##                            text += 'Поиск спортсменов: активен'
##                            search = True
##                        else:
##                            text += 'Поиск спортсменов: не активен'
##                            search = False
##                        if user_data['approve_coach']:
##                            text += '\nКоличество спортсменов: ' + str(user_data['students_count'])
##                        return self.bot.send_message(message.chat.id, 'Меню:\n' + text, reply_markup=self.gen_markup(step=999, search=search, qual=qual, student=False))            
                        
                    if activate:
                        today = date.today()
                        targets = user_data['targets']
                        targets_arr = []
                        while targets != 0:
                            pw = 1
                            while 2 ** (pw + 1) <= targets:
                                pw += 1
                            targets -= 2 ** pw
                            targets_arr.append(pw)

                        locations = user_data['locations']
                        locations_arr = []
                        while locations != 0:
                            pw = 1
                            while 2 ** (pw + 1) <= locations:
                                pw += 1
                            locations -= 2 ** pw
                            locations_arr.append(pw)


                        today = date.today()
                        born = user_data['birthday'].split('.')
                        born.reverse()
                        born = date(int(born[0]), int(born[1]), int(born[2]))
                        user_data['age'] = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

                        if user_data['self_link'] == None:
                            user_data['self_link'] = 'Не указаны'
                            
                        if user_data['disability'] == 1:
                            user_data['disability'] = 'Да'
                        elif user_data['disability'] == 0:
                            user_data['disability'] = 'Нет'
##                        cur.execute('SELECT text FROM locations WHERE id = ?', [user_data['location'], ])
##                        location = cur.fetchone()['text']
##                        print(location)
##                        user_data['location'] = location
                        
                        if user_data['self_photo']:
                            arr_photo = [open(IMG_PATH + photo, 'rb') for photo in user_data['self_photo'].split(',')]
                            self_photos = [InputMediaPhoto(i) for i in arr_photo]
                            self.bot.send_media_group(message.chat.id, self_photos)
                            for i in arr_photo:
                                i.close()
                        #### active_coach = 0 ?
                        cur.execute('UPDATE coaches SET active_coach = 1 WHERE id = ?', [user_id, ])
                        conn.commit()
                        cur.execute('SELECT id, target, health_status, location FROM students WHERE search = 1 AND (coach == "" OR coach IS NULL)')
                        students = cur.fetchall()
                        user_data['active_coach'] = 1
                        self.bot.send_message(message.chat.id, 'Поиск спортсменов включён')
                        i = 0
                        for student_i in students:
                            if student_i['target'] not in targets_arr:
                                continue
                            if student_i['location'] not in locations_arr:
                                continue
                            if user_data['disability'] == 1 and student_i['health_status'] == 0:
                                continue
                            cur.execute('INSERT INTO matches (coach_id, student_id, date) VALUES(?, ?, ?)', [user_data['id'], student_i['id'], today.strftime('%d.%m.%Y')])
                            cur.execute('UPDATE students SET coach = ? WHERE id = ?', [user_id, student_i['id']])
                            conn.commit()
                            cur.execute('SELECT location from students WHERE id = ?', [student_i['id'], ])
                            id_location = cur.fetchone()['location']
                            print(id_location)
                            cur.execute('SELECT text FROM locations WHERE id = ?', [id_location, ])
                            location = cur.fetchone()['text']
                            print(location)
                            user_data['location'] = location
                            #custom_message = Mess(student_i['id'], 'kryA')
                            #message_handler(custom_message, student_i['id'], match=True)
                            text = 'Ура, мы нашли тебе тренера!\nВот информация о нём:\nИмя: {fio}\nВозраст: {age}\nЗал по адресу: {location}\nКвалификации: {bio_text}\nО себе: {about_you}\nСоцсети: {self_link}\nКонтакт: {contact}\nРаботает с людьми, которые имеют ограничения по здоровью: {disability}'
                            self.bot.send_message(student_i['id'], text.format(**user_data), reply_markup=self.gen_markup(step=12, student=True))
                        conn.close()
                        #return message_handler(message, student=False)
                    if deactivate:
                        if user_data['approve_coach']:
                            cur.execute("UPDATE coaches SET active_coach = 0 WHERE id = ?", [user_id, ])
                            conn.commit()
                            conn.close()
                            user_data['active_coach'] = 0
                            self.bot.send_message(message.chat.id, 'Поиск спортсменов выключён')
                            return message_handler(message, student=False)

                    if my_students:
                        cur.execute('SELECT student_id FROM matches WHERE coach_id = ? AND state = 1', [user_id, ])
                        students_id = cur.fetchall()
                        students = []
                        for i in students_id:
                            cur.execute('SELECT * FROM students WHERE id = ?', [i['student_id']])
                            data = cur.fetchone()
                            students.append(data)
                        if students:
                            i = 1
                            self.bot.send_message(message.chat.id, 'Количество подобранных спортсменов: {0}'.format(len(students_id)))
                            for student in students:
                                text = 'Карточка спортсмена ' + str(i)
                                i += 1
                                text += '\nИмя: {fio}\nВозраст: {age}\nКонтакт: {contact}\nМестоположение зала: {location}\nЦель: {target}\nУровень подготовки: {level}'
                                target = int(student['target'])
                                if student['give_contact'] == 0:
                                    student['contact'] = 'Не указано'
                                    
                                cur.execute('SELECT text FROM targets WHERE id = ?', [target, ])
                                student['target'] = cur.fetchone()['text']
                                cur.execute('SELECT text FROM students_levels WHERE id = ?', [student['level'], ])
                                level = cur.fetchone()['text']
                                student['level'] = level
                                location = int(student['location'])
                                cur.execute('SELECT text FROM locations WHERE id = ?', [location, ])
                                student['location'] = cur.fetchone()['text']                            
                                self.bot.send_message(user_id, text.format(**student))
                            conn.close()
                            return
                        elif students_id:
                            conn.close()
                            return self.bot.send_message(message.chat.id, 'Количество подобранных спортсменов: {0}'.format(len(student_id)))
                        else:
                            conn.close()
                            return self.bot.send_message(message.chat.id, 'Пока спортсмены не подобраны')
#####################################student
                    
                    elif user_data['step'] == 'contact_student':
                        cur.execute('SELECT text FROM texts_students WHERE key = "give_contact"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE students SET step = 'give_contact' , contact = ? WHERE id = ?", [message.text, user_id])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=3, student=True))
                    elif user_data['step'] == 'give_contact' and (give_contact_yes or give_contact_no):
                        if give_contact_yes:
                            cur.execute('SELECT text FROM texts_students WHERE key = "give_contact_yes"')
                            give_contact = 1
                            self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                                       text=message.text+'\nТвой выбор: Да')
                        else:
                            cur.execute('SELECT text FROM texts_students WHERE key = "give_contact_no"')
                            give_contact = 0
                            self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                                       text=message.text+'\nТвой выбор: Нет')
                        text1 = cur.fetchone()['text']
                        cur.execute('SELECT text FROM texts_students WHERE key = "fio_student"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE students SET step = 'fio_student', give_contact = ? WHERE id = ?", [give_contact, user_id])
                        conn.commit()
                        conn.close()
                        self.bot.send_message(message.chat.id, text1)
                        return self.bot.send_message(message.chat.id, text)
                    elif user_data['step'] == 'fio_student':
                        cur.execute('SELECT text FROM texts_students WHERE key = "age"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE students SET step = 'age' , fio = ? WHERE id = ?", [message.text, user_id])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text)
                    elif user_data['step'] == 'age':
                        if not message.text.isdigit():
                            return self.bot.send_message(message.chat.id, 'Укажите возраст цифрами.')
                        cur.execute('SELECT text FROM texts_students WHERE key = "gender"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE students SET step = 'gender' , age = ? WHERE id = ?", [message.text, user_id])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=4, student=True))
                    elif user_data['step'] == 'gender' and gender:
                        cur.execute('SELECT text FROM texts_students WHERE key = "weight"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE students SET step = 'weight' , gender = ? WHERE id = ?", [gender, user_id])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text)
                    elif user_data['step'] == 'weight':
                        if not message.text.isdigit():
                            return self.bot.send_message(message.chat.id, 'Укажите вес цифрами.')
                        cur.execute('SELECT text FROM texts_students WHERE key = "height"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE students SET step = 'height' , weight = ? WHERE id = ?", [message.text, user_id])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text)
                    elif user_data['step'] == 'height':
                        if not message.text.isdigit():
                            return self.bot.send_message(message.chat.id, 'Укажите вес цифрами.')
                        cur.execute('SELECT text FROM texts_students WHERE key = "level"')
                        text = cur.fetchone()['text']
                        cur.execute("UPDATE students SET step = 'level' , height = ? WHERE id = ?", [message.text, user_id])
                        cur.execute('SELECT id, text FROM students_levels')
                        levels = cur.fetchall()
                        levels_but = []
                        for i, level in enumerate(levels):
                            text += '\n{0}) {1}'.format(i+1, level['text'])
                            levels_but.append([i, level['id']])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=5, student=True, levels_but=levels_but))
                    elif user_data['step'] == 'level' and level:
                        cur.execute('SELECT text FROM texts_students WHERE key = "target_student"')
                        text = cur.fetchone()['text']
                        cur.execute('SELECT text FROM students_levels WHERE id = ?', [level, ])
                        level_name = cur.fetchone()['text']
                        cur.execute("UPDATE students SET step = 'target_student', level = ? WHERE id = ?", [level, user_id])

                        cur.execute('SELECT id, text FROM students_targets')
                        targets = cur.fetchall()
                        targets_but = []
                        for i, target in enumerate(targets):
                            text += '\n{0}) {1}'.format(i+1, target['text'])
                            targets_but.append([i, target['id']])
                        
                        conn.commit()
                        conn.close()
                        self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                                   text='Выбранный уровень подготовки: {0}'.format(level_name))
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=6, student=True, targets_but=targets_but))

                    
                    elif user_data['step'] == 'target_student' and target:
                        cur.execute('SELECT text FROM texts_students WHERE key = "health_status"')
                        text = cur.fetchone()['text']
                        cur.execute('SELECT text FROM students_targets WHERE id = ?', [target, ])
                        target_name = cur.fetchone()['text']
                        cur.execute("UPDATE students SET step = 'health_status', target = ? WHERE id = ?", [target, user_id])
                        conn.commit()
                        conn.close()
                        self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                                   text='Выбранная цель тренировок: {0}'.format(target_name))
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=8, student=True))
                    elif user_data['step'] == 'health_status' and health_status:
                        cur.execute('SELECT text FROM texts_students WHERE key = "location_student"')
                        text = cur.fetchone()['text']
                        if health_status == "0":
                            status_name = "Нет"
                        else:
                            status_name = "Да"
                        cur.execute("UPDATE students SET step = 'location_student', health_status = ? WHERE id = ?", [health_status, user_id])

                        cur.execute('SELECT id, text FROM locations')
                        locations = cur.fetchall()
                        locations_but = []
                        for i, location in enumerate(locations):
                            text += '\n{0}) {1}'.format(i+1, location['text'])
                            locations_but.append([i, location['id']])
                        
                        conn.commit()
                        conn.close()
                        self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                                   text='Наличие ограничений по здоровью: {0}'.format(status_name))
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=10, student=True, locations_but=locations_but))
                    elif user_data['step'] == 'location_student' and location:
                        cur.execute('SELECT text FROM texts_students WHERE key = "thx_for_info"')
                        text = cur.fetchone()['text']
                        cur.execute('SELECT text FROM locations WHERE id = ?', [location, ])
                        location_name = cur.fetchone()['text']
                        cur.execute("UPDATE students SET step = 'thx_for_info', location = ? WHERE id = ?", [location, user_id])
                        conn.commit()
                        conn.close()
                        self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                                   text='Выбранное местоположение зала: {0}'.format(location_name))
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=777))
                    elif user_data['step'] == 'thx_for_info':
                        print('подобрать тренера')
                        cur.execute("UPDATE students SET step = '' WHERE id = ?", [user_id, ])
                        conn.commit()
                        
                    elif user_data['step'] == '' and not reference_book and not nutrition and not my_info and not search and (student or not student) and not match and not coach_info and not previous_coach and not refuse_from_coach and not activate:
                        print('пустой шаг')
                        print(user_data)
##                        print(message.kek)
                        if student:
                            print(student)
                            if user_data['search'] == 1:
                                text = 'Поиск включен\nМеню:'
                                search = 1
                            else:
                                text = 'Поиск выключен\nМеню:'
                                search = 0
                            if user_data['coach']:
                                have_coach = True
                            else:
                                have_coach = None
                            return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=999, student=True, search=search, have_coach=have_coach))
                        else:
                            if user_data['approve_coach']:
                                text = 'Квалификация: подтверждена\n'
                                qual = True
                            else:
                                text = 'Квалификация: не подтверждена\n'
                                qual = False
                            if user_data['active_coach']:
                                text += 'Поиск спортсменов: активен'
                                search = True
                            else:
                                text += 'Поиск спортсменов: не активен'
                                search = False
                            if user_data['approve_coach']:
                                text += '\nКоличество спортсменов: ' + str(user_data['students_count'])
                            return self.bot.send_message(message.chat.id, text + '\nМеню:', reply_markup=self.gen_markup(step=999, search=search, qual=qual, student=False))

                    elif search:
                        if user_data['coach']:
                            cur.execute('SELECT state FROM matches WHERE coach_id = ? AND student_id = ?', [user_data['coach'], user_id])
                            state = cur.fetchone()['state']
                            cur.execute('UPDATE matches SET state = -1 WHERE coach_id = ? AND student_id = ?', [user_data['coach'], user_id])
                            cur.execute('UPDATE students SET coach = "" WHERE id = ?', [user_id, ])
                            if state == 1:
                                cur.execute('UPDATE coaches SET students_count = students_count - 1 WHERE id = ?', [user_data['coach'], ])
                            if not search_another:
                                self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                                   text=message.text + '\nТвой выбор: Не подходит')
                        cur.execute('UPDATE students SET search = 1 WHERE id = ?', [user_id, ])
##                        user_data['search'] = 1
                        conn.commit()
                        print('шаг')
                        print('research=', research)
                        if user_data['search'] == 1 and not research:
                            cur.execute('UPDATE students SET search = 0 WHERE id = ?', [user_id, ])
                            text = 'Поиск выключен\nМеню:'
                            search = 0
                            conn.commit()
                        else:
                            cur.execute('UPDATE students SET search = 1 WHERE id = ?', [user_id, ])
                            text = 'Поиск включен\nМеню:'
                            search = 1
                            conn.commit()
                        
                            cur.execute('SELECT * FROM coaches WHERE active_coach = 1 ORDER BY students_count')
                            coaches = cur.fetchall()
                            
                            if not coaches:
                                text = 'Тренер не найден'
                                return self.bot.send_message(message.chat.id, text)
                            
                            for coach in coaches:
                                cur.execute('SELECT * FROM matches WHERE coach_id = ? AND student_id = ?', [coach['id'], user_id])
                                if cur.fetchone():
                                    print('syka')
                                    continue
                                elif user_data['health_status'] == 1 and coach['disability'] == 0:
                                    continue
                                else:
                                    targets = coach['targets']
                                    targets_arr = []
                                    while targets != 0:
                                        pw = 1
                                        while 2 ** (pw + 1) <= targets:
                                            pw += 1
                                        targets -= 2 ** pw
                                        targets_arr.append(pw)
                                    coach['targets'] = targets_arr

                                    locations = coach['locations']
                                    locations_arr = []
                                    while locations != 0:
                                        pw = 1
                                        while 2 ** (pw + 1) <= locations:
                                            pw += 1
                                        locations -= 2 ** pw
                                        locations_arr.append(pw)
                                    coach['locations'] = locations_arr

                                    today = date.today()
                                    born = coach['birthday'].split('.')
                                    born.reverse()
                                    born = date(int(born[0]), int(born[1]), int(born[2]))
                                    coach['age'] = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

                                    if coach['self_link'] == None:
                                        coach['self_link'] = 'Не указаны'
                                        
                                    if user_data['target'] in coach['targets'] and user_data['location'] in coach['locations']:
                                        if coach['disability'] == 1:
                                            coach['disability'] = 'Да'
                                        elif coach['disability'] == 0:
                                            coach['disability'] = 'Нет'
                                    cur.execute('SELECT text FROM locations WHERE id = ?', [user_data['location'], ])
                                    location = cur.fetchone()['text']
                                    print(location)
                                    coach['location'] = location
                                    
                                    if coach['self_photo']:
                                        arr_photo = [open(IMG_PATH + photo, 'rb') for photo in coach['self_photo'].split(',')]
                                        self_photos = [InputMediaPhoto(i) for i in arr_photo]
                                        self.bot.send_media_group(message.chat.id, self_photos)
                                        for i in arr_photo:
                                            i.close()
                                    text = 'Ура, мы нашли тебе тренера!\nВот информация о нём:\nИмя: {fio}\nВозраст: {age}\nЗал по адресу: {location}\nКвалификации: {bio_text}\nО себе: {about_you}\nСоцсети: {self_link}\nКонтакт: {contact}\nРаботает с людьми, которые имеют ограничения по здоровью: {disability}'
                                    self.bot.send_message(message.chat.id, text.format(**coach), reply_markup=self.gen_markup(step=12, student=True))
                                    cur.execute('INSERT INTO matches (coach_id, student_id, date) VALUES(?, ?, ?)', [coach['id'], user_id, today.strftime('%d.%m.%Y')])
                                    cur.execute('UPDATE students SET coach = ? WHERE id = ?', [coach['id'], user_id])
                                    conn.commit()
                                    conn.close()
                                    return
                            else:
                                cur.execute('SELECT text FROM texts_students WHERE key = "prev_coach"')
                                text = cur.fetchone()['text']
                                cur.execute('SELECT id, coach_id FROM matches WHERE student_id = ?', [user_id, ])
                                previous_coach = False
                                if cur.fetchone():
                                    previous_coach = True
                                conn.close()
                                return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=13, previous_coach = True, student=True))
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=999, student=True, search=search))
                    elif previous_coach and not match:
                        print('показать предыдущего тренера')
                        cur.execute('SELECT id, coach_id FROM matches WHERE student_id = ?', [user_id, ])
                        previous_match = cur.fetchall()[-1]
                        cur.execute('UPDATE matches SET state = 0 WHERE id = ?', [previous_match['id'], ])
                        cur.execute('UPDATE students SET coach = ? WHERE id = ?', [previous_match['coach_id'], user_id])
                        cur.execute('SELECT * FROM coaches WHERE id = ?', [previous_match['coach_id'], ])
                        conn.commit()
                        coach = cur.fetchone()
                        targets = coach['targets']
                        targets_arr = []
                        while targets != 0:
                            pw = 1
                            while 2 ** (pw + 1) <= targets:
                                pw += 1
                            targets -= 2 ** pw
                            targets_arr.append(pw)
                        coach['targets'] = targets_arr

                        locations = coach['locations']
                        locations_arr = []
                        while locations != 0:
                            pw = 1
                            while 2 ** (pw + 1) <= locations:
                                pw += 1
                            locations -= 2 ** pw
                            locations_arr.append(pw)
                        coach['locations'] = locations_arr

                        today = date.today()
                        born = coach['birthday'].split('.')
                        born.reverse()
                        born = date(int(born[0]), int(born[1]), int(born[2]))
                        coach['age'] = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

                        if coach['self_link'] == None:
                            coach['self_link'] = 'Не указаны'
                            
                        if user_data['target'] in coach['targets'] and user_data['location'] in coach['locations']:
                            if coach['disability'] == 1:
                                coach['disability'] = 'Да'
                            elif coach['disability'] == 0:
                                coach['disability'] = 'Нет'
                        cur.execute('SELECT text FROM locations WHERE id = ?', [user_data['location'], ])
                        location = cur.fetchone()['text']
                        print(location)
                        coach['location'] = location
                        
                        if coach['self_photo']:
                            arr_photo = [open(IMG_PATH + photo, 'rb') for photo in coach['self_photo'].split(',')]
                            self_photos = [InputMediaPhoto(i) for i in arr_photo]
                            self.bot.send_media_group(message.chat.id, self_photos)
                            for i in arr_photo:
                                i.close()
                        text = 'Ура, мы нашли тебе тренера!\nВот информация о нём:\nИмя: {fio}\nВозраст: {age}\nЗал по адресу: {location}\nКвалификации: {bio_text}\nО себе: {about_you}\nСоцсети: {self_link}\nКонтакт: {contact}\nРаботает с людьми, которые имеют ограничения по здоровью: {disability}'
                        self.bot.send_message(message.chat.id, text.format(**coach), reply_markup=self.gen_markup(step=12, student=True))
                        #cur.execute('INSERT INTO matches (coach_id, student_id, date) VALUES(?, ?, ?)', [coach['id'], user_id, today.strftime('%d.%m.%Y')])
                        cur.execute('UPDATE students SET coach = ? WHERE id = ?', [coach['id'], user_id])
                        conn.commit()
                        conn.close()        
                        return
                    elif match:
                        print('мэтч')
                        cur.execute('SELECT id, coach_id, notification FROM matches WHERE student_id = ? AND state = 0', [user_id, ])
                        data = cur.fetchone()
                        coach_id = data['coach_id']
                        match_id = data['id']
                        notification = data['notification']
                        if not notification:
                            cur.execute('UPDATE matches SET state = 1, notification = 1 WHERE id = ?', [match_id, ])
                        else:
                            cur.execute('UPDATE matches SET state = 1 WHERE id = ?', [match_id, ])
                        cur.execute('UPDATE students SET search = 0 WHERE id = ?', [user_id, ])
                        cur.execute('UPDATE coaches SET students_count = students_count + 1 WHERE id = ?', [coach_id, ])
                        conn.commit()
                        user_data['coach'] = coach_id
                        user_data['search'] = search
                        self.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                                   text=message.text + '\nТвой выбор: Подходит')
##                        if user_data['coach']:
##                            have_coach = True
##                        else:
##                            have_coach = None
                        if not notification:
                            if user_data['give_contact'] == 1:
                                cur.execute('SELECT text FROM texts_coaches WHERE key = "match_with_contact"')
                                text = cur.fetchone()['text']
                                text += '\nИмя: {fio}\nВозраст: {age}\nКонтакт: {contact}\nМестоположение зала: {location}\nЦель: {target}\nУровень подготовки: {level}'
                                target = int(user_data['target'])
                                cur.execute('SELECT text FROM targets WHERE id = ?', [target, ])
                                user_data['target'] = cur.fetchone()['text']
                                cur.execute('SELECT text FROM students_levels WHERE id = ?', [user_data['level'], ])
                                level = cur.fetchone()['text']
                                user_data['level'] = level
                                location = int(user_data['location'])
                                cur.execute('SELECT text FROM locations WHERE id = ?', [location, ])
                                user_data['location'] = cur.fetchone()['text']
                                self.bot.send_message(coach_id, text.format(**user_data), reply_markup=self.gen_markup(step=999, student=False, search=True))
                            else:
                                cur.execute('SELECT text FROM texts WHERE key = "match_without_contact"')
                                text = cur.fetchone()['text']
                                self.bot.send_message(coach_id, text.format(**user_data))
                                #self.bot.send_message(coach_id, 'Меню:', reply_markup=self.gen_markup(step=999, student=False))
                        return self.bot.send_message(message.chat.id, 'Меню:', reply_markup=self.gen_markup(step=999, student=True, have_coach=True)) 

                    elif refuse_from_coach:
                        print('otkaz')
                        cur.execute('SELECT id, coach_id, notification FROM matches WHERE student_id = ? AND state = 1', [user_id, ])
                        data = cur.fetchone()
                        match_id = data['id']
                        coach_id = data['coach_id']
                        cur.execute('UPDATE students SET coach = ?, search = 1 WHERE id = ?', ['', user_id])
                        cur.execute('UPDATE matches SET state = -1 WHERE id = ?', [match_id, ])
                        cur.execute('UPDATE coaches SET students_count = students_count - 1 WHERE id = ?', [coach_id, ])
                        conn.commit()
                        conn.close()
                        self.bot.send_message(message.chat.id, text='Вы отказались от тренера.')
                        return message_handler(message, search=True, student=True)
                        #return self.bot.send_message(message.chat.id, 'Меню:', reply_markup=self.gen_markup(step=999, student=True, have_coach=False, search=False))

                        
                    elif coach_info:
                        cur.execute('SELECT * FROM coaches WHERE id = ?', [user_data['coach'], ])
                        coach = cur.fetchone()
                        targets = coach['targets']
                        targets_arr = []
                        while targets != 0:
                            pw = 1
                            while 2 ** (pw + 1) <= targets:
                                pw += 1
                            targets -= 2 ** pw
                            targets_arr.append(pw)
                        coach['targets'] = targets_arr

                        locations = coach['locations']
                        locations_arr = []
                        while locations != 0:
                            pw = 1
                            while 2 ** (pw + 1) <= locations:
                                pw += 1
                            locations -= 2 ** pw
                            locations_arr.append(pw)
                        coach['locations'] = locations_arr

                        today = date.today()
                        born = coach['birthday'].split('.')
                        born.reverse()
                        born = date(int(born[0]), int(born[1]), int(born[2]))
                        coach['age'] = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

                        if coach['self_link'] == None:
                            coach['self_link'] = 'Не указаны'
                            
                        if user_data['target'] in coach['targets'] and user_data['location'] in coach['locations']:
                            if coach['disability'] == 1:
                                coach['disability'] = 'Да'
                            elif coach['disability'] == 0:
                                coach['disability'] = 'Нет'
                        cur.execute('SELECT text FROM locations WHERE id = ?', [user_data['location'], ])
                        location = cur.fetchone()['text']
                        #print(location)
                        coach['location'] = location
                        
                        if coach['self_photo']:
                            arr_photo = [open(IMG_PATH + photo, 'rb') for photo in coach['self_photo'].split(',')]
                            self_photos = [InputMediaPhoto(i) for i in arr_photo]
                            self.bot.send_media_group(message.chat.id, self_photos)
                            for i in arr_photo:
                                i.close()
                        text = 'Информация о твоём тренере:\nИмя: {fio}\nВозраст: {age}\nЗал по адресу: {location}\nКвалификации: {bio_text}\nО себе: {about_you}\nСоцсети: {self_link}\nКонтакт: {contact}\nРаботает с людьми, которые имеют ограничения по здоровью: {disability}'
                        self.bot.send_message(message.chat.id, text.format(**coach), reply_markup=self.gen_markup(step=99, student=True))
                    elif my_info:
                        print(student_data)
                        if student_data:
                            print('kk')
                            text = 'Контакт: {contact}\nПередавать контакт: {give_contact}\nФИО: {fio}\nВозраст: {age}\nПол: {gender}\nВес: {weight}\nРост: {height}\n' +\
                                   'Ограчиения по здоровью: {health_status}\nУровень подготовки: {level}\nЦель: {target}\nМестоположение зала: {location}'
                            if user_data['give_contact'] == 1:
                                user_data['give_contact'] = 'Да'
                            else:
                                user_data['give_contact'] = 'Нет'
                            if user_data['gender'] == 1:
                                user_data['gender'] = 'Мужской'
                            else:
                                user_data['gender'] = 'Женский'
                            if user_data['health_status'] == "0":
                                user_data['health_status'] = "Нет"
                            else:
                                user_data['health_status'] = "Да"
                            cur.execute('SELECT text FROM students_levels WHERE id = ?', [user_data['level'], ])
                            level = cur.fetchone()['text']
                            user_data['level'] = level
                            target = int(user_data['target'])
                            cur.execute('SELECT text FROM students_targets WHERE id = ?', [target, ])
                            user_data['target'] = cur.fetchone()['text']
                            location = int(user_data['location'])
                            cur.execute('SELECT text FROM locations WHERE id = ?', [location, ])
                            user_data['location'] = cur.fetchone()['text']
                        elif coach_data:
                            text = 'Контакт: {contact}\nФИО: {fio}\nДата рождения: {birthday}\nКвалификация: {bio_text}\nЦели:\n{targets}Местоположение зала:\n{locations}О себе: {about_you}\nСсылки на соцсети: {self_link}\nРаботаешь с людьми, которые имеют ограничения по здоровью: {disability}'
                            if user_data['disability'] == "0":
                                user_data['disability'] = "Нет"
                            else:
                                user_data['disability'] = "Да"
                            targets = user_data['targets']
                            targets_arr = []
                            while targets != 0:
                                pw = 1
                                while 2 ** (pw + 1) <= targets:
                                    pw += 1
                                targets -= 2 ** pw
                                targets_arr.append(pw)
                            targets_text = ''
                            for target in targets_arr:
                                cur.execute('SELECT text FROM targets WHERE id = ?', [target, ])
                                targets_text += cur.fetchone()['text'] + ';\n'
                            user_data['targets'] = targets_text

                            locations = user_data['locations']
                            locations_arr = []
                            while locations != 0:
                                pw = 1
                                while 2 ** (pw + 1) <= locations:
                                    pw += 1
                                locations -= 2 ** pw
                                locations_arr.append(pw)
                            locations_text = ''
                            for location in locations_arr:
                                cur.execute('SELECT text FROM locations WHERE id = ?', [location, ])
                                locations_text += cur.fetchone()['text'] + ';\n'
                            user_data['locations'] = locations_text

                            if user_data['self_link'] == None:
                                user_data['self_link'] = 'Не указаны'
                            if user_data['qual_photo']:
                                arr_photo = [open(IMG_PATH + photo, 'rb') for photo in user_data['qual_photo'].split(',')]
                                qual_photos = [InputMediaPhoto(arr_photo[i], caption = 'Фото квалификации' if i == 0 else '') for i in range(len(arr_photo))]
                                self.bot.send_media_group(message.chat.id, qual_photos)
                                for i in arr_photo:
                                    i.close()
                            if user_data['self_photo']:
                                arr_photo = [open(IMG_PATH + photo, 'rb') for photo in user_data['self_photo'].split(',')]
                                self_photos = [InputMediaPhoto(arr_photo[i], caption = 'Личные фото' if i == 0 else '') for i in range(len(arr_photo))]
                                self.bot.send_media_group(message.chat.id, self_photos)
                                for i in arr_photo:
                                    i.close()
                        return self.bot.send_message(message.chat.id, text.format(**user_data), reply_markup=self.gen_markup(step=99))
                    elif reference_book:
                        text = 'Здесь вы можете найти полезную информацию, связанную со спортом.'
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=100))

                elif (message.content_type == 'photo' or message.content_type == 'document') and user_data['step'] == 'self_photo':
                        if message.content_type == 'photo':
                            file_name = str(user_id) + '_self_photo_' + str(message.message_id) + '.png'
                            file_info = self.bot.get_file(message.photo[-1].file_id)
                            ext = file_info.file_path[file_info.file_path.rfind('.'):]
                            if ext not in ('.png', '.jpg', '.jpeg'):
                                text = 'Не подходящий формат файла. Пожалуйста, отправь фото или нажми кнопку "Не прикреплять фото"'
                                conn.close()
                                return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=4))
                            downloaded_file = self.bot.download_file(file_info.file_path)
                            with open(IMG_PATH + file_name, 'wb') as new_file:
                                new_file.write(downloaded_file)
                            
                        elif message.content_type == 'document':
                            file_name = str(user_id) + '_self_photo_' + str(message.message_id) + '.png'
                            file_info = self.bot.get_file(message.document.file_id)
                            ext = file_info.file_path[file_info.file_path.rfind('.'):]
                            if ext not in ('.png', '.jpg', '.jpeg'):
                                text = 'Не подходящий формат файла. Пожалуйста, отправь фото или нажми кнопку "Не прикреплять фото"'
                                conn.close()
                                return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=4))
                            downloaded_file = self.bot.download_file(file_info.file_path)
                            with open(IMG_PATH + file_name, 'wb') as new_file:
                                new_file.write(downloaded_file)
                        else:
                            file_name = None
                        cur.execute('SELECT text FROM texts_coaches WHERE key = "end_self_photo"')
                        text = cur.fetchone()['text']
                        cur.execute('SELECT * FROM coaches WHERE id = ?', [user_id, ])
                        user_data = cur.fetchone()
                        if user_data['self_photo']:
                            file_name = user_data['self_photo'] + ',' + file_name
                        cur.execute("UPDATE coaches SET self_photo = ? WHERE id = ?", [file_name, user_id])
                        conn.commit()
                        conn.close()
                        return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=5))

                elif (message.content_type == 'photo' or message.content_type == 'document') and user_data['step'] == 'bio_photo':
                    bio = message.caption
                    if message.content_type == 'photo':
                        file_name = str(user_id) + '_qual_photo_' + str(message.message_id) + '.png'
                        file_info = self.bot.get_file(message.photo[-1].file_id)
                        ext = file_info.file_path[file_info.file_path.rfind('.'):]
                        if ext not in ('.png', '.jpg', '.jpeg'):
                            text = 'Не подходящий формат файла. Пожалуйста, отправь фото или нажми кнопку "Не прикреплять фото"'
                            conn.close()
                            return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=6))
                        downloaded_file = self.bot.download_file(file_info.file_path)
                        with open(IMG_PATH + file_name, 'wb') as new_file:
                            new_file.write(downloaded_file)
                    elif message.content_type == 'document':
                        file_name = str(user_id) + '_qual_photo_' + str(message.message_id) + '.png'
                        file_info = self.bot.get_file(message.document.file_id)
                        ext = file_info.file_path[file_info.file_path.rfind('.'):]
                        if ext not in ('.png', '.jpg', '.jpeg'):
                            text = 'Не подходящий формат файла. Пожалуйста, отправь фото или нажми кнопку "Не прикреплять фото"'
                            conn.close()
                            return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=6), parse_mode='HTML')
                        downloaded_file = self.bot.download_file(file_info.file_path)
                        with open(IMG_PATH + file_name, 'wb') as new_file:
                            new_file.write(downloaded_file)
                    cur.execute("UPDATE coaches SET step = 'end_qual_photo', qual_photo = ? WHERE id = ?", [file_name, user_id])
                    conn.commit()
                    cur.execute('SELECT text FROM texts_coaches WHERE key = "end_qual_photo"')
                    text = cur.fetchone()['text']
                    conn.close()
                    return self.bot.send_message(message.chat.id, text, reply_markup=self.gen_markup(step=8))
                
                    
                        
                
                    
                    
                    
                    
                    
##            except Exception as err:
##                print(err)
                conn.close()
                #return self.bot.send_message(366531509, str(err), parse_mode='HTML')
        
            
        
        
    def start(self):
        self.router()
        self.bot.polling(none_stop=True)

app = App()

