import telebot
import config
from telebot import types
from .models import Oblasti,Kenesh,Raiony,City


def gen_markup_main():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton('📜 Бот жөнүндө')
    item2 = types.KeyboardButton('📝 Каттоого киргизүү')
    markup.add(item1,item2)
    
    return markup

def gen_markup_ok():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton("Yes", callback_data="yes"),
    types.InlineKeyboardButton("No", callback_data="no"))
    return markup


def gen_markup_work():
    markup = types.ReplyKeyboardMarkup(row_width=1,one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('👨🏼‍⚖️ Глава МСУ')
    itembtn2 = types.KeyboardButton('🏙️ Мэр города')
    itembtn3 = types.KeyboardButton('🏘️ Депутат айылного кенеша')
    itembtn4 = types.KeyboardButton('👨‍💼 Депутат городского кенеша')
    itembtn5 = types.KeyboardButton('👩‍💼 Муниципальный служащий')
    itembtn6 = types.KeyboardButton('👩‍💼 Начальник ФЭО айыл окмоту/мэрии')
    itembtn7 = types.KeyboardButton('Партнерлор')
    itembtn8 = types.KeyboardButton('Эксперттер')
    itembtn9 = types.KeyboardButton('ЖОБ Союзунун окулу')
    
    back = types.KeyboardButton('🏡 Главное меню')

    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6,itembtn7,itembtn8,itembtn9,back)
    return markup

def get_work(txt):
    work = {"Партнерлор":"Партнерлор","Эксперттер":"Эксперттер","ЖОБ Союзунун окулу":"ЖОБ Союзунун окулу",👨🏼‍⚖️ Глава МСУ":"Глава МСУ","🏙️ Мэр города":"Мэр города","🏘️ Депутат айылного кенеша":"Депутат айылного кенеша","👨‍💼 Депутат городского кенеша":"Депутат городского кенеша","👩‍💼 Муниципальный служащий":"Муниципальный служащий","👩‍💼 Начальник ФЭО айыл окмоту/мэрии":"Начальник ФЭО айыл окмоту/мэрии"}
    
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

