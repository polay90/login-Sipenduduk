# Bot Telegram Sipenduduk Pekanbaru

Bot Telegram untuk registrasi dan login sistem informasi penduduk Kota Pekanbaru.

## 🚀 Fitur

- ✅ Registrasi akun baru dengan validasi data
- ✅ Login dengan email atau nomor handphone
- ✅ Penyimpanan data pengguna (JSON)
- ✅ Interface user-friendly dengan inline buttons
- ✅ Validasi email dan nomor telepon
- ✅ Konfirmasi data sebelum registrasi

## 📋 Requirement

- Python 3.8+
- pip (Python package manager)
- Token Bot Telegram dari BotFather

## 🔧 Setup

### 1. Clone Repository
```bash
git clone <repository_url>
cd sipenduduk-telegram-bot
```

### 2. Buat Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Bot Token
Dapatkan token bot dari Telegram BotFather:
- Buka @BotFather di Telegram
- Kirim `/newbot`
- Ikuti instruksi untuk membuat bot baru
- Copy token yang diberikan

Kemudian buat file `.env`:
```bash
cp .env.example .env
# Edit .env dan masukkan TELEGRAM_BOT_TOKEN
```

### 5. Jalankan Bot
```bash
python bot.py
```

## 📱 Cara Penggunaan

### Untuk User:

1. **Cari Bot**: Cari bot Anda di Telegram (nama yang Anda berikan saat setup)
2. **Mulai**: Ketik `/start` untuk melihat menu utama
3. **Pilih Menu**:
   - 🔐 Login: Login dengan akun yang sudah terdaftar
   - 📝 Daftar: Membuat akun baru
   - ℹ️ Info: Informasi tentang bot

### Menu Registrasi:
- Masukkan nama lengkap
- Masukkan nomor handphone (08xxx...)
- Masukkan email valid
- Masukkan nomor WhatsApp
- Buat password (minimal 4 karakter)
- Konfirmasi password
- Verifikasi data

### Menu Login:
- Masukkan email atau nomor handphone
- Masukkan password
- Jika berhasil, tampil data profil

## 📁 Struktur File

```
sipenduduk-telegram-bot/
├── bot.py                 # File utama bot
├── requirements.txt       # Dependencies Python
├── .env.example          # Template environment variables
├── users.json            # Database pengguna (auto-generated)
└── README.md             # Dokumentasi ini
```

## 💾 Data Pengguna

Data pengguna disimpan dalam file `users.json` dengan format:
```json
{
  "email@example.com": {
    "name": "John Doe",
    "phone": "08123456789",
    "email": "email@example.com",
    "whatsapp": "08123456789",
    "password": "password123",
    "registered_at": "25-05-2024 10:30:00",
    "status": "active"
  }
}
```

## 🔒 Keamanan

⚠️ **PENTING**: Untuk production:
- Gunakan database yang aman (PostgreSQL, MySQL, MongoDB)
- Hash password menggunakan bcrypt atau argon2
- Implementasikan rate limiting
- Gunakan HTTPS untuk API
- Jangan simpan password plain text

## 📚 Contoh Flow

### Registrasi
```
User: /start
Bot: Tampil menu (Login, Daftar, Info)
User: Klik "Daftar Akun Baru"
Bot: Minta nama
User: "John Doe"
Bot: Minta nomor HP
User: "08123456789"
Bot: Minta email
User: "john@email.com"
Bot: Minta WhatsApp
User: "08123456789"
Bot: Minta password
User: "pass123"
Bot: Minta konfirmasi password
User: "pass123"
Bot: Tampil ringkasan data
User: Klik "Ya, Lanjutkan"
Bot: "✅ Registrasi Berhasil!"
```

### Login
```
User: /start
Bot: Tampil menu
User: Klik "Login"
Bot: Minta email/nomor HP
User: "08123456789"
Bot: Minta password
User: "pass123"
Bot: "✅ Login Berhasil! Selamat datang..."
```

## 🐛 Troubleshooting

### Bot tidak merespons
- Pastikan TELEGRAM_BOT_TOKEN sudah diset di .env
- Cek koneksi internet
- Jalankan bot dengan `python bot.py`

### Error module not found
```bash
pip install -r requirements.txt
```

### File users.json tidak terupdate
- Pastikan folder memiliki write permission
- Cek error log di console

## 🔗 Referensi

- [Dokumentasi python-telegram-bot](https://docs.python-telegram-bot.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [BotFather Commands](https://core.telegram.org/bots#botfather)

## 📞 Support

Untuk pertanyaan atau bantuan:
- 📧 Email: admin@sipenduduk.pekanbaru.go.id
- 🌐 Website: https://sipenduduk.pekanbaru.go.id

## 📄 Lisensi

Copyright © 2024 Dinas Kependudukan Kota Pekanbaru

## 👨‍💻 Author

Bot dibuat untuk Sistem Informasi Penduduk Kota Pekanbaru
