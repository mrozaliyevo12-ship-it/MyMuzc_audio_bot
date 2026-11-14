import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from yt_dlp import YoutubeDL

# Tokeningiz
TOKEN = "8882989637:AAGv71zJgc5-N7OLeOlWirUf3mYBn9HvOdU"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Start komandasi
@dp.message(F.text == "/start")
async def start_cmd(message: types.Message):
    await message.answer("Salom! Menga YouTube havolasini yuboring, men uni faqat **audio (musiqa)** shaklida yuklab beraman.")

# Havola kelganda faqat audio yuklash
@dp.message(F.text.startswith("http"))
async def download_audio(message: types.Message):
    url = message.text.strip()
    processing_msg = await message.answer("⏳ Audio yuklanmoqda, iltimos kuting...")
    
    loop = asyncio.get_event_loop()
    file_path = None
    
    try:
        # Faqat eng yaxshi audio formatni tanlash sozlamasi
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
        }
        
        def run_ytdl():
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info), info.get('title', 'Audio')
        
        file_path, title = await loop.run_in_executor(None, run_ytdl)
        
        # Ovoz faylini yuborish
        audio = types.FSInputFile(file_path)
        await message.answer_audio(audio=audio, title=title)
        
        # Faylni kompyuterdan o'chirish
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        await processing_msg.delete()
        
    except Exception as e:
        await processing_msg.edit_text(f"❌ Xatolik yuz berdi: {e}")

# Botni ishga tushirish
async def main():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())