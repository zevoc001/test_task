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

def get_mess_photo(user_id):
    mess = bot.send_message(user_id, 'Отправьте пожалуйста ваше фото', reply_markup=hide_board)
    return mess

def get_mess_fio(user_id):
    mess = bot.send_message(user_id, 'Введите ваше ФИО (полностью)', reply_markup=hide_board)
    return mess

def get_mess_sex(user_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_male = types.KeyboardButton('Мужской')
        button_female = types.KeyboardButton('Женский')
        markup.add(button_male, button_female)
        mess = bot.send_message(user_id, 'Выберите ваш пол', reply_markup=markup)
        return mess

def get_mess_born(user_id):
    mess = bot.send_message(user_id, 'Напиши свою дату рождения в формате дд.мм.гггг', reply_markup=hide_board)
    return mess

def get_mess_education_level(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_school = types.KeyboardButton('Школа')
    button_college = types.KeyboardButton('Среднее профессиональное')
    button_high_school = types.KeyboardButton('Высшее')
    button_student = types.KeyboardButton('Студент')
    markup.add(button_school, button_college, button_high_school, button_student)
    mess = bot.send_message(user_id, 'Выберите уровень вашего образования', reply_markup=markup)
    return mess

def get_mess_course(user_id):
    mess = bot.send_message(user_id, 'Введите номер курса, на котором вы обучаетесь', reply_markup=hide_board)
    return mess

def get_mess_profission(user_id):
    mess = bot.send_message(user_id, 'Введите специальность и место обучения', reply_markup=hide_board)
    return mess

def get_mess_min_salary(user_id):
    mess = bot.send_message(user_id, 'За какую оплату в час вы готовы работать?\nНапишите числом', reply_markup=hide_board)
    return mess

def get_mess_hardwork(user_id, sex):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = types.KeyboardButton('Да')
    btn_no = types.KeyboardButton('Нет')
    markup.add(btn_yes, btn_no)
    mess = bot.send_message(user_id, 'Готовы ли вы выполнять тяжелую работу (копать, ломать, строить)?', reply_markup=markup)
    return mess

def get_mess_midwork(user_id, sex):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = types.KeyboardButton('Да')
    btn_no = types.KeyboardButton('Нет')
    markup.add(btn_yes, btn_no)
    if sex == 'Мужской':
       mess = bot.send_message(user_id, 'Готовы ли вы выполнять средней тяжести (уборка территорий, прочистка труб, и т.д.)?', reply_markup=markup)
       return mess
    else:
        mess = bot.send_message(user_id, 'Готовы ли вы ухаживать за детьми или пожилими людьми?', reply_markup=markup)
        return mess

def get_mess_artwork(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = types.KeyboardButton('Да')
    btn_no = types.KeyboardButton('Нет')
    markup.add(btn_yes, btn_no)
    mess = bot.send_message(user_id, 'Готовы ли вы выполнять творческую работу (аниматорство, ведение соцсетей, фото/видеосъемка и.т.д.)?', reply_markup=markup)
    return mess

def get_mess_addwork(user_id):
    mess = bot.send_message(user_id, 'Напишите, какие иные работы вы готовы выполнять (Если нет иных работ, напишите нет)', reply_markup=hide_board)
    return mess

def get_mess_phone(user_id):
    mess = bot.send_message(user_id, 'Введите ваш контактный номер телефона (формат 89995550011)', reply_markup=hide_board)
    return mess

def get_mess_tools(user_id):
    mess = bot.send_message(user_id, 'Какие инструменты для работы у вас есть (компьютер, дрель, электропила и т.д.)?', reply_markup=hide_board)
    return mess

def get_mess_local(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = types.KeyboardButton('Да')
    btn_no = types.KeyboardButton('Нет')
    markup.add(btn_yes, btn_no)
    mess = bot.send_message(user_id, 'Почти закончили. Хорошо ли вы ориентируетесь в Ставрополе?', reply_markup=markup)
    return mess

def get_mess_final(user_id):
    mess = 'Отлично, давайте еще раз проверим, все ли верно. Вот ваши данные'
    for i in temp_user_data[user_id]:
        if i != 'Фотография':
            data = temp_user_data[user_id][i]
            mess += '\n{}: {}'.format(i, data)
    return mess

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if db.user_is_exist(user_id):
        info = db.get_user_info(user_id)
        fio = info[2]
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
    mess = bot.send_message(user_id, 'Хорошо, приступим! Для продолжения необходимо заполнить небольшую анкету.\nОтправьте пожалуйста свое фото', reply_markup=hide_board)
    bot.register_next_step_handler(mess, process_photo_step)

def process_photo_step(message):
    user_id = message.from_user.id
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        photo = bot.download_file(file_info.file_path)
        temp_user_data[user_id]['Фотография'] = photo
        mess = get_mess_fio(user_id)
        bot.register_next_step_handler(mess, process_fio_step)
    except:
        mess = bot.send_message(user_id, 'Ошибка загрузки! Попробуйте отправить другую фотографию', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_photo_step)

def process_fio_step(message):
    user_id = message.from_user.id
    if bool(re.match(r'^[а-яА-Я\s]+$', message.text)):
        temp_user_data[user_id]['ФИО'] = message.text
        mess = get_mess_sex(user_id)
        bot.register_next_step_handler(mess, process_sex_step)
    else:
        mess = bot.send_message(user_id, ' Пожалуйста, попробуйте ввести ФИО иначе.')
        bot.register_next_step_handler(mess, process_fio_step)

def process_sex_step(message):
    user_id = message.from_user.id
    if message.text in ['Мужской', 'Женский']:
        temp_user_data[user_id]['Пол'] = message.text
        mess = get_mess_born(user_id)
        bot.register_next_step_handler(mess, process_born_step)
    else:
        mess = bot.send_message(user_id, 'Некорректный ввод. Пожалуйста, выберите один из представленных вариантов ответа')
        bot.register_next_step_handler(mess, process_sex_step)

def process_born_step(message):
    user_id = message.from_user.id
    try:
        datetime.datetime.strptime(message.text, '%d.%m.%Y')
        temp_user_data[user_id]['Дата рождения'] = message.text
        mess = get_mess_education_level(user_id)
        bot.register_next_step_handler(mess, process_education_level_step)
    except ValueError:
        mess = bot.send_message(user_id, 'Некорректный ввод. Пожалуйства введите дату в соответствии с шаблоном (дд.мм.гггг)')
        bot.register_next_step_handler(mess, process_born_step)

def process_education_level_step(message):
    user_id = message.from_user.id
    if message.text in ['Среднее профессиональное', 'Высшее']:
        temp_user_data[user_id]['Образование'] = message.text
        mess = get_mess_profission(user_id)
        bot.register_next_step_handler(mess, process_profession_step)
    elif message.text == 'Студент':
        temp_user_data[user_id]['Образование'] = message.text
        mess = get_mess_course(user_id)
        bot.register_next_step_handler(mess, process_course_step)
    elif message.text == 'Школа':
        temp_user_data[user_id]['Образование'] = message.text
        mess = get_mess_min_salary(user_id)
        bot.register_next_step_handler(mess, process_min_salary_step)
    else:
        mess = bot.send_message(user_id, 'Пожалуйста, выберите один из представленных вариантов ответов')
        bot.register_next_step_handler(mess, process_education_level_step)

def process_course_step(message):
    user_id = message.from_user.id
    temp_user_data[user_id]['Курс'] = message.text
    mess = get_mess_profission(user_id)
    bot.register_next_step_handler(mess, process_profession_step)

def process_profession_step(message):
    user_id = message.from_user.id
    if message.text not in command_list:
        temp_user_data[user_id]['Специальность'] = message.text
        mess = get_mess_min_salary(user_id)
        bot.register_next_step_handler(mess, process_min_salary_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Попробуйте снова')
        bot.register_next_step_handler(mess, process_profession_step)

def process_min_salary_step(message):
    user_id = message.from_user.id
    if bool(re.match(r"^\d+$", message.text)):
        temp_user_data[user_id]['Минимальная оплата (в час)'] = message.text
        mess = get_mess_hardwork(user_id, temp_user_data[user_id]['Пол'])
        bot.register_next_step_handler(mess, process_hardwork_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Введите пожалуйста числом')
        bot.register_next_step_handler(mess, process_min_salary_step)

def process_hardwork_step(message):
    user_id = message.from_user.id
    if message.text in ['Да', 'Нет']:
        temp_user_data[user_id]['Тяжелая работа'] = message.text
        mess = get_mess_midwork(user_id,  temp_user_data[user_id]['Пол'])
        bot.register_next_step_handler(mess, process_midwork_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Выберите один из предложенных вариантов ответа')
        bot.register_next_step_handler(mess, process_hardwork_step)

def process_midwork_step(message):
    user_id = message.from_user.id
    if message.text in ['Да', 'Нет']:
        temp_user_data[user_id]['Работа средней сложности'] = message.text
        mess = get_mess_artwork(user_id)
        bot.register_next_step_handler(mess, process_artwork_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Выберите один из предложенных вариантов ответа')
        bot.register_next_step_handler(mess, process_midwork_step)

def process_artwork_step(message):
    user_id = message.from_user.id
    if message.text in ['Да', 'Нет']:
        temp_user_data[user_id]['Творческая работа'] = message.text
        mess = get_mess_addwork(user_id)
        bot.register_next_step_handler(mess, process_addwork_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Выберите один из предложенных вариантов ответа')
        bot.register_next_step_handler(mess, process_artwork_step)

def process_addwork_step(message):
    user_id = message.from_user.id
    temp_user_data[user_id]['Иные работы'] = message.text
    mess = get_mess_tools(user_id)
    bot.register_next_step_handler(mess, process_tools_step)

def process_tools_step(message):
    user_id = message.from_user.id
    temp_user_data[user_id]['Инструменты в наличии'] = message.text
    mess = get_mess_phone(user_id)
    bot.register_next_step_handler(mess, process_phone_step)

def process_phone_step(message):
    user_id = message.from_user.id
    if bool(re.match(r"^\d+$", message.text)):
        temp_user_data[user_id]['Телефон'] = message.text
        mess = get_mess_local(user_id)
        bot.register_next_step_handler(mess, process_local_step)
    else:
        mess = bot.send_message(user_id, 'Неверный формат, пожалуйства введите номер в соответствии с шаблоном (формат: 85551116699)')
        bot.register_next_step_handler(mess, process_phone_step)

def process_local_step(message):
    user_id = message.from_user.id
    if message.text in ['Да', 'Нет']:
        temp_user_data[user_id]['Местный'] = message.text
        photo = temp_user_data[user_id]['Фотография']
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_save = types.KeyboardButton('Сохранить')
        btn_restart = types.KeyboardButton('Заполнить заново')
        markup.add(btn_save, btn_restart)
        mess = bot.send_photo(user_id, photo, get_mess_final(user_id), reply_markup=markup)
        bot.register_next_step_handler(mess, process_save_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Выберите один из предложенных вариантов ответа')
        bot.register_next_step_handler(mess, process_local_step)

def process_save_step(message):
    user_id = message.from_user.id
    if message.text == 'Сохранить':
        data_reg = datetime.date.today()
        photo = temp_user_data[user_id]['Фотография']
        fio = temp_user_data[user_id]['ФИО']
        sex = temp_user_data[user_id]['Пол']
        born = temp_user_data[user_id]['Дата рождения']
        education_level = temp_user_data[user_id]['Образование']
        min_salary = temp_user_data[user_id]['Минимальная оплата (в час)']
        hardwork = temp_user_data[user_id]['Тяжелая работа']
        midwork = temp_user_data[user_id]['Работа средней сложности']
        artwork = temp_user_data[user_id]['Творческая работа']
        addwork = temp_user_data[user_id]['Иные работы']
        tools = temp_user_data[user_id]['Инструменты в наличии']
        phone = temp_user_data[user_id]['Телефон']
        local = temp_user_data[user_id]['Местный']
        if 'Курс' in temp_user_data[user_id]:
            course = temp_user_data[user_id]['Курс']
            if 'Специальность' in temp_user_data[user_id]:
                profession = temp_user_data[user_id]['Специальность']
                db.add_user(user_id, data_reg, photo, fio, sex, born, education_level, course, profession, min_salary, hardwork, midwork, artwork, addwork, tools, phone, local)
            else:
                db.add_user(user_id, data_reg, photo, fio, sex, born, education_level, course, None, min_salary, hardwork, midwork, artwork, addwork, tools, phone, local)
        else:
            db.add_user(user_id, data_reg, photo, fio, sex, born, education_level, None, None, min_salary, hardwork, midwork, artwork, addwork, tools, phone, local)
        mess = 'Отлично, регистрация завершена'
        temp_user_data.pop(user_id)
        bot.send_message(user_id, mess)
    else:
        temp_user_data[user_id] = {}
        mess = bot.send_message(user_id, 'Хорошо, начнем сначала.\nОтправьте пожалуйста свое фото', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_photo_step)

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