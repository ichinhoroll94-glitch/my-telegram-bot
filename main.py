import telebot
from telebot import types

# ТАНЫ БОТНЫ НУУЦ ТҮЛХҮҮР (Би саяны ирсэн кодыг чинь шууд холбочихлоо)
TOKEN = "8779069842:AAEm2u9onh-6cFEd8e519q2h6aZw0_utISE"
bot = telebot.TeleBot(TOKEN)

# 🛍️ ДЭЛГҮҮРИЙН БҮТЭЭГДЭХҮҮНҮҮД БА ҮНЭ (Үүнийг дараа нь өөрчилж болно)
BARAANUUD = {
    "🎁 Бэлгийн багц": 35000,
    "👕 Загварлаг цамц": 45000,
    "👟 Спорт пүүз": 85000,
    "🎒 Аялалын үүргэвч": 60000
}

# Үйлчлүүлэгч /start гэж дарах үед угтах хэсэг
@bot.message_handler(commands=['start'])
def welcome(message):
    # Дардаг гоё товчлуур үүсгэх (Reply Keyboard)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Бүтээгдэхүүн бүрт зориулж товчлуур нэмэх
    for baraa in BARAANUUD.keys():
        markup.add(types.KeyboardButton(baraa))
    
    markup.add(types.KeyboardButton("🛒 Сагс хоослох"), types.KeyboardButton("📞 Холбоо барих"))

    bot.send_message(
        message.chat.id, 
        f"👋 Сайн уу, {message.from_user.first_name}!\n"
        "**Манай ухаалаг дэлгүүрийн бот хуудсанд тавтай морил.**\n"
        "Та доорх товчлууруудаас сонгон бүтээгдэхүүний үнэ харах болон захиалга өгөх боломжтой:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# Хэрэглэгчийн дарсан товчлуурыг уншиж хариулах хэсэг
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text

    # 1. Хэрэв бараа сонговол үнийг нь харуулж, захиалах уу гэж асууна
    if text in BARAANUUD:
        une = BARAANUUD[text]
        
        # Мессеж дотор байрлах тусдаа гоё товчлуур (Inline Keyboard)
        inline_markup = types.InlineKeyboardMarkup()
        захиалах_товч = types.InlineKeyboardButton(text="📥 Яг одоо захиалах", callback_data=f"order_{text}")
        inline_markup.add(захиалах_товч)
        
        bot.send_message(
            message.chat.id,
            f"🔎 **{text}**\n\n"
            f"💰 Үнэ: {une:,} ₮\n"
            f"📦 Төлөв: Бэлэн байгаа\n\n"
            f"Та энэ барааг захиалахыг хүсвэл доорх товчийг дарна уу:",
            reply_markup=inline_markup,
            parse_mode="Markdown"
        )
        
    # 2. Холбоо барих хэсэг
    elif text == "📞 Холбоо барих":
        bot.send_message(
            message.chat.id,
            "📞 **Холбоо барих мэдээлэл:**\n\n"
            "📍 Хаяг: Улаанбаатар хот\n"
            "📞 Утас: 85607378\n"
            "🌐 Вэб сайт: ://onrender.com",
            parse_mode="Markdown"
        )
    
    # 3. Сагс хоослох
    elif text == "🛒 Сагс хоослох":
        bot.send_message(message.chat.id, "🛒 Таньд одоогоор сонгосон бараа байхгүй байна.")
    
    else:
        bot.send_message(message.chat.id, "💡 Доорх бэлэн товчлууруудыг ашиглан чатлана уу.")

# "Яг одоо захиалах" товчлуур дарах үед ажиллах хэсэг
@bot.callback_query_handler(func=lambda call: call.data.startswith('order_'))
def callback_inline(call):
    baraa_ner = call.data.replace('order_', '')
    une = BARAANUUD.get(baraa_ner, 0)
    
    # Захиалга амжилттай болсон тухай хариу
    bot.answer_callback_query(call.id, text="Захиалга бүртгэгдлээ!")
    bot.send_message(
        call.message.chat.id,
        f"🎉 **Баяр хүргэе!**\n\n"
        f"Таны **{baraa_ner}** ({une:,} ₮)-ийн захиалга амжилттай бүртгэгдлээ.\n"
        f"Манай менежер таны утас руу залгаж хүргэлтийн хаягийг тань баталгаажуулах болно. Баярлалаа! 🙏",
        parse_mode="Markdown"
    )

# Ботыг тасралтгүй ажиллуулах нээлттэй үлдээх хэсэг
print("Бот амжилттай аслаа... Telegram руугаа орж шалгана уу!")
bot.infinity_polling()
