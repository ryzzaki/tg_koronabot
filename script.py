# -*- coding: utf-8 -*-
import requests as req
import telebot
import config
from datetime import datetime

bot = telebot.TeleBot(config.api_key)
print("[" + str(datetime.now()) + "] Running...")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print("[" + str(datetime.now()) + "] /start by " +
          message.from_user.username)
    bot.reply_to(message, 'Hello, *' +
                 str(message.from_user.first_name) + "*!", parse_mode='Markdown')


@bot.message_handler(commands=['countries'])
def list_countries(message):
    print("[" + str(datetime.now()) + "] /countries by " +
          message.from_user.username)
    r_countries = req.get('https://corona.lmao.ninja/countries').json()
    res_msg = "*Supported Countries*" + ("\n"*2)
    for country_obj in r_countries:
        res_msg = "\n" + res_msg + country_obj['country'] + "\n"
    bot.send_message(message.chat.id, res_msg,
                     parse_mode='Markdown')


@bot.message_handler(commands=['corona'])
def corona_stat(message):
    print("[" + str(datetime.now()) + "] /corona by " +
          message.from_user.username)
    command = str(message.text).split()
    if len(command) < 2:
        bot.reply_to(message, "Missing argument.", parse_mode='Markdown')
    else:
        msg = str(message.text).split()
        msg.remove("/corona")
        input_country = " ".join(msg).strip()
        if input_country == "all":
            r_all = req.get('https://corona.lmao.ninja/all').json()
            res_msg = f"*Global Statistics*" + \
                ("\n"*2) + f"*Total number of Cases:* {r_all['cases']}" + \
                "\n" + f"*Total number of Deaths:* {r_all['deaths']}" + \
                "\n" + f"*Total number of Recovers:* {r_all['recovered']}"
            bot.send_message(message.chat.id, res_msg, parse_mode='Markdown')
        else:
            r_countries = req.get('https://corona.lmao.ninja/countries').json()
            flag = False
            for country_obj in r_countries:
                if country_obj["country"].lower() == input_country.lower():
                    res_msg = f"*Statistics for* {country_obj['country'].upper()}" + \
                        ("\n"*2) + f"*Total number of Cases:* {country_obj['cases']}" + \
                        "\n" + f"*Number of New Cases:* {country_obj['todayCases']}" + \
                        ("\n"*2) + f"*Total number of Deaths:* {country_obj['deaths']}" + \
                        "\n" + f"*Number of New Deaths:* {country_obj['todayDeaths']}" + \
                        ("\n"*2) +\
                        f"*Total number of Recovers:* {country_obj['recovered']}" + \
                        "\n" + \
                        f"*Total number of Critical Conditions:* {country_obj['critical']}"
                    bot.send_message(message.chat.id, res_msg,
                                     parse_mode='Markdown')
                    flag = True
                    break
            if not flag:
                bot.reply_to(
                    message, f"Not found... *{input_country}* is probably not a country. Try again.", parse_mode='Markdown')


bot.polling(none_stop=True)
