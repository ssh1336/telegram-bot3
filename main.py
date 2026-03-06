# -*- coding: utf-8 -*-
import telebot
from telebot.types import ChatPermissions
import time

TOKEN = "PUT_YOUR_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN)

print("🔥 Global Bot V2 is running...")

warnings = {}

# -----------------------------
# التحقق من المشرف
# -----------------------------
def is_admin(chat_id, user_id):
    try:
        admins = bot.get_chat_administrators(chat_id)
        for admin in admins:
            if admin.user.id == user_id:
                return True
    except:
        return False
    return False

# -----------------------------
# أمر /start
# -----------------------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "أنا روبوت لإدارة مجموعتك 👑\nI am a bot for managing your group."
    )

# -----------------------------
# أوامر المشرفين بالعربي
# -----------------------------

# 🔴 حظر
@bot.message_handler(commands=['حظر'])
def ban_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "هذا الأمر للمشرفين فقط.")
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.ban_chat_member(message.chat.id, user_id)
        bot.send_message(message.chat.id, "تم حظر العضو بنجاح 🔴")
    else:
        bot.reply_to(message, "قم بالرد على رسالة العضو لحظره.")

# 🟢 فك الحظر
@bot.message_handler(commands=['الغاء_حظر'])
def unban_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        bot.unban_chat_member(message.chat.id, user_id)
        bot.send_message(message.chat.id, "تم إلغاء الحظر 🟢")

# 🟡 تحذير
@bot.message_handler(commands=['تحذير'])
def warn_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        bot.reply_to(message, "هذا الأمر للمشرفين فقط.")
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        warnings[user_id] = warnings.get(user_id, 0) + 1

        bot.send_message(message.chat.id,
            f"⚠️ تحذير {warnings[user_id]}/3")

        if warnings[user_id] >= 3:
            bot.ban_chat_member(message.chat.id, user_id)
            bot.send_message(message.chat.id,
                "🚫 تم حظر العضو بسبب 3 تحذيرات.")
    else:
        bot.reply_to(message, "قم بالرد على رسالة العضو لتحذيره.")

# 🧹 مسح التحذيرات
@bot.message_handler(commands=['مسح_التحذيرات'])
def clear_warns(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        warnings[user_id] = 0
        bot.send_message(message.chat.id, "تم تصفير التحذيرات ✅")

# 🔇 كتم لمدة دقيقة
@bot.message_handler(commands=['كتم'])
def mute_user(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        until = int(time.time()) + 60
        bot.restrict_chat_member(
            message.chat.id,
            user_id,
            ChatPermissions(can_send_messages=False),
            until_date=until
        )
        bot.send_message(message.chat.id, "تم كتم العضو لمدة دقيقة 🔇")

# -----------------------------
# الردود الذكية + الحماية
# -----------------------------
@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    text = message.text.lower()

    # ردودك الخاصة 👑
    if "من انت" in text or "who are you" in text:
        bot.reply_to(message,
            "𓆩˹𝚈𝙴𝙼 الـقـيـاده شــاهر 🇾🇪˼𓆪")

    elif "ما اسمك" in text or "what is your name" in text:
        bot.reply_to(message,
            "اسمي 𓆩˹𝚈𝙴𝙼 الـقـيـاده شــاهر 🇾🇪˼𓆪")

    elif "كيف حالك" in text or "how are you" in text:
        bot.reply_to(message,
            "الحمد لله بخير ❤️ / I am fine.")

    # 🚫 منع الروابط
    elif "http" in text or "www" in text:
        if not is_admin(message.chat.id, message.from_user.id):
            user_id = message.from_user.id
            bot.delete_message(message.chat.id, message.message_id)

            warnings[user_id] = warnings.get(user_id, 0) + 1

            bot.send_message(message.chat.id,
                f"🚫 ممنوع الروابط | تحذير {warnings[user_id]}/3")

            if warnings[user_id] >= 3:
                bot.ban_chat_member(message.chat.id, user_id)
                bot.send_message(message.chat.id,
                    "🚫 تم حظر العضو بسبب تكرار الروابط.")

# -------------------------
# Web Server للـ 24/7
# -------------------------
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

bot.infinity_polling()
