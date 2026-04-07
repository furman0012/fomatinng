import telebot

# --- CONFIGURATION ---
API_TOKEN = '8281592181:AAGoaEPUXCby4uUN7_z8jiixKFE50RfFYGc'
CHAT_ID = '1857783746'
bot = telebot.TeleBot(API_TOKEN)

def get_multiline_input(prompt):
    print(f"\n[?] {prompt}")
    print("(Ek baar me saare usernames paste karein, phir 'DONE' likh kar Enter maarein)")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'DONE':
            break
        if line.strip():
            lines.append(line.strip())
    return lines

def format_usernames_with_numbers(usernames):
    """Format usernames with numbers - each in monospace using <code> tag"""
    result = []
    for i, user in enumerate(usernames, 1):
        # Proper alignment with spaces
        if i < 10:
            result.append(f" {i}  - <code>{user}</code>")
        else:
            result.append(f" {i} - <code>{user}</code>")
    return "\n".join(result)

def start_script():
    print("🚀 --- Account Data Formatter & Sender --- 🚀")
    
    # 1. Collect Usernames
    usernames = get_multiline_input("PASTE ALL USERNAMES:")
    
    if not usernames:
        print("❌ No usernames entered. Script stopping.")
        return

    # 2. Collect Password
    print("\n[?] ENTER PASSWORD:")
    password = input(">> ").strip()

    # 3. Collect Mail
    print("\n[?] ENTER MAIL:")
    mail_input = input(">> ").strip()
    # Fix mail format: /accept + user_mail
    mail = f"/accept {mail_input}"

    print("\n⏳ Sending to Telegram...")

    # --- FORMAT USERNAMES WITH MONOSPACE (HTML) ---
    username_list = format_usernames_with_numbers(usernames)
    
    # --- MESSAGE WITH EXACT FORMAT (no extra gaps) ---
    professional_msg = (
        "📂 <b>𝙳𝙰𝚃𝙰𝙱𝙰𝚂𝙴 𝙸𝙽𝙵𝙾</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 <b>𝚄𝚂𝙴𝚁𝚂</b> ({len(usernames)})\n"
        f"{username_list}\n\n"
        f"🔑 <b>𝙿𝙰𝚂𝚂</b> : <code>{password}</code>\n"
        f"📧 <b>𝙼𝙰𝙸𝙻</b> : <code>{mail}</code>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ <b>𝙰𝚕𝚕 𝙰𝚌𝚝𝚒𝚟𝚎</b> | 𝙵𝙱 𝙵𝚒𝚡𝚎𝚍\n"
        "⚡ <i>𝙰𝚞𝚝𝚘 𝙶𝚎𝚗𝚎𝚛𝚊𝚝𝚎𝚍</i>\n\n"
        "📜 <b>𝙿𝚘𝚕𝚒𝚌𝚢</b> : <a href='https://t.me/c/1545549574/5927'>Read before use</a>"
    )

    try:
        bot.send_message(CHAT_ID, professional_msg, parse_mode='HTML')
        print("\n✅ Data sent to Telegram!")
        print(f"📤 Message sent to CHAT_ID: {CHAT_ID}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    start_script()
