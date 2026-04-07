import telebot
import os
import re

# Environment variables se le
API_TOKEN = os.environ.get('BOT_TOKEN')
if not API_TOKEN:
    API_TOKEN = '5793659179:AAHYCzXArtN-zGkdw2ZFsgzW1Ps-GL81qhY'  # Backup

bot = telebot.TeleBot(API_TOKEN)

# Store user data temporarily (simple dict)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.reply_to(message, 
        "⚡ *BOT READY* ⚡\n\n"
        "📤 *Send me in this format:*\n"
        "```\nusername1\nusername2\nusername3\n\npass: yourpass\nmail: yourmail\n```\n\n"
        "✅ I'll convert into clean database format",
        parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()
    lines = text.split('\n')
    
    usernames = []
    password = None
    mail = None
    
    for line in lines:
        if line.lower().startswith('pass:'):
            password = line.split(':', 1)[1].strip()
        elif line.lower().startswith('mail:'):
            mail_input = line.split(':', 1)[1].strip()
            mail = f"/accept {mail_input}"
        else:
            if line.strip():
                usernames.append(line.strip())
    
    # Validate
    if not password or not mail:
        bot.reply_to(message, 
            "❌ *Invalid Format!*\n\n"
            "Send like this:\n"
            "```\nusername1\nusername2\npass: yourpass\nmail: yourmail\n```",
            parse_mode="Markdown")
        return
    
    if not usernames:
        bot.reply_to(message, "❌ No usernames found!")
        return
    
    # Format output with HTML
    output = "📂 <b>𝙳𝙰𝚃𝙰𝙱𝙰𝚂𝙴 𝙸𝙽𝙵𝙾</b>\n"
    output += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    output += f"👥 <b>𝚄𝚂𝙴𝚁𝚂</b> ({len(usernames)})\n"
    
    for i, user in enumerate(usernames, 1):
        if i < 10:
            output += f" {i}  - <code>{user}</code>\n"
        else:
            output += f" {i} - <code>{user}</code>\n"
    
    output += f"\n🔑 <b>𝙿𝙰𝚂𝚂</b> : <code>{password}</code>\n"
    output += f"📧 <b>𝙼𝙰𝙸𝙻</b> : <code>{mail}</code>\n"
    output += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    output += "✅ <b>𝙰𝚕𝚕 𝙰𝚌𝚝𝚒𝚟𝚎</b> | 𝙵𝙱 𝙵𝚒𝚡𝚎𝚍\n"
    output += "⚡ <i>𝙰𝚞𝚝𝚘 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚎𝚍</i>\n\n"
    output += "📜 <b>𝙿𝚘𝚕𝚒𝚌𝚢</b> : <a href='https://t.me/c/1545549574/5927'>Read before use</a>"
    
    bot.reply_to(message, output, parse_mode='HTML')

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, 
        "📖 *How to use:*\n\n"
        "Send me a message with:\n"
        "- Usernames (one per line)\n"
        "- `pass: yourpassword`\n"
        "- `mail: yourmail@example.com`\n\n"
        "*Example:*\n"
        "```\ngouttad16_sdert\nceoutyer18_derxd\npass: pary90\nmail: dwrnvsr@indogmail.com\n```",
        parse_mode="Markdown")

print("✅ Bot is running on Railway...")
bot.infinity_polling()
