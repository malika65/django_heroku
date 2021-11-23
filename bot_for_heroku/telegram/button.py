import telebot
import config
from telebot import types
from .models import Oblasti,Kenesh,Raiony,City


def gen_markup_main():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton('📜 Бот жөнүндө')
    item2 = types.KeyboardButton('📝 Каттоого киргизүү')
    item3 = types.KeyboardButton('📝 Башынан баштоо')
    markup.add(item1,item2,item3)
    
    return markup

def chose_who():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton('Выбрать по должностям')
    item2 = types.KeyboardButton('Выбрать по областям')
    back = types.KeyboardButton('🏡 Башкы меню')
    markup.add(item1,item2,back)
    
    return markup

def gen_markup_ok():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton("Yes", callback_data="yes"),
    types.InlineKeyboardButton("No", callback_data="no"))
    return markup

def gen_kanal():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(types.InlineKeyboardButton("Телеграм канал", url="https://t.me/msu_union_info"))
    return markup

def admin_panel():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(types.InlineKeyboardButton('Документ + текст', callback_data="doc"),
    types.InlineKeyboardButton('Изображение + текст', callback_data="img"),
    types.InlineKeyboardButton('Текст', callback_data="text"))
    
    return markup

def gen_markup_work():
    markup = types.ReplyKeyboardMarkup(row_width=1,one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('👨🏼‍⚖️ ЖӨБ башчысы')
    itembtn2 = types.KeyboardButton('🏙️ Шаардын мэри')
    itembtn3 = types.KeyboardButton('🏘️ Айылдык кеңештин депутаты')
    itembtn4 = types.KeyboardButton('👨‍💼 Шаардык кеңештин депутаты')
    itembtn5 = types.KeyboardButton('👩‍💼 Муниципалдык кызматкер')
    itembtn6 = types.KeyboardButton('👩‍💼 ФЭО айыл өкмөтүнүн башчысы / мэрия')
    itembtn7 = types.KeyboardButton('Өнөктөш')
    itembtn8 = types.KeyboardButton('Эксперттер')
    itembtn9 = types.KeyboardButton('ЖӨБ Союзунун өкүлү')
    
    back = types.KeyboardButton('🏡 Башкы меню')

    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6,itembtn7,itembtn8,itembtn9,back)
    return markup

def get_work(txt):
    work = {"Өнөктөш":"Өнөктөш","Эксперттер":"Эксперттер","ЖӨБ Союзунун өкүлү":"ЖӨБ Союзунун өкүлү","👨🏼‍⚖️ ЖӨБ башчысы":"ЖӨБ башчысы","🏙️ Шаардын мэри":"Шаардын мэри","🏘️ Айылдык кеңештин депутаты":"Айылдык кеңештин депутаты","👨‍💼 Шаардык кеңештин депутаты":"Шаардык кеңештин депутаты","👩‍💼 Муниципалдык кызматкер":"Муниципалдык кызматкер","👩‍💼 ФЭО айыл өкмөтүнүн башчысы / мэрия":"ФЭО айыл өкмөтүнүн башчысы / мэрия"}
    
    return work[txt]   

def gen_markup_place():
    markup = types.ReplyKeyboardMarkup(row_width=1,one_time_keyboard=True, resize_keyboard=True)
    oblasty = Oblasti.objects.all()
    for i in oblasty:
        markup.add(types.KeyboardButton(str(i)))

    back = types.KeyboardButton('🏡 Башкы меню')
    markup.add(back)
    return markup
    
def get_place(txt):
    oblasty = Oblasti.objects.get(name=txt)
    return oblasty.name


def gen_category():
    markup = types.ReplyKeyboardMarkup(row_width=1,one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Район')
    itembtn2 = types.KeyboardButton('Шаар')
    
    back = types.KeyboardButton('🏡 Башкы меню')

    markup.add(itembtn1, itembtn2,back)
    return markup

def gen_raion(oblast):
    markup = types.ReplyKeyboardMarkup(row_width=1,one_time_keyboard=True, resize_keyboard=True)
    r = Raiony.objects.filter(oblasti__name=oblast)
    for i in r:
        markup.add(types.KeyboardButton(str(i)))
    back = types.KeyboardButton('🏡 Башкы меню')
    markup.add(back)

    return markup

def get_city(oblast):
    markup = types.ReplyKeyboardMarkup(row_width=1,one_time_keyboard=True, resize_keyboard=True)
    r = City.objects.filter(oblasti__name=oblast)
    for i in r:
        markup.add(types.KeyboardButton(str(i)))
    back = types.KeyboardButton('🏡 Башкы меню')
    markup.add(back)
    return markup

def get_kenesh(raion):
    markup = types.ReplyKeyboardMarkup(row_width=1,one_time_keyboard=True, resize_keyboard=True)
    r = Kenesh.objects.filter(raiony__name=raion)
    for i in r:
        markup.add(types.KeyboardButton(str(i)))
    back = types.KeyboardButton('🏡 Башкы меню')
    markup.add(back)
    return markup
    

    

def gen_markup_number():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) #Подключаем клавиатуру
    button_phone = types.KeyboardButton(text="Телефон жөнөтүү", request_contact=True) #Указываем название кнопки, которая появится у пользователя
    markup.add(button_phone) #Добавляем эту кнопку
    
    return markup

