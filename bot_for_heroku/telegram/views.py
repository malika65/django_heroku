from telebot import TeleBot, types
from rest_framework.response import Response
from rest_framework.views import APIView
import telebot
from telebot import types
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
    gen_raion,
    get_place,
    get_work,
    get_kenesh,
    gen_category,
    get_city,
    admin_panel,
    chose_who,
    gen_kanal
)


bot = telebot.TeleBot(settings.TOKEN)
  
links = {"ЖӨБ башчысы":"https://t.me/joinchat/Pug4_9U3A403ZTY6",
"Шаардын мэри":"https://t.me/joinchat/bAhpq76qt0AyYTky",
"Айылдык кеңештин депутаты":"https://t.me/joinchat/uhr3HwTpvXo3NzBi",
"Шаардык кеңештин депутаты":"https://t.me/joinchat/q-XXDpdckdRkODNi",
"Муниципалдык кызматкер":"https://t.me/joinchat/hQ25EcquKttlMGJi",
"ФЭО айыл өкмөтүнүн башчысы / мэрия":"https://t.me/joinchat/O5Gb9mwAczM4NTA6",
"Өнөктөш":"https://t.me/msu_union_info",
"Эксперттер":"https://t.me/msu_union_info",
"ЖОБ Союзунун окулу":"https://t.me/msu_union_info"}

class UpdateBot(APIView):
    def post(self, request,):
        # Сюда должны получать сообщения от телеграм и далее обрабатываться ботом
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])
 
        return Response({'code': 200})



user_dict = {}
distribut_dict = {}

class User:
    
    def __init__(self, fullname):
        self.fullname = fullname
        keys = ['place','raion','phone','doljnost','city','kenesh']
        for key in keys:
            self.key = None

class Distribution:
    
    def __init__(self, method):
        self.method = method
        keys = ['docum','whome','doljnost','oblast','text']
        for key in keys:
            self.key = None


# если /help, /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Саламатсызбы "
    + message.from_user.first_name
    + ", мен ботмун, эмнени билгиңиз келет?", reply_markup=gen_markup_main())

    bot.send_message(message.chat.id, "Бардык окуялардан кабардар болуп туруу үчүн биздин телеграм каналыбызга өтүңүз"
    , reply_markup=gen_kanal())

    bot.send_message(message.chat.id, "https://www.youtube.com/watch?v=knpNbLKO0QA")

    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            

# /about
@bot.message_handler(commands=['about'])
def send_about(message):

    bot.send_message(message.chat.id,"Бул бот сизге каттоого кирүүгө жардам берип, топко кошулуу үчүн шилтемени жөнөтөт.")
    

# /admin
@bot.message_handler(commands=['admin'])
def send_admin(message):
    bot.send_message(settings.CHAT_ID,"Создавайте рассылки пользователям вашего бота",reply_markup=admin_panel())
  

# /register
@bot.message_handler(commands=["register"])
def user_reg(message):
    if People.objects.filter(p_id=message.chat.id).exists():
        msg = bot.send_message(message.chat.id, 'Сиз буга чейин катталгансыз.')
    else:
        markup = types.ReplyKeyboardRemove(selective=False)
        msg = bot.send_message(message.chat.id, 'Урматтуу колдонуучу, өзүңүздүн маалыматыңызды туура киргизиңиз.Болбосо, сиздин арызыңыз каралбайт жана сиз КР ЖӨБ Союзунун топторуна кошула албайсыз.')
        msg = bot.send_message(message.chat.id, 'Фамилиясы Аты Атасынын аты.',reply_markup=markup)
        
        bot.register_next_step_handler(msg, process_fullname_step)
       
def process_fullname_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = People(p_id=chat_id,name=message.text)
    
        msg = bot.send_message(chat_id, '\"Телефон жөнөтүү\" баскычын басыңыз.',reply_markup=gen_markup_number())
        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        print(e)
        bot.reply_to(message, '🔠 Текст киргизиңиз')
        msg = bot.send_message(message.chat.id, 'Фамилиясы Аты Атасынын аты.')
        bot.register_next_step_handler(msg, process_fullname_step)
        
def process_phone_step(message):
    try:
        if message.text == '🏡 Башкы меню':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" категорияны тандаңыз",reply_markup=gen_markup_main())
        else:

            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.telephone = message.contact.phone_number
            
            msg = bot.send_message(chat_id, 'Ээлеген кызматы',reply_markup=gen_markup_work())
            bot.register_next_step_handler(msg, process_work_step)
                
    except Exception as e:
        print(e)
        msg = bot.reply_to(message, 'Сиз башкабир нерсени киргиздиңиз. Сураныч,телефон  номерин киргизиңиз.')
        msg = bot.send_message(chat_id, '\"Телефон жөнөтүү\" баскычын басыңыз.',reply_markup=gen_markup_number())
        bot.register_next_step_handler(msg, process_phone_step)

def process_work_step(message):
    try:
        if message.text == '🏡 Башкы меню':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" категорияны тандаңыз",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.doljnost = get_work(message.text) 
            
            # удалить старую клавиатуру
            markup = types.ReplyKeyboardRemove(selective=False)

            msg = bot.send_message(chat_id, 'Област',reply_markup=gen_markup_place())
            bot.register_next_step_handler(msg, process_place_step)

    except Exception as e:
        bot.reply_to(message, 'Сураныч, астындагы тизмеден тандаңыз')
        msg = bot.send_message(chat_id, 'Ээлеген кызматы',reply_markup=gen_markup_work())
        bot.register_next_step_handler(msg, process_work_step)
        
def process_place_step(message):
    try:
        if message.text == '🏡 Башкы меню':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" категорияны тандаңыз",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.oblast = get_place(message.text)

            msg = bot.send_message(chat_id, 'Категорияны тандаңыз',reply_markup=gen_category())
            bot.register_next_step_handler(msg, process_city_or_raion)

    except Exception as e:
        bot.reply_to(message, 'Сураныч, астындагы тизмеден тандаңыз')
        msg = bot.send_message(chat_id, 'Област',reply_markup=gen_markup_place())
        bot.register_next_step_handler(msg, process_place_step)

def process_city_or_raion(message):
    try:
        if message.text == '🏡 Башкы меню':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" категорияны тандаңыз",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            oblast = user.oblast          
            
            if message.text == 'Шаар':
                msg = bot.send_message(chat_id, 'Шаар тандаңыз',reply_markup=get_city(oblast))
                bot.register_next_step_handler(msg, process_save_city_or_obl)
            elif message.text == 'Район':
                msg = bot.send_message(chat_id, 'Район тандаңыз',reply_markup=gen_raion(oblast))
                bot.register_next_step_handler(msg, process_raion)

    except Exception as e:
        print(e)
        bot.reply_to(message, 'Сураныч, астындагы тизмеден тандаңыз')
        msg = bot.send_message(chat_id, 'Категорияны тандаңыз',reply_markup=gen_category())
        bot.register_next_step_handler(msg, process_city_or_raion)

def process_raion(message):
    try:
        if message.text == '🏡 Башкы меню':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" категорияны тандаңыз",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.raion = message.text

            msg = bot.send_message(chat_id, 'Мэрия / айыл өкмөттү тандаңыз:',reply_markup=get_kenesh(message.text))
            bot.register_next_step_handler(msg, process_kenesh)
            
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Сураныч, астындагы тизмеден тандаңыз')
        msg = bot.send_message(chat_id, 'Категорияны тандаңыз',reply_markup=gen_category())
        bot.register_next_step_handler(msg, process_city_or_raion)

def process_kenesh(message):
    try:
        if message.text == '🏡 Башкы меню':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" категорияны тандаңыз",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.kenesh = message.text
            user.save()
            
        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, ' Сиздин отүнмө', message.from_user.first_name), parse_mode="Markdown",reply_markup=gen_markup_main())
        bot.send_message(chat_id, getRegData(user, ' Сиздин отүнмөңүз кабыл алынганда, сизге билдирүү келет '), parse_mode="Markdown",reply_markup=gen_markup_main())

        # отправить админу
        try:
            bot.send_message(settings.CHAT_ID, getRegData(user, 'Боттон отүм', bot.get_me().username), parse_mode="Markdown",reply_markup=gen_markup_ok())
        except Exception as e:
            print(e)
                
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Сураныч, астындагы тизмеден тандаңыз')
        msg = bot.send_message(chat_id, 'Категорияны тандаңыз',reply_markup=gen_category())
        bot.register_next_step_handler(msg, process_city_or_raion)
        
def process_save_city_or_obl(message):
    try:
        if message.text == '🏡 Башкы меню' or message.text == '📝 Башынан баштоо':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" категорияны тандаңыз",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            user = user_dict[chat_id]
            user.city = message.text
            user.save()
            
        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, ' Сиздин отүнмө', message.from_user.first_name), parse_mode="Markdown",reply_markup=gen_markup_main())
        bot.send_message(chat_id, getRegData(user, ' Сиздин отүнмөңүз кабыл алынганда, сизге билдирүү келет '), parse_mode="Markdown",reply_markup=gen_markup_main())
        
        # отправить админу
        try:
            bot.send_message(settings.CHAT_ID, getRegData(user, 'Боттон отүм', bot.get_me().username), parse_mode="Markdown",reply_markup=gen_markup_ok())
        except Exception as e:
            print(e)
                
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Сураныч, астындагы тизмеден тандаңыз')
        msg = bot.send_message(chat_id, 'Категорияны тандаңыз',reply_markup=gen_category())
        bot.register_next_step_handler(msg, process_city_or_raion)
        


# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template('$title *$name* \n ФИО: *$fullname* \n Телефон: *$phone* \n Кесиби: *$doljnost* \n Жашаган жери: *$place* \n Шаар: *$city* \n Район : *$raion* \n Мэрия / айыл өкмөтү: : *$kenesh* \n ID: *$p_id*')

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
    if message.text=='📜 Бот жөнүндө':
        send_about(message)    
    elif message.text=='📝 Каттоого киргизүү':
        user_reg(message)
    elif message.text=='🏡 Башкы меню':
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        bot.send_message(message.chat.id, message.from_user.first_name+" категорияны тандаңыз",reply_markup=gen_markup_main())
    else:
        bot.send_message(message.chat.id, 'Бул бот сизге каттоого кирүүгө жардам берип, топко кошулуу үчүн шилтемени жөнөтөт',reply_markup=gen_markup_main())
        

def add_text(message):
    try:
        if message.text == '🏡 Башкы меню' or message.text == '📝 Башынан баштоо':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" категорияны тандаңыз",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            
            distribution = distribut_dict[chat_id]
            distribution.text = message.text
            if distribution.method == 'doc':
                msg = bot.send_message(message.chat.id, 'Выберите файл с устройства')
                bot.register_next_step_handler(msg,docum_send)
            elif distribution.method == 'img':
                msg = bot.send_message(message.chat.id, 'Выберите изображение с устройства')
                bot.register_next_step_handler(msg,photo_send)
            elif distribution.method == 'text':
                msg = bot.send_message(message.chat.id, "Выберите кому отправить",reply_markup=chose_who())
                bot.register_next_step_handler(msg, choose_whome)

    except Exception as e:
        print(e)
        msg = bot.reply_to(message, 'Введите описание вашей рассылки')
        bot.register_next_step_handler(msg, add_text)
        
def docum_send(message):
    try:
        if message.text == '🏡 Башкы меню' or message.text == '📝 Башынан баштоо':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" категорияны тандаңыз",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            distribution = distribut_dict[chat_id]
           
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = 'C:/Users/Lenovo/itrun/msu_bot/bot_for_heroku/telegram/distribution/' + message.document.file_name;
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            distribution.docum = downloaded_file

            msg = bot.send_message(message.chat.id, "Выберите кому отправить",reply_markup=chose_who())
            bot.register_next_step_handler(msg, choose_whome)

    except Exception as e:
        print(e)
        msg = bot.reply_to(message, 'Выберите файл с устройства')
        bot.register_next_step_handler(msg, docum_send)

def photo_send(message):
    try:
        if message.text == '🏡 Башкы меню' or message.text == '📝 Башынан баштоо':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" категорияны тандаңыз",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            distribution = distribut_dict[chat_id]
            
            distribution.docum = message.photo[0].file_id
            
            msg = bot.send_message(message.chat.id, "Выберите кому отправить",reply_markup=chose_who())
            bot.register_next_step_handler(msg, choose_whome)

    except Exception as e:
        print(e)
        msg = bot.reply_to(message, 'Выберите файл с устройства')
        bot.register_next_step_handler(msg, docum_send)



def choose_whome(message):
    try:
        if message.text == '🏡 Башкы меню' or message.text == '📝 Башынан баштоо':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" категорияны тандаңыз",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id

            distribution = distribut_dict[chat_id]
            distribution.whome = message.text

            if distribution.whome == 'Выбрать по должностям':
                msg = bot.send_message(message.chat.id, "Выберите кому отправить",reply_markup=gen_markup_work())
                bot.register_next_step_handler(msg,send_dist)

            elif distribution.whome == 'Выбрать по областям':
                msg = bot.send_message(message.chat.id, "Выберите куда отправить",reply_markup=gen_markup_place())
                bot.register_next_step_handler(msg,send_dist)

    except Exception as e:
        print(e)
        msg = bot.reply_to(message, 'Выберите кому отправить')
        bot.register_next_step_handler(msg, choose_whome)

def send_dist(message):
    try:
        if message.text == '🏡 Башкы меню' or message.text == '📝 Башынан баштоо':
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            bot.send_message(message.chat.id, message.from_user.first_name+" категорияны тандаңыз",reply_markup=gen_markup_main())
        else:
            chat_id = message.chat.id
            distribution = distribut_dict[chat_id]
            if distribution.whome == 'Выбрать по должностям':
                users = People.objects.filter(doljnost=get_work(message.text))
            elif distribution.whome == 'Выбрать по областям':
                users = People.objects.filter(oblast=message.text)
            for user in users:
                try:
                    if distribution.method == 'doc':
                        bot.send_message(user.p_id,distribution.text)
                        bot.send_document(user.p_id, distribution.docum,parse_mode="Markdown")
                    elif distribution.method == 'img':
                        bot.send_message(user.p_id,distribution.text)
                        bot.send_photo(user.p_id, photo=distribution.docum, caption=message.caption)
                    elif distribution.method == 'text':
                        bot.send_message(user.p_id,distribution.text)
                       
                except Exception as e:
                    continue
        bot.send_message(settings.CHAT_ID, "Рассылка была отправлена всем выбраным пользователям",reply_markup=gen_markup_main())

            
    except Exception as e:
        print(e)
        msg = bot.reply_to(message, 'Выберите кому отправить')
        bot.register_next_step_handler(msg, choose_whome)
        
    
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    try:
        if call.data == 'yes':
            person = People.objects.get(p_id=call.message.text.split("ID:",1)[1].strip())
            person.sale = True
            person.save()
            bot.send_message(person.p_id,'Өтүнмөңүз жактырылды.Топко кошулуу үчүн шилтемени басыңыз :'+links[person.doljnost])

            bot.send_message(message.chat.id, "Бардык окуялардан кабардар болуп туруу үчүн биздин телеграм каналыбызга өтүңүз"
            , reply_markup=gen_kanal())
            
        elif call.data == 'no':
            person = People.objects.get(p_id=call.message.text.split("ID:",1)[1].strip())
            bot.send_message(person.p_id,'Өтүнмөңүз четке кагылды.Толтуруп жатканда туура эмес маалыматтарды киргизгендирсиз.')
            person.delete()

        elif call.data == 'doc':
            try:
                msg = bot.send_message(call.message.chat.id, 'Введите описание вашей рассылки')
                chat_id = call.message.chat.id
                distribut_dict[chat_id] = Distribution(call.data)
                bot.register_next_step_handler(msg,add_text)
            except Exception as e:
                print("Excelent")
                print(e)
                
        elif call.data == 'img':
            msg = bot.send_message(call.message.chat.id, 'Введите описание вашей рассылки')
            distribut_dict[call.message.chat.id] = Distribution(call.data)
            bot.register_next_step_handler(msg,add_text)
        elif call.data == 'text':
            msg = bot.send_message(call.message.chat.id, 'Введите описание вашей рассылки')
            distribut_dict[call.message.chat.id] = Distribution(call.data)
            bot.register_next_step_handler(msg,add_text)
    except Exception as e:
        print(e)

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

