import random
from telebot import *
import telebot

from constants import *
bot = telebot.TeleBot("5910953607:AAGp0eV6OPwZRDbIKtih8EiZ6SZAAR_J65w")

users = {}
registered_users = {}
reff = {}
# Handler for the /start and /help commands
tyype = ""
rewards_list = {
    "10": ["100 Birr Card", "150 Min voice"],
    "25": ["200 Birr Card", "250 Min voice"],
    "100": ["itel A33", "1 year unlimited internet premium"]
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if message.text.startswith('/start '):
        referral_code = message.text.split(' ')[1]
        print(referral_code)
        u_id = reff[referral_code]
        if referral_code in reff and user_id not in users[u_id]["referrals"] and user_id not in users:
            # get the user who referred the new user
            users[u_id]["coins"] += 10
            users[u_id]["referrals"].append(user_id)
        # increment the referral count for the referrer
        bot.reply_to(
            message, hello["ENGLISH"])
        return
    if user_id not in registered_users:
        bot.reply_to(
            message,  hello["ENGLISH"])
    else:
        bot.reply_to(
            message, hello_word[users[user_id]['Lang']].format(users[user_id]['first_name']))

# Handler for the /register command


@bot.message_handler(commands=['register'])
def register_user(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name if message.from_user.last_name else ""

    if user_id not in registered_users:
        users[user_id] = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "iid": 1,
            "score": 0,
            "Lang": "ENGLISH",
            "rewarded": [],

            'referral_code': ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=6)),
            'coins': 0,
            'referrals': [],

        }
        reff[users[user_id]['referral_code']] = user_id
        users[user_id]["referral_link"] = f"https://t.me/{bot.get_me().username}?start={users[user_id]['referral_code']}"

        registered_users[user_id] = True
        # generate_Language_inline_keyboard()
        bot.reply_to(
            message, registered_w[users[user_id]['Lang']].format(
                users[user_id]['referral_link']))

    else:
        bot.reply_to(message, already[users[user_id]['Lang']])

# Handler for the /menu command


@ bot.message_handler(commands=['menu'])
def show_menu(message):
    user_id = message.from_user.id

    # Check if the user is registered
    if user_id not in registered_users:
        bot.reply_to(
            message, first_register[users[user_id]['Lang']])
        return
    markup = telebot.types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('/Quiz')
    item2 = telebot.types.KeyboardButton('/Referral')
    item5 = telebot.types.KeyboardButton('/Balance')
    item4 = telebot.types.KeyboardButton('/Scoreboard', )
    item3 = telebot.types.KeyboardButton('/Change_Language')
    item6 = telebot.types.KeyboardButton('/Reward_list')
    markup.add(item1, item2, item4, item3, item5, item6)
    bot.send_message(
        user_id, Choose[users[user_id]['Lang']], reply_markup=markup)


def generate_inline_keyboard_quiz():
    markup = types.InlineKeyboardMarkup()
    for ans in ["Tech", "history"]:
        btn = types.InlineKeyboardButton(
            ans, callback_data=f"**{ans}")
        markup.add(btn)

    return markup


# create a dictionary of quiz questions and answers
quiz_questions = {
    "Tech":  {
        "In which decade was the American Institute of Electrical Engineers (AIEE) founded?": "1850s",
        "What is part of a database that holds only one type of information?": "Field",
        "'OS' computer abbreviation usually means ?": "Operating System",
        "In which decade with the first transatlantic radio broadcast occur?": "1900s",
        "'.MOV' extension refers usually to what kind of file?": "Image file",
        "In which decade was the SPICE simulator introduced?": "1950s",
        "Most modern TV's draw power even if turned off. The circuit the power is used in does what function?": "Sound",
        "Which is a type of Electrically-Erasable Programmable Read-Only Memory?": "Flash",
    },
    "history": {
        "In which Italian city can you find the Colosseum?": "Venice",
        "In the TV show New Girl, which actress plays Jessica Day?": "Alyson Hannigan",
        "What is the largest canyon in the world?": "Kings Canyon, Australia",
        "How long is the border between the United States and Canada?": "3,525 miles",
        "What is the largest active volcano in the world? ": "Mount Etna",
        "When did Lenin die?": "21 January 1944",
        "In which US state did the Scopes Monkey Trial happen?": "Maryland",
        "When was the book “To Kill a Mockingbird” by Harper Lee published?": "1980",
        "In which museum can you find Leonardo Da Vincis Mona Lisa?": "Le Louvre",
        "In which city can you find the Prado Museum?": "Buenos Aires",
        "When did Salt Lake City host the Winter Olympics?": "1998",
        "In the Big Bang Theory, what is the name of Sheldon and Leonards neighbour?": "Penny",
    }

}


# create a list of possible answers for each question
quiz_answers = {
    "Tech":
    [

        ['1850s', '1880s', '1930s', '1950s'],
        ['Report', 'Field', 'Record', 'File'],
        ['Order of Significance', 'Open Software',
         'Operating System', 'Optical Sensor'],
        ['1850s', '1860s', '1870s', '1900s'],
        ['Animation/movie file', 'Audio file', 'MS Office document'],
        ['1950s', '1960s', '1970s', '1980s'],
        ['Sound', 'Remote control', 'Color balance', 'High voltage'],
        ['Flash', 'Flange', 'Fury', 'FRAM']


    ],
    "history":
    [
        ['Venice', 'Rome', 'Naples', 'Milan'],
        ["Zooey Deschanel", "Kaley Cuoco", "Jennifer Aniston", "Alyson Hannigan"],
        ["Verdon Gorge, France", "Kings Canyon, Australia",
            "Grand Canyon, USA", "Fjaðrárgljúfur Canyon, Iceland"],
        ["3,525 miles", "4,525 miles", "5,525 miles", "6,525 miles"],
        ["Mount Etna", "Mount Vesuvius", "Mouna Loa", "Mount Batur"],
        ['21 January 1924', '21 January 1934',
            '21 January 1944', '21 January 1954'],
        ['Maryland', 'South Dakota', 'Indiana', 'Tennessee'],
        ['1950', '1960', '1970', '1980'],
        ['Le Louvre', 'Uffizi Museum', 'British Museum',
            'Metropolitan Museum of Art'],
        ['Buenos Aires', 'Barcelona', 'Santiago', 'Madrid'],
        ['1992', '1998', "2002", "2008"],
        ['Penny', 'Patty', 'Lily', 'Jessie']
    ]

}


# create a function to generate the inline keyboard with answer options


def generate_inline_keyboard(question_num, ty):
    markup = types.InlineKeyboardMarkup()
    for ans in quiz_answers[ty][question_num - 1]:
        btn = types.InlineKeyboardButton(
            ans, callback_data=f"{question_num}_{ans}")
        markup.add(btn)
    return markup


@ bot.message_handler(commands=['Change_Language'])
def generate_Language_inline_keyboard(message):
    user_id = message.from_user.id

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(
        "ENGLISH", callback_data=f"--ENGLISH")
    btn2 = types.InlineKeyboardButton(
        "AMHARIC", callback_data=f"--AMHARIC")
    btn3 = types.InlineKeyboardButton(
        "AFFAN_OROMO", callback_data=f"--AFFAN_OROMO")
    btn4 = types.InlineKeyboardButton(
        "ትግርኛ", callback_data=f"--ትግርኛ")
    markup.add(btn, btn2, btn4, btn3)
    bot.send_message(
        user_id, Choose["ENGLISH"], reply_markup=markup)


# create a function to send the quiz question


def send_question(chat_id, question_num, ty):
    question = list(quiz_questions[ty].keys())[question_num - 1]
    keyboard = generate_inline_keyboard(question_num, ty)
    bot.send_message(chat_id, question, reply_markup=keyboard)

# create a function to handle user input


@ bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user = call.from_user.id
    print(call.data)
    if "**" in call.data:
        # print(888888)
        global tyype
        tyype = call.data[2:]
        idd = users[user]["iid"]
        send_question(call.message.chat.id, idd, call.data[2:])
    elif "--" in call.data:
        users[user]['Lang'] = call.data[2:]
        bot.send_message(
            call.message.chat.id, done[users[user]["Lang"]].format(call.data[2:]))
    elif "++" in call.data:
        price, index = call.data[2:].split("_")
        if users[user]["coins"] < int(price):
            bot.send_message(
                call.message.chat.id, enough[users[user]["Lang"]])
        else:
            secret_key = ''.join(random.choices(
                'ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=12))
            users[user]["rewarded"].append(secret_key)
            users[user]["coins"] -= int(price)
            item = rewards_list[price][int(index)]
            bot.send_message(
                call.message.chat.id, secret[users[user]["Lang"]].format(item, secret_key))

    else:
        question_num, answer = call.data.split("_")
        users[user]["iid"] += 1
        print(question_num, 100000)

        if (int(question_num)+1) % 5 == 0:
            if answer == quiz_questions[tyype][list(quiz_questions[tyype].keys())[int(question_num) - 1]]:
                bot.quiz_scores[user] += 1
                users[user]["score"] += 1
            final_score = users[user]["score"]
            bot.send_message(
                call.message.chat.id, congra[users[user]['Lang']].format(final_score, len(quiz_questions[tyype])))
            if users[user]["iid"]-1 == len(quiz_questions[tyype]):
                print(778)
                bot.quiz_scores[user] = 0
                users[user]["score"] = 0
            return
        if not hasattr(bot, 'quiz_scores'):
            bot.quiz_scores = {}
        if user not in bot.quiz_scores:
            bot.quiz_scores[user] = 0
            users[user]["score"] = 0

        if answer == quiz_questions[tyype][list(quiz_questions[tyype].keys())[int(question_num) - 1]]:
            # bot.answer_callback_query(call.id, text="Correct!")
            bot.quiz_scores[user] += 1
            users[user]["score"] += 1
            if int(question_num) < len(quiz_questions[tyype]) and (int(question_num)+1) % 5 != 0:
                send_question(call.message.chat.id,
                              int(question_num) + 1, tyype)
            else:
                final_score = users[user]["score"]  # bot.quiz_scores[user]
                bot.send_message(
                    call.message.chat.id, congra[users[user]['Lang']].format(final_score, len(quiz_questions[tyype])))
                if users[user]["iid"]-1 == len(quiz_questions[tyype]):
                    # print(778)
                    bot.quiz_scores[user] = 0
                    users[user]["score"] = 0
                users[user]["iid"] = 1

        else:

            if int(question_num) < len(quiz_questions[tyype]) and (int(question_num)+1) % 5 != 0:
                send_question(call.message.chat.id,
                              int(question_num) + 1, tyype)
            else:
                final_score = bot.quiz_scores[user]
                bot.send_message(
                    call.message.chat.id, congra[users[user]['Lang']].format(final_score, len(quiz_questions[tyype])))
                # print()
                if users[user]["iid"]-1 == len(quiz_questions[tyype]):
                    # print(770)
                    bot.quiz_scores[user] = 0
                    users[user]["score"] = 0
                users[user]["iid"] = 1


@ bot.message_handler(commands=['Balance'])
def balance(message):
    user_id = message.from_user.id
    if user_id in users:
        bot.reply_to(message, coins_text[users[user_id]['Lang']].format(
            users[user_id]['coins']))
    else:
        bot.reply_to(message, start[users[user_id]['Lang']])


@ bot.message_handler(commands=['Scoreboard'])
def scoreboard(message):
    user_id = message.from_user.id
    if user_id in users:
        ree = sorted(users, key=lambda x: users[x]["score"])[::-1]
        print(ree)
        top_users = ""
        print(users)
        for i, u in enumerate(ree[:10]):
            name = f"#{i+1}." + users[u]["first_name"] + \
                " "+users[u]["last_name"]+"     " + \
                str(users[u]["score"])+" Points" + "\n"
            top_users += name
        bot.reply_to(
            message, top_users+"\n" + rank[users[user_id]['Lang']].format(ree.index(user_id)+1, len(users), users[user_id]['score']))
    else:
        bot.reply_to(message, start)


@ bot.message_handler(commands=['Referral'])
def ref(message):
    user_id = message.from_user.id
    if user_id in users:
        bot.reply_to(
            message, referral__[users[user_id]['Lang']].format(users[user_id]['referral_link']))
    else:
        bot.reply_to(message, start)


@bot.message_handler(commands=['Reward_list'])
def reward(message):
    user_id = message.from_user.id
    for k, y in rewards_list.items():
        markup = types.InlineKeyboardMarkup()
        for i, g in enumerate(y):
            btn = types.InlineKeyboardButton(
                g, callback_data=f"++{k}_{i}")
            markup.add(btn)

        bot.send_message(
            user_id, buy[users[user_id]['Lang']].format(k), reply_markup=markup)


# create a function to start the quiz
@ bot.message_handler(commands=['Quiz'])
def start_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, Choose[users[user_id]['Lang']],
                     reply_markup=generate_inline_keyboard_quiz())


bot.polling()
