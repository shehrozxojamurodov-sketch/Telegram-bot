import telebot
import os
from flask import Flask
from threading import Thread
from telebot import types

# Tokenni muhit oʻzgaruvchisidan olish
TOKEN = "8730458805:AAGufW-Oxhrs_gFoyFDsMyJ5varyv-mIX9k"   
bot = telebot.TeleBot(TOKEN)

# /start buyrug‘i – menyuni ko‘rsatish
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)  # 2 tugma bir qatorda
    btn1 = types.InlineKeyboardButton("📄 Ilmiy maqola", callback_data="article")
    btn2 = types.InlineKeyboardButton("📊 Taqdimot", callback_data="presentation")
    btn3 = types.InlineKeyboardButton("📝 Referat", callback_data="essay")
    btn4 = types.InlineKeyboardButton("✍ Mustaqil ish", callback_data="independent")
    btn5 = types.InlineKeyboardButton("🎓 Kurs ishi", callback_data="coursework")
    btn6 = types.InlineKeyboardButton("🏆 Diplom ishi", callback_data="thesis")
    btn7 = types.InlineKeyboardButton("✒ Qo‘lyozma", callback_data="manuscript")
    btn8 = types.InlineKeyboardButton("📄 PDF → Word", callback_data="pdf2word")
    btn9 = types.InlineKeyboardButton("📝 Word → PDF", callback_data="word2pdf")
    btn10 = types.InlineKeyboardButton("🧠 Psixologik ko‘mak", callback_data="psychology")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10)

    bot.send_message(message.chat.id, "🔽 Xizmatlar menyusi: 🔽", reply_markup=markup)

# Tugmalarni boshqarish
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "article":
        text = "📄 *Ilmiy maqola* xizmati.\n\nMaqolangizni yuboring, biz uni formatlab beramiz (tez orada qo‘shiladi)."
    elif call.data == "presentation":
        text = "📊 *Taqdimot* yaratish.\n\nMavzuni yozing, biz sizga slaydlar tayyorlab beramiz."
    elif call.data == "essay":
        text = "📝 *Referat* yozish.\n\nReferat mavzusini va talablarini yuboring."
    elif call.data == "independent":
        text = "✍ *Mustaqil ish*.\n\nMustaqil ish mavzusini va hajmini yozing."
    elif call.data == "coursework":
        text = "🎓 *Kurs ishi*.\n\nKurs ishi uchun mavzu va yo‘riqnomani yuboring."
    elif call.data == "thesis":
        text = "🏆 *Diplom ishi*.\n\nDiplom ishi mavzusi va talablarni yuboring."
    elif call.data == "manuscript":
        text = "✒ *Qo‘lyozma*.\n\nQo‘lyozmangizni yuboring, uni matnga aylantiramiz."
    elif call.data == "pdf2word":
        text = "📄 *PDF → Word*.\n\nPDF faylni yuboring, Word formatiga o‘giramiz."
    elif call.data == "word2pdf":
        text = "📝 *Word → PDF*.\n\nWord faylni yuboring, PDF ga o‘giramiz."
    elif call.data == "psychology":
        text = "🧠 *Psixologik ko‘mak*.\n\nMaslahat uchun @psixolog_user ga murojaat qiling (vaqtincha)."
    else:
        text = "Nomaʼlum buyruq."

    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    bot.answer_callback_query(call.id)  # tugma bosilganda "yuklanmoqda" animatsiyasini yopish

# Boshqa matnli xabarlar uchun
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, "Menyuni ko‘rish uchun /start ni bosing.")

# Render uchun web server (botni jonli saqlash)
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
print("Bot is running!")
bot.polling()

