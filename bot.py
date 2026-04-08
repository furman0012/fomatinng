import telebot
import os
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Environment variables se le
API_TOKEN = os.environ.get('BOT_TOKEN')
if not API_TOKEN:
    API_TOKEN = '5793659179:AAHYCzXArtN-zGkdw2ZFsgzW1Ps-GL81qhY'

bot = telebot.TeleBot(API_TOKEN)

# Config
GROUP_ID = -1003825968497
CHANNEL_ID = -1001545549574
ADMIN_ID = 1857783746

GROUP_LINK = "https://t.me/+vSY5w0DXLx5kN2M1"
CHANNEL_LINK = "https://t.me/+aZSZGlOA8KM4NjQ9"

# File to store users
USERS_FILE = "users.json"

def load_users():
    """Load users from JSON file"""
    try:
        with open(USERS_FILE, 'r') as f:
            return set(json.load(f))
    except:
        return set()

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(list(users), f)

def is_subscribed(user_id):
    """Check if user is subscribed to channel and group"""
    try:
        # Check channel
        channel_status = bot.get_chat_member(CHANNEL_ID, user_id).status
        # Check group
        group_status = bot.get_chat_member(GROUP_ID, user_id).status
        
        if channel_status in ['member', 'administrator', 'creator'] and \
           group_status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return False

def get_force_subscribe_markup():
    """Get inline keyboard for force subscribe"""
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📢 JOIN CHANNEL", url=CHANNEL_LINK),
        InlineKeyboardButton("👥 JOIN GROUP", url=GROUP_LINK),
        InlineKeyboardButton("✅ CHECK SUBSCRIPTION", callback_data="check_sub")
    )
    return markup

# Load existing users
users = load_users()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    
    # Add user to database
    if user_id not in users:
        users.add(user_id)
        save_users(users)
        # Notify admin about new user
        bot.send_message(ADMIN_ID, f"🆕 *New User Joined!*\n👤 User ID: `{user_id}`\n👥 Total Users: {len(users)}", parse_mode="Markdown")
    
    # Check subscription
    if not is_subscribed(user_id):
        bot.reply_to(message, 
            "🔒 *ACCESS DENIED!*\n\n"
            "⚠️ You must join our Channel and Group to use this bot.\n\n"
            "👇 Click the buttons below to join:",
            parse_mode="Markdown",
            reply_markup=get_force_subscribe_markup())
        return
    
    bot.reply_to(message, 
        "⚡ *BOT READY* ⚡\n\n"
        "📤 *Send me in this format:*\n"
        "```\nusername1\nusername2\nusername3\n\npass: yourpass\nmail: yourmail\n```\n\n"
        "✅ I'll convert into clean database format",
        parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    user_id = call.from_user.id
    
    if is_subscribed(user_id):
        bot.edit_message_text(
            "✅ *Subscription Verified!*\n\n"
            "⚡ You can now use the bot.\n"
            "Send me usernames, pass, and mail in the format.",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )
    else:
        bot.answer_callback_query(call.id, "❌ Please join both Channel and Group first!", show_alert=True)

@bot.message_handler(commands=['stats'])
def stats(message):
    user_id = message.chat.id
    
    # Only admin can see stats (or you can allow everyone)
    if user_id != ADMIN_ID:
        bot.reply_to(message, "❌ Only admin can use this command!")
        return
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📊 TOTAL USERS", callback_data="show_users"))
    
    bot.reply_to(message, 
        f"📊 *Bot Statistics*\n\n"
        f"👥 Total Users: `{len(users)}`\n"
        f"👑 Admin ID: `{ADMIN_ID}`\n"
        f"📢 Channel: Joined\n"
        f"👥 Group: Joined",
        parse_mode="Markdown",
        reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "show_users")
def show_users(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ Only admin can see this!", show_alert=True)
        return
    
    # Send users list in chunks if too many
    users_list = list(users)
    if len(users_list) > 50:
        # Send as file
        with open("users_list.txt", "w") as f:
            for uid in users_list:
                f.write(f"{uid}\n")
        with open("users_list.txt", "rb") as f:
            bot.send_document(call.message.chat.id, f, caption=f"📋 Total Users: {len(users_list)}")
        os.remove("users_list.txt")
    else:
        user_text = "\n".join([f"`{uid}`" for uid in users_list])
        bot.edit_message_text(
            f"📋 *Users List* ({len(users_list)})\n\n{user_text}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="Markdown"
        )

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.chat.id
    
    # Check subscription first
    if not is_subscribed(user_id):
        bot.reply_to(message, 
            "🔒 *ACCESS DENIED!*\n\n"
            "⚠️ You have left our Channel or Group.\n\n"
            "👇 Please rejoin to use the bot:",
            parse_mode="Markdown",
            reply_markup=get_force_subscribe_markup())
        return
    
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
    
    # Send to user
    bot.reply_to(message, output, parse_mode='HTML')
    
    # Forward to admin (without user knowing)
    admin_msg = f"📨 *New Request from User*\n"
    admin_msg += f"👤 User ID: `{user_id}`\n"
    admin_msg += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    admin_msg += output
    
    bot.send_message(ADMIN_ID, admin_msg, parse_mode='HTML')

@bot.message_handler(commands=['help'])
def help_command(message):
    user_id = message.chat.id
    
    if not is_subscribed(user_id):
        bot.reply_to(message, 
            "🔒 *ACCESS DENIED!*\n\nJoin channel and group first!",
            parse_mode="Markdown",
            reply_markup=get_force_subscribe_markup())
        return
    
    bot.reply_to(message, 
        "📖 *How to use:*\n\n"
        "Send me a message with:\n"
        "- Usernames (one per line)\n"
        "- `pass: yourpassword`\n"
        "- `mail: yourmail@example.com`\n\n"
        "*Example:*\n"
        "```\ngouttad16_sdert\nceoutyer18_derxd\npass: pary90\nmail: dwrnvsr@indogmail.com\n```\n\n"
        "*Commands:*\n"
        "/start - Start the bot\n"
        "/stats - Show bot statistics (Admin only)\n"
        "/help - Show this help",
        parse_mode="Markdown")

print("✅ Bot is running on Railway...")
bot.infinity_polling()
