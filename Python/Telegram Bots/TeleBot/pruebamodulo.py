# KEBERLEIN, Gian Franco - circa Sept. - Oct. 2020
# Ejemplo de uso del TeleBot

import modulotelegram as bot

token = "Your token here."

if __name__ == "__main__":
    myBot = bot.TeleBot(token)
    myBot.StartBot()
