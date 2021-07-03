from telebot import TeleBot, types
from rest_framework.response import Response
from rest_framework.views import APIView
import telebot
from django.conf import settings
from bot.models import People
from telebot import types
from string import Template
from .button import (
    gen_markup_ok,
    gen_markup_main,
    gen_markup_work,
    gen_markup_number,
    gen_markup_place,
    gen_markup_submenu,
    gen_raion,
    get_place,
    get_work,
    get_raion,
    gen_category
)


bot = telebot.TeleBot(settings.TOKEN)
  
links = {"Глава МСУ":"https://t.me/joinchat/Pug4_9U3A403ZTY6",
"Мэр города":"https://t.me/joinchat/bAhpq76qt0AyYTky",
"Депутат айылного кенеша":"https://t.me/joinchat/uhr3HwTpvXo3NzBi",
"Депутат городского кенеша":"https://t.me/joinchat/q-XXDpdckdRkODNi",
"Муниципальный служащий":"https://t.me/joinchat/hQ25EcquKttlMGJi",
"Начальник ФЭО айыл окмоту/мэрии":"https://t.me/joinchat/O5Gb9mwAczM4NTA6"}

class UpdateBot(APIView):
    def post(self, request,):
        # Сюда должны получать сообщения от телеграм и далее обрабатываться ботом
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])
 
        return Response({'code': 200})



user_dict = {}

class User:
    
    def __init__(self, fullname):
        self.fullname = fullname
        keys = ['place','raion','phone','doljnost','city','kenesh']
        for key in keys:
            self.key = None


# если /help, /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    
    bot.send_message(message.chat.id, "Здравствуйте "
    + message.from_user.first_name
    + ", я бот, чтобы вы хотели узнать?", reply_markup=gen_markup_main())
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            

# /about
@bot.message_handler(commands=['about'])
def send_about(message):

    bot.send_message(message.chat.id, "Здесь вы можете зарегистрироваться и получить ссылку на группу , в которую хотите вступить")
    

# /register
@bot.message_handler(commands=["register"])
def user_reg(message):
    if People.objects.filter(p_id=message.chat.id).exists():
        msg = bot.send_message(message.chat.id, 'Вы уже зарегистрированы.')
    else:
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id, 'Уважаемый пользователь, вводите ваши верные данные. В ином случае ваша заявка не будет рассмотрена и вы не получите доступ к группам')
        msg = bot.send_message(message.chat.id, 'Фамилия Имя Отчество',reply_markup=markup)
        
        bot.register_next_step_handler(msg, process_fullname_step)
       
def process_fullname_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = People(p_id=chat_id,name=message.text)
    
        msg = bot.send_message(chat_id, 'Номер телефона',reply_markup=gen_markup_number())
        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        print(e)
        bot.reply_to(message, '🔠 Введите текст')
        msg = bot.send_message(message.chat.id, 'Фамилия Имя Отчество')
        bot.register_next_step_handler(msg, process_fullname_step)
        
def process_phone_step(message):
    try:
        if message.text == '🏡 Главное меню':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" выберите категорию",reply_markup=gen_markup_main())
        else:

            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.telephone = message.contact.phone_number
            
            msg = bot.send_message(chat_id, 'Занимаемая должность',reply_markup=gen_markup_work())
            bot.register_next_step_handler(msg, process_work_step)
                
    except Exception as e:
        print(e)
        msg = bot.reply_to(message, 'Вы ввели что то другое. Пожалуйста введите номер телефона.')
        msg = bot.send_message(chat_id, 'Нажмите на кнопку \'Отправить телефон\'',reply_markup=gen_markup_number())
        bot.register_next_step_handler(msg, process_phone_step)

def process_work_step(message):
    try:
        if message.text == '🏡 Главное меню':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" выберите категорию",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.doljnost = get_work(message.text) 
            
            # удалить старую клавиатуру
            markup = types.ReplyKeyboardRemove(selective=False)

            msg = bot.send_message(chat_id, 'Область',reply_markup=gen_markup_place())
            bot.register_next_step_handler(msg, process_place_step)

    except Exception as e:
        bot.reply_to(message, 'Пожалуйста выберите что-то из списка ниже')
        msg = bot.send_message(chat_id, 'Занимаемая должность',reply_markup=gen_markup_work())
        bot.register_next_step_handler(msg, process_work_step)
        
def process_place_step(message):
    try:
        if message.text == '🏡 Главное меню':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" выберите категорию",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.oblast = get_place(message.text)

            msg = bot.send_message(chat_id, 'Выберите категорию',reply_markup=gen_category())
            bot.register_next_step_handler(msg, process_city_or_raion)

    except Exception as e:
        bot.reply_to(message, 'Пожалуйста выберите что-то из списка ниже')
        msg = bot.send_message(chat_id, 'Область',reply_markup=gen_markup_place())
        bot.register_next_step_handler(msg, process_place_step)

def process_city_or_raion(message):
    try:
        if message.text == '🏡 Главное меню':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" выберите категорию",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            oblast = user.oblast          
            
            msg = bot.send_message(chat_id, 'Выберите место работы',reply_markup=gen_raion(oblast, message.text))
            if message.text == 'Город':
                bot.register_next_step_handler(msg, process_save_city_or_obl)
            elif message.text == 'Район':
                bot.register_next_step_handler(msg, process_raion)

    except Exception as e:
        print(e)
        bot.reply_to(message, 'Пожалуйста выберите что-то из списка ниже')
        msg = bot.send_message(chat_id, 'Выберите категорию',reply_markup=gen_category())
        bot.register_next_step_handler(msg, process_save_city_or_obl)

def process_raion(message):
    try:
        if message.text == '🏡 Главное меню':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" выберите категорию",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.raion = message.text
            
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Пожалуйста выберите что-то из списка ниже')
        msg = bot.send_message(chat_id, 'Выберите категорию',reply_markup=gen_category())
        bot.register_next_step_handler(msg, process_city_or_raion)

def process_kenesh(message):
    try:
        if message.text == '🏡 Главное меню':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" выберите категорию",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.kenesh = message.text
            
        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, ' Ваша заявка', message.from_user.first_name), parse_mode="Markdown",reply_markup=gen_markup_main())
        
        # отправить админу
        try:
            bot.send_message(settings.CHAT_ID, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown",reply_markup=gen_markup_ok())
        except Exception as e:
            print(e)
                
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Пожалуйста выберите что-то из списка ниже')
        msg = bot.send_message(chat_id, 'Выберите категорию',reply_markup=gen_category())
        bot.register_next_step_handler(msg, process_city_or_raion)
        
def process_save_city_or_obl(message):
    try:
        if message.text == '🏡 Главное меню':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" выберите категорию",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.city = message.text
            user.save()
            
        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, ' Ваша заявка', message.from_user.first_name), parse_mode="Markdown",reply_markup=gen_markup_main())
        
        # отправить админу
        try:
            bot.send_message(settings.CHAT_ID, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown",reply_markup=gen_markup_ok())
        except Exception as e:
            print(e)
                
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Пожалуйста выберите что-то из списка ниже')
        msg = bot.send_message(chat_id, 'Выберите категорию',reply_markup=gen_category())
        bot.register_next_step_handler(msg, process_city_or_raion)
        


# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template('$title *$name* \n ФИО: *$fullname* \n Телефон: *$phone* \n Род деятельности: *$doljnost* \n Место проживания: *$place* \n Город: *$city* \n Район : *$raion* \n Кенеш : *$kenesh* \n ID: *$p_id*')

    return t.substitute({
        'title': title,
        'p_id':user.p_id,
        'name': name,
        'fullname': user.name,
        'phone': user.telephone ,
        'doljnost': user.doljnost,
        'place':user.oblast,
        'city':user.city,
        'raion':user.raion,
        'kenesh':user.kenesh
    })

# произвольный текст
@bot.message_handler(content_types=["text"])
def send_help(message):
    if message.text=='📜 О боте':
        send_about(message)    
    elif message.text=='📝 Регистрация':
        user_reg(message)
    elif message.text=='🏡 Главное меню':
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.send_message(message.chat.id, message.from_user.first_name+" выберите категорию",reply_markup=gen_markup_main())
    else:
        bot.send_message(message.chat.id, 'Здесь вы можете зарегистрироваться и получить ссылку на группу , в которую хотите вступить',reply_markup=gen_markup_main())
        

        
# произвольное фото
@bot.message_handler(content_types=["photo"])
def send_help_text(message):
    bot.send_message(message.chat.id, 'Напишите текст')
    

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'yes':
        person = People.objects.get(p_id=call.message.text.split("ID:",1)[1].strip())
        person.sale = True
        person.save()
        bot.send_message(person.p_id,'Ваша заявка была одобрена.Перейдите по ссылке чтобы вступить в группу :'+links[person.doljnost])
    elif call.data == 'no':
        person = People.objects.get(p_id=call.message.text.split("ID:",1)[1].strip())
        bot.send_message(person.p_id,'Ваша заявка была отклонена. Возможно при заполнении вы ввели некорректные данные.')
        person.delete()

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

