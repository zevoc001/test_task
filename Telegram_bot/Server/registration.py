

def fio_step(message, next_func):
    user_id = message.from_user.id
    if bool(re.match(r'^[а-яА-Я\s]+$', message.text)):
        temp_user_data[user_id]['fio'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_male = types.KeyboardButton('Мужской')
        button_female = types.KeyboardButton('Женский')
        markup.add(button_male, button_female)
        mess = bot.send_message(user_id, 'Выберите ваш пол', reply_markup=markup)
        
    else:
        mess = bot.send_message(user_id, 'Некорректный ввод. Пожалуйста, введите ваше ФИО', reply_markup=hide_board)
        bot.register_next_step_handler(mess, guest_fio_step)