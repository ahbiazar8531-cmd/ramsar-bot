import telebot
import pandas as pd
import os

# توکن شما
TOKEN = '7976332425:AAGJw9WaGwEBClEEywNLBf0Ya0TeG4G3mo4'
bot = telebot.TeleBot(TOKEN)

# تابع تبدیل زمان (دقیقاً مشابه کد استریم‌لیت شما)
def format_excel_time(t):
    if pd.isna(t): return "-"
    try:
        if isinstance(t, (float, int)):
            seconds = int(round(t * 24 * 3600))
            h = seconds // 3600
            m = (seconds % 3600) // 60
            return f"{h:02d}:{m:02d}"
        return str(t)
    except:
        return str(t)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "👋 سلام! به ربات دانشگاه آزاد رامسر خوش آمدید.\n🔍 نام درس یا نام استاد را بفرستید تا برنامه را برایتان پیدا کنم.")

@bot.message_handler(func=lambda message: True)
def search(message):
    query = message.text.strip()
    
    if not os.path.exists("schedule.xlsx"):
        bot.reply_to(message, "❌ خطا: فایل schedule.xlsx در سرور یافت نشد.")
        return

    try:
        df = pd.read_excel("schedule.xlsx")
        # جستجو در نام درس و نام استاد
        filtered = df[(df['نام درس'].astype(str).str.contains(query, na=False)) | 
                      (df['نام استاد'].astype(str).str.contains(query, na=False))]

        if filtered.empty:
            bot.reply_to(message, "😔 موردی یافت نشد. لطفاً نام را کامل‌تر یا دقیق‌تر بنویسید.")
        else:
            response = f"✅ نتایج یافت شده برای «{query}»:\n\n"
            for _, row in filtered.head(10).iterrows(): # نمایش حداکثر ۱۰ مورد
                time_val = format_excel_time(row.get('زمان شروع', row.get('زمان', '-')))
                response += (f"📘 درس: {row['نام درس']}\n"
                            f"👤 استاد: {row['نام استاد']}\n"
                            f"📅 روز: {row['روز']}\n"
                            f"⏰ زمان: {time_val}\n"
                            f"🏛 کلاس: {row['شماره کلاس']}\n"
                            f"------------------------\n")
            
            bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.reply_to(message, "🛠 خطایی در پردازش اطلاعات رخ داد.")
        print(f"Error: {e}")

bot.polling()