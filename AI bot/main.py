import telebot, requests, os
from telebot import TeleBot
from config import TOKEN
from classification import detect

bot = telebot.TeleBot(TOKEN)
model_path = 'models/model1/model_1.h5'
label_path = 'models/model1/labels_1.txt'
meal = {
    "голубь": ["перловка, пшеница, ячмень, семечки, гречка, просо, горох, чечевица и другие крупы в сухом виде."],
    "синица": ["семена подсолнечника, орешки: грецкие, фундук, кедровые, кусочки сала (обязательно несоленого!)"],
    "ворона": ["нежирное мясо (курица, индейка, говядина), субпродукты (сердце, печень), вареное яйцо (куриное или перепелиное), обезжиренный творог, морская рыба, свежие овощи и фрукты (яблоки, морковь, тыква), ягоды, зелень"],
    "пеликан": ["свежая живая рыба (карп, сазан, лещ, окунь, плотва, сельдь)"]
}

@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.reply_to(message, 'Привет, я бот! Умею распозновать картинки! Посмотреть команды можно написав /help')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    result = detect(file_name, model_path, label_path)
    result2 = result[0].replace("\n", "")
    class_name = result[0].replace('\n', '').lower
    percent = int(result[1]*100)
    bot.reply_to(message, f"На изображении {class_name}, с вероятностью {percent}%")
    match result2:
        case "Голуби":
            print("Кормить:", *meal["голубь"])
        case "Синички":
            print("Кормить:", *meal["синица"])
        case "Вороны":
            print("Кормить:", *meal["ворона"])
        case "Пеликаны":
            print("Кормить:", *meal["пеликан"])
    os.remove(f"./{file_name}")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.reply_to(message.chat.id, 'Фото не обнаружено')

print('Бот запущен')
bot.polling()