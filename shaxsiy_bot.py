import telebot
import os
from flask import Flask
from threading import Thread
from telebot import types
import openai

# ========== MUHIT O‘ZGARUVCHILARI ==========
TOKEN = os.environ.get('BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# OpenAI ni sozlash
openai.api_key = OPENAI_API_KEY

bot = telebot.TeleBot(TOKEN)

# ========== AI yordamchisi ==========
def ask_ai(prompt):
    """OpenAI API orqali so‘rov yuboradi va javobni qaytaradi"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # yoki "gpt-4" agar mavjud bo‘lsa
            messages=[
                {"role": "system", "content": "Siz ilmiy yordamchi bot. Foydalanuvchiga ilmiy maqola, taqdimot, referat va boshqa akademik ishlarda yordam berasiz."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

# ========== /start menyusi ==========
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("📄 Ilmiy maqola", callback_data="article")
    btn2 = types.InlineKeyboardButton("📊 Taqdimot", callback_data="presentation")
    btn3 = types.InlineKeyboardButton("📝 Referat", callback_data="essay")
    btn4 = types.InlineKeyboardButton("✍️ Mustaqil ish", callback_data="independent")
    btn5 = types.InlineKeyboardButton("🎓 Kurs ishi", callback_data="coursework")
    btn6 = types.InlineKeyboardButton("🏆 Diplom ishi", callback_data="thesis")
    btn7 = types.InlineKeyboardButton("✒️ Qo‘lyozma", callback_data="manuscript")
    btn8 = types.InlineKeyboardButton("📄 PDF → Word", callback_data="pdf2word")
    btn9 = types.InlineKeyboardButton("📝 Word → PDF", callback_data="word2pdf")
    btn10 = types.InlineKeyboardButton("🧠 Psixologik ko‘mak", callback_data="psychology")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10)
    bot.send_message(message.chat.id, "🔽 Xizmatlar menyusi: 🔽", reply_markup=markup)

# ========== Tugmalarni boshqarish ==========
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "article":
        # Foydalanuvchidan mavzu so‘rash
        msg = bot.send_message(call.message.chat.id, "📄 Ilmiy maqola mavzusini yozing:")
        bot.register_next_step_handler(msg, process_article)
    else:
        # Boshqa tugmalar hozircha statik xabar
        bot.send_message(call.message.chat.id, "Bu xizmat hozircha tayyorlanmoqda.")
    
    bot.answer_callback_query(call.id)

# ========== Ilmiy maqola uchun AI so‘rovi ==========
def process_article(message):
    topic = message.text
    # Foydalanuvchiga kutish xabari
    bot.send_message(message.chat.id, "⏳ AI maqola tayyorlamoqda, iltimos kuting...")
    # AI dan javob olish
    prompt = f"Ilmiy maqola mavzusi: {topic}. Iltimos, maqola sarlavhasi, kirish, asosiy qism (2-3 band), xulosa va foydalanilgan adabiyotlar bilan to‘liq maqola matnini yozing. Maqola ilmiy uslubda bo‘lsin."
    answer = ask_ai(prompt)
    # Javobni yuborish (agar uzun bo‘lsa, qismlarga bo‘lish mumkin)
    bot.send_message(message.chat.id, answer)

# ========== Boshqa matnli xabarlar ==========
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, "Menyuni ko‘rish uchun /start ni bosing.")

# ========== Flask server (Render uchun) ==========
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
bot.polling()
