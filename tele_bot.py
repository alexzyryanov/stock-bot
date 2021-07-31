from opening_excel import *
import telebot


bot = telebot.TeleBot("TOKEN")


@bot.message_handler(content_types=["document"])
def document(message):
    print(message.from_user.id)
    user_id = message.from_user.id
    file = bot.get_file(message.document.file_id)
    r = bot.download_file(file.file_path)
    with open(f'{user_id}.xlsx', 'wb') as f:
        f.write(r)
    try:
        clean(user_id)
    except:
        pass
    create(user_id)
    bot.send_message(message.chat.id, f"{check(user_id)}")
