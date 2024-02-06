import sys, re
import telebot
import datetime
from telebot import types
sys.path.insert(0, 'E:\\Job\\Telegram_bot\\DataBase')
from DataBase import Telegram_DB


token = '6850135105:AAFGbka8Bi2tpedXNuMFvEmw-XdNOa6q22g'
bot = telebot.TeleBot(token)
temp_user_data = {}
hide_board = types.ReplyKeyboardRemove()
command_list = ['/start', '/profile']


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if db.user_is_exist(user_id):
        info = db.get_user_info(user_id)
        fio = info[3]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Да')
        markup.add(button)
        mess = bot.send_message(user_id, 'Здравствуйте, {0}. Хотите начать поиск работы?'.format(fio), reply_markup=markup)
        bot.register_next_step_handler(mess, get_job)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Да')
        markup.add(button)
        mess = bot.send_message(user_id, 'Здравствуйте. Мы компания, которая помогает найти работу. Хотите начать?', reply_markup=markup)
        bot.register_next_step_handler(mess, start_reg)

def start_reg(message):
    user_id = message.from_user.id
    temp_user_data[user_id] = {}
    mess = bot.send_message(user_id, 'Хорошо, начнем! Напиши свое ФИО', reply_markup=hide_board)
    bot.register_next_step_handler(mess, process_fio_step)

def process_fio_step(message):
    user_id = message.from_user.id
    if bool(re.match(r'^[а-яА-Я\s]+$', message.text)):
        temp_user_data[user_id]['fio'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_male = types.KeyboardButton('Мужской')
        button_female = types.KeyboardButton('Женский')
        markup.add(button_male, button_female)
        mess = bot.send_message(user_id, 'Выберите ваш пол', reply_markup=markup)
        bot.register_next_step_handler(mess, process_sex_step)
    else:
        mess = bot.send_message(user_id, 'Некорректный ввод. Пожалуйста, введите ваше ФИО', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_fio_step)

def process_sex_step(message):
    user_id = message.from_user.id
    if message.text in ['Мужской', 'Женский']:
        temp_user_data[user_id]['sex'] = message.text
        mess = bot.send_message(user_id, 'Напиши свою дату рождения в формате дд.мм.гггг', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_born_step)
    else:
        mess = bot.send_message(user_id, 'Пожалуйста, выберите один из представленных вариантов ответов')
        bot.register_next_step_handler(mess, process_sex_step)

def process_born_step(message):
    user_id = message.from_user.id
    try:
        datetime.datetime.strptime(message.text, '%d.%m.%Y')
        temp_user_data[user_id]['born'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_school = types.KeyboardButton('Школа')
        button_college = types.KeyboardButton('Среднее профессиональное')
        button_high_school = types.KeyboardButton('Высшее')
        button_student = types.KeyboardButton('Студент')
        markup.add(button_school, button_college, button_high_school, button_student)
        mess = bot.send_message(user_id, 'Выберите уровень вашего образования', reply_markup=markup)
        bot.register_next_step_handler(mess, process_education_level_step)
    except ValueError:
        mess = bot.send_message(user_id, 'Неверная дата, пожалуйства введите дату в соответствии с шаблоном (дд.мм.гггг)')
        bot.register_next_step_handler(mess, process_born_step)

def process_education_level_step(message):
    user_id = message.from_user.id
    if message.text in ['Среднее профессиональное', 'Высшее', 'Студент']:
        temp_user_data[user_id]['education_level'] = message.text
        mess = bot.send_message(user_id, 'Введите специальность обучения', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_education_profession_step)
    elif message.text in ['Школа']:
        temp_user_data[user_id]['education_level'] = message.text
        mess = bot.send_message(user_id, 'Введите контактный номер (формат: 85551116699)', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_phone_step)
    else:
        mess = bot.send_message(user_id, 'Пожалуйста, выберите один из представленных вариантов ответов')
        bot.register_next_step_handler(mess, process_education_level_step)

def process_education_profession_step(message):
    user_id = message.from_user.id
    if bool(re.match(r'^[а-яА-Я\s]+$', message.text)):
        temp_user_data[user_id]['profession'] = message.text
        mess = bot.send_message(user_id, 'Введите контактный номер (формат: 85551116699)', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_phone_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Попробуйте снова')
        bot.register_next_step_handler(mess, process_education_profession_step)

def process_phone_step(message):
    user_id = message.from_user.id
    if bool(re.match(r"^\d+$", message.text)):
        temp_user_data[user_id]['phone'] = message.text
        mess = bot.send_message(user_id, 'Введите дополнительную информацию о себе, которая может быть полезной  подборе работы', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_add_info_step)
    else:
        mess = bot.send_message(user_id, 'Неверный формат, пожалуйства введите номер в соответствии с шаблоном (формат: 85551116699)', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_phone_step)

def process_add_info_step(message):
    user_id = message.from_user.id
    temp_user_data[user_id]['add_information'] = message.text

    fio = temp_user_data[user_id]['fio']
    sex = temp_user_data[user_id]['sex']
    born = temp_user_data[user_id]['born']
    education_level = temp_user_data[user_id]['education_level']
    phone = temp_user_data[user_id]['phone']
    add_information = temp_user_data[user_id]['add_information']

    markup = types.InlineKeyboardMarkup(row_width=1)
    button_save = types.InlineKeyboardButton(text='Все верно', callback_data='save_user')
    button_restart = types.InlineKeyboardButton(text='Заполнить профиль заново', callback_data='restart')
    markup.add(button_save, button_restart)
    try: 
        profession = temp_user_data[user_id]['profession']
        mess = 'Отлично, проверьте правильность данных:\nФИО: {0}\nПол: {1}\nДата рождения: {2}\nОбразование: {3}\nСпециализация: {4}\nТелефон: {5}\nДополнительная информация: {6}'.format(fio, sex, born, education_level, profession, phone, add_information)
    except:
        mess = 'Отлично, проверьте правильность данных:\nФИО: {0}\nПол: {1}\nДата рождения: {2}\nОбразование: {3}\nТелефон: {4}\nДополнительная информация: {5}'.format(fio, sex, born, education_level, phone, add_information)
    bot.send_message(user_id, mess, reply_markup=markup)

def get_job(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Функция еще находится в разработке')


@bot.message_handler(commands=['profile'])
def profile(message):
    user_id = message.from_user.id
    if db.user_is_exist(user_id):
        info = db.get_user_info(user_id)
        data_reg = info[0]
        profit = info[1]
        orders = info[2]
        fio = info[3]
        sex = info[4]
        born = info[5]
        education_level = info[6]
        profession = info[7]
        phone = info[8]
        add_information = info[9]
        try: 
            profession = temp_user_data[user_id]['profession']
            mess = 'Ваш профиль:\nДата регистрации: {0}\nЗаработок: {1}\nВыполненных заказов: {2}\nФИО: {3}\nПол: {4}\nДата рождения: {5}\nОбразование: {6}\nСпециализация: {7}\nТелефон: {8}\nДополнительная информация: {9}'.format(data_reg, profit, orders, fio, sex, born, education_level, profession, phone, add_information)
        except:
            mess = 'Ваш профиль:\nДата регистрации: {0}\nЗаработок: {1}\nВыполненных заказов: {2}\nФИО: {3}\nПол: {4}\nДата рождения: {5}\nОбразование: {6}\nТелефон: {7}\nДополнительная информация: {8}'.format(data_reg, profit, orders, fio, sex, born, education_level, phone, add_information)
        bot.send_message(user_id, text=mess)
    else:
        pass


@bot.callback_query_handler(func= lambda call: True)
def response(callback):
    user_id = callback.from_user.id
    if callback.data == 'start_reg':
        mess = 'Отлично. Для начала необходимо пройти небольшую анкету, чтобы нам было проще подобрать подходящую работу.\nВведите свое ФИО полностью'
        bot.send_message(user_id, text=mess)
        temp_user_data[user_id]['status'] = 'waiting_fio'
    if callback.data == 'save_user':
        data_reg = datetime.date.today()
        fio = temp_user_data[user_id]['fio']
        sex = temp_user_data[user_id]['sex']
        born = temp_user_data[user_id]['born']
        education_level = temp_user_data[user_id]['education_level']
        phone = temp_user_data[user_id]['phone']
        add_information = temp_user_data[user_id]['add_information']
        try:
            if 'profession' in temp_user_data[user_id]:
                profession = temp_user_data[user_id]['profession']
                db.add_user(user_id, data_reg, fio, sex, born, education_level, profession, phone, add_information)
            else:
                db.add_user(user_id, data_reg, fio, sex, born, education_level, 'NULL', phone, add_information)

            temp_user_data.pop(user_id)
            mess = 'Регистрация завершена, перейти к поиску работы?'
            markup = types.InlineKeyboardMarkup()
            button_yes = types.InlineKeyboardButton(text='Да', callback_data='finding_job')
            markup.add(button_yes)
            bot.send_message(user_id, text=mess, reply_markup=markup)
        except:
            bot.send_message(user_id, 'Ошибка. Повторите попытку позже')

        
        
    if callback.data == 'restart':
        temp_user_data[user_id] = {}
        mess = bot.send_message(user_id, 'Хорошо, начнем! Напиши свое ФИО', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_fio_step)
    
    if callback.data == 'finding_job':
        bot.send_message(user_id, 'Функция еще находится в разработке')
            

if __name__ == '__main__':
    db = Telegram_DB()
    bot.infinity_polling()