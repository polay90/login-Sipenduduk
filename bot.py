#!/usr/bin/env python3
"""
Telegram Bot for Sipenduduk Pekanbaru Registration and Login
Supports login and registration with data persistence
"""

import logging
import os
import json
import re
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(LOGIN, 
 REGISTER_NAME, 
 REGISTER_PHONE, 
 REGISTER_EMAIL, 
 REGISTER_WHATSAPP,
 REGISTER_PASSWORD,
 REGISTER_PASSWORD_CONFIRM,
 REGISTER_CONFIRM) = range(8)

# User data storage
USERS_DB = {}

def load_users():
    """Load users from JSON file"""
    global USERS_DB
    if os.path.exists('users.json'):
        try:
            with open('users.json', 'r') as f:
                USERS_DB = json.load(f)
        except:
            USERS_DB = {}

def save_users():
    """Save users to JSON file"""
    with open('users.json', 'w') as f:
        json.dump(USERS_DB, f, indent=2)

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    """Validate phone number"""
    return phone.startswith('08') and len(phone) >= 10 and phone.isdigit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the bot and show main menu"""
    keyboard = [
        [InlineKeyboardButton("🔐 Login", callback_data='login')],
        [InlineKeyboardButton("📝 Daftar Akun Baru", callback_data='register')],
        [InlineKeyboardButton("ℹ️ Info", callback_data='info')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 *Selamat Datang di Bot Sipenduduk Pekanbaru*\n\n"
        "Sistem Informasi Penduduk Kota Pekanbaru\n\n"
        "Silakan pilih menu di bawah:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle button presses"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'login':
        await query.edit_message_text(
            "🔐 *LOGIN AKUN SIPENDUDUK*\n\n"
            "Masukkan email atau nomor handphone Anda:",
            parse_mode='Markdown'
        )
        return LOGIN
    
    elif query.data == 'register':
        await query.edit_message_text(
            "📝 *DAFTAR AKUN BARU*\n\n"
            "Mari kita isi formulir registrasi.\n"
            "Ketikkan nama lengkap Anda (minimal 3 karakter):",
            parse_mode='Markdown'
        )
        return REGISTER_NAME
    
    elif query.data == 'info':
        await query.edit_message_text(
            "ℹ️ *INFORMASI BOT SIPENDUDUK*\n\n"
            "Bot ini membantu Anda untuk:\n"
            "✅ Login ke akun Sipenduduk\n"
            "✅ Mendaftar akun baru\n"
            "✅ Verifikasi data penduduk\n\n"
            "📧 Email: admin@sipenduduk.pekanbaru.go.id\n"
            "🌐 Website: https://sipenduduk.pekanbaru.go.id\n\n"
            "Untuk mulai, gunakan /start"
        )

async def handle_login_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle login email/phone input"""
    email_or_phone = update.message.text.strip()
    context.user_data['login_identifier'] = email_or_phone
    
    await update.message.reply_text(
        "🔐 Masukkan kata sandi Anda:",
        reply_markup=ReplyKeyboardRemove()
    )
    return LOGIN

async def handle_login_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle login password verification"""
    password = update.message.text.strip()
    identifier = context.user_data.get('login_identifier')
    
    # Find user by email or phone
    user_found = False
    logged_in_email = None
    
    for email, user_data in USERS_DB.items():
        if (user_data.get('email') == identifier or 
            user_data.get('phone') == identifier):
            if user_data.get('password') == password:
                user_found = True
                logged_in_email = email
                break
    
    if user_found:
        user_data = USERS_DB[logged_in_email]
        context.user_data['logged_in_email'] = logged_in_email
        
        await update.message.reply_text(
            f"✅ *LOGIN BERHASIL*\n\n"
            f"Selamat datang, {user_data.get('name')}! 👋\n\n"
            f"📧 Email: {user_data.get('email')}\n"
            f"📱 No. HP: {user_data.get('phone')}\n"
            f"💬 WhatsApp: {user_data.get('whatsapp')}\n"
            f"📅 Terdaftar: {user_data.get('registered_at')}\n\n"
            f"Anda sekarang dapat mengakses layanan Sipenduduk.\n"
            f"Gunakan /start untuk menu utama.",
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            "❌ *LOGIN GAGAL*\n\n"
            "Email/No. HP atau kata sandi tidak ditemukan.\n\n"
            "Opsi:\n"
            "1️⃣ Coba login lagi: /start\n"
            "2️⃣ Daftar akun baru: /start",
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove()
        )
    
    return ConversationHandler.END

async def handle_register_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle registration name input"""
    name = update.message.text.strip()
    
    if len(name) < 3:
        await update.message.reply_text(
            "❌ Nama harus minimal 3 karakter.\nCoba lagi:"
        )
        return REGISTER_NAME
    
    context.user_data['reg_name'] = name
    await update.message.reply_text(
        f"✅ Nama: {name}\n\n"
        "Masukkan nomor handphone (contoh: 08123456789):"
    )
    return REGISTER_PHONE

async def handle_register_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle registration phone input"""
    phone = update.message.text.strip()
    
    if not is_valid_phone(phone):
        await update.message.reply_text(
            "❌ Nomor handphone tidak valid.\n"
            "Harus dimulai dari 08 dan minimal 10 digit.\n"
            "Coba lagi (contoh: 08123456789):"
        )
        return REGISTER_PHONE
    
    # Check if phone already registered
    for user in USERS_DB.values():
        if user.get('phone') == phone:
            await update.message.reply_text(
                "❌ Nomor handphone ini sudah terdaftar.\n"
                "Gunakan nomor lain:"
            )
            return REGISTER_PHONE
    
    context.user_data['reg_phone'] = phone
    await update.message.reply_text(
        f"✅ No. HP: {phone}\n\n"
        "Masukkan email Anda (contoh: nama@email.com):"
    )
    return REGISTER_EMAIL

async def handle_register_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle registration email input"""
    email = update.message.text.strip().lower()
    
    if not is_valid_email(email):
        await update.message.reply_text(
            "❌ Email tidak valid.\n"
            "Coba lagi (contoh: nama@email.com):"
        )
        return REGISTER_EMAIL
    
    # Check if email already exists
    if email in USERS_DB:
        await update.message.reply_text(
            "❌ Email ini sudah terdaftar.\n"
            "Gunakan email lain:"
        )
        return REGISTER_EMAIL
    
    context.user_data['reg_email'] = email
    await update.message.reply_text(
        f"✅ Email: {email}\n\n"
        "Masukkan nomor WhatsApp aktif (contoh: 08123456789):"
    )
    return REGISTER_WHATSAPP

async def handle_register_whatsapp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle registration WhatsApp input"""
    whatsapp = update.message.text.strip()
    
    if not is_valid_phone(whatsapp):
        await update.message.reply_text(
            "❌ Nomor WhatsApp tidak valid.\n"
            "Harus dimulai dari 08 dan minimal 10 digit.\n"
            "Coba lagi:"
        )
        return REGISTER_WHATSAPP
    
    context.user_data['reg_whatsapp'] = whatsapp
    await update.message.reply_text(
        f"✅ No. WhatsApp: {whatsapp}\n\n"
        "Buat kata sandi baru (minimal 4 karakter):"
    )
    return REGISTER_PASSWORD

async def handle_register_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle registration password input"""
    password = update.message.text.strip()
    
    if len(password) < 4:
        await update.message.reply_text(
            "❌ Kata sandi harus minimal 4 karakter.\n"
            "Coba lagi:"
        )
        return REGISTER_PASSWORD
    
    context.user_data['reg_password'] = password
    await update.message.reply_text(
        "Konfirmasi kata sandi.\n"
        "Ketikkan ulang kata sandi yang sama:"
    )
    return REGISTER_PASSWORD_CONFIRM

async def handle_register_password_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle password confirmation"""
    password_confirm = update.message.text.strip()
    
    if password_confirm != context.user_data.get('reg_password'):
        await update.message.reply_text(
            "❌ Kata sandi tidak cocok.\n"
            "Coba lagi:"
        )
        return REGISTER_PASSWORD_CONFIRM
    
    # Show confirmation summary
    summary = (
        "📝 *RINGKASAN DATA REGISTRASI*\n\n"
        f"👤 Nama: {context.user_data.get('reg_name')}\n"
        f"📱 No. HP: {context.user_data.get('reg_phone')}\n"
        f"📧 Email: {context.user_data.get('reg_email')}\n"
        f"💬 WhatsApp: {context.user_data.get('reg_whatsapp')}\n\n"
        "✅ Apakah data sudah benar?"
    )
    
    keyboard = [
        [InlineKeyboardButton("✅ Ya, Lanjutkan", callback_data='confirm_yes')],
        [InlineKeyboardButton("❌ Tidak, Ubah", callback_data='confirm_no')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        summary,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return REGISTER_CONFIRM

async def handle_register_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle registration confirmation"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'confirm_yes':
        # Save user to database
        email = context.user_data.get('reg_email')
        USERS_DB[email] = {
            'name': context.user_data.get('reg_name'),
            'phone': context.user_data.get('reg_phone'),
            'email': email,
            'whatsapp': context.user_data.get('reg_whatsapp'),
            'password': context.user_data.get('reg_password'),
            'registered_at': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            'status': 'active'
        }
        save_users()
        
        await query.edit_message_text(
            "✅ *REGISTRASI BERHASIL*\n\n"
            "🎉 Akun Anda telah terdaftar!\n\n"
            "Anda sekarang dapat login dengan:\n"
            f"📧 Email: {email}\n"
            f"📱 atau No. HP: {context.user_data.get('reg_phone')}\n\n"
            "👉 Gunakan /start untuk login.",
            parse_mode='Markdown'
        )
    else:
        await query.edit_message_text(
            "📝 Mari kita mulai lagi.\n"
            "Ketikkan nama lengkap Anda:"
        )
        return REGISTER_NAME
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel conversation"""
    await update.message.reply_text(
        "❌ Dibatalkan.\n\nGunakan /start untuk menu utama.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help information"""
    help_text = (
        "🤖 *BANTUAN BOT SIPENDUDUK*\n\n"
        "*Perintah Tersedia:*\n"
        "`/start` - Menu utama\n"
        "`/help` - Bantuan\n"
        "`/cancel` - Batalkan proses\n\n"
        "*Fitur:*\n"
        "🔐 Login - Masuk ke akun Anda\n"
        "📝 Daftar - Buat akun baru\n"
        "ℹ️ Info - Informasi bot\n\n"
        "*Kontak:*\n"
        "📧 Email: admin@sipenduduk.pekanbaru.go.id\n"
        "🌐 Website: https://sipenduduk.pekanbaru.go.id"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    """Main function to run the bot"""
    # Load existing users
    load_users()
    logger.info(f"Loaded {len(USERS_DB)} users from database")
    
    # Create the Application
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    
    app = Application.builder().token(token).build()
    
    # Add conversation handler for login
    login_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern='login')],
        states={
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_login_password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Add conversation handler for registration
    register_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback, pattern='register')],
        states={
            REGISTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_register_name)],
            REGISTER_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_register_phone)],
            REGISTER_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_register_email)],
            REGISTER_WHATSAPP: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_register_whatsapp)],
            REGISTER_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_register_password)],
            REGISTER_PASSWORD_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_register_password_confirm)],
            REGISTER_CONFIRM: [CallbackQueryHandler(handle_register_confirm)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    # Add handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('cancel', cancel))
    app.add_handler(login_handler)
    app.add_handler(register_handler)
    app.add_handler(CallbackQueryHandler(button_callback, pattern='^(info)$'))
    
    # Run the bot
    logger.info("🚀 Bot Telegram Sipenduduk Pekanbaru dimulai...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
