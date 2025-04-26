from datetime import datetime
import telebot
import sql
import map
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os


load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

locations = []


def agree_menu():
    agree = InlineKeyboardMarkup()
    agree.row(InlineKeyboardButton('Да', callback_data='yes'), InlineKeyboardButton('Нет', callback_data='no'))
    return agree


def start_menu():
    start = InlineKeyboardMarkup()
    start.row(InlineKeyboardButton('Отправить местоположение поста ДПС', callback_data='send_marker'))
    start.row(InlineKeyboardButton('Отправить карту нарядов', callback_data='send_custom_map'))
    return start


def back_menu():
    back = InlineKeyboardMarkup()
    back.row(InlineKeyboardButton('Назад', callback_data='back'))
    return back


@bot.message_handler(commands=['start'])
def send_start_message(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=start_menu())


@bot.message_handler(content_types=['location'])
def set_coordinates(coordinates):
    if not hasattr(coordinates, 'location') or not coordinates.location:
        bot.send_message(coordinates.chat.id, "Неверная геопозиция", reply_markup=start_menu())
        return

    lat = coordinates.location.latitude
    lon = coordinates.location.longitude
    time = datetime.fromtimestamp(coordinates.date)
    location = [lat, lon, time]
    try:
        bot.edit_message_text("Получаем геопозицию", coordinates.chat.id, coordinates.message_id - 1)
    except:
        pass
    bot.send_message(coordinates.chat.id,
                     f"Вы уверены, что хотите добавить эти ({lat};{lon}) координаты?",
                     reply_markup=agree_menu()
                     )

    locations.append(location)


@bot.callback_query_handler(
    func=lambda call: call.data in ['yes', 'no'])
def add_coordinates(call):
    bot.answer_callback_query(call.id)
    if call.data == 'yes':
        bot.edit_message_text("Координаты добавлены",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=back_menu())
        try:
            bot.edit_message_text("Успешно", call.message.chat.id, call.message.message_id - 2)
        except:
            pass
        lat = locations[0][0]
        lon = locations[0][1]
        time = locations[0][2].strftime('%d.%m.%Y %H:%M')
        sql.set_data(lat, lon, time, call.from_user.username)
        locations.clear()

    if call.data == 'no':
        bot.edit_message_text('Отправьте геопозицию 📎',
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=back_menu())
        locations.pop()


@bot.callback_query_handler(
    func=lambda call: call.data in ['send_marker', 'send_custom_map', 'back'])
def callback_data_main_menu(call):
    if call.data == 'send_marker':
        reply = bot.edit_message_text('Отправьте геопозицию 📎',
                                      call.message.chat.id,
                                      call.message.message_id,
                                      reply_markup=back_menu())

    if call.data == 'back':
        bot.edit_message_text("Выберите действие",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=start_menu())
    if call.data == 'send_custom_map':
        bot.send_photo(call.message.chat.id, map.generate_static_map())
        bot.edit_message_text('Карта нарядов', call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Выберите действие", reply_markup=start_menu())
    bot.answer_callback_query(call.id)


bot.polling(none_stop=True)
