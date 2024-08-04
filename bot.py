import logging
import os
import time

import requests
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, \
    CallbackQueryHandler, CallbackContext
from public.data import ChatUser
from public.menu import *
from config import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    from_user = update.effective_user
    if ChatUser().get(from_user):
        print(111)
        await update.message.reply_text(text="1111111", reply_markup=Default_menu())
    else:
        print(2211122)

        ChatUser().post(from_user)
        await update.message.reply_text(text="1111111", reply_markup=Default_menu())



async def get_chat_history(update: Update, context: CallbackContext):
    await update.message.reply_text('请点击以下按钮：', reply_markup=message_menu())

async def button_event(update: Update, context: CallbackContext):
    query = update.callback_query
    print(query)
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")
# 监听所有文本消息
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    current_time = time.time()
    if chat_id in last_message_time:
        print(1)
        time_passed = current_time - last_message_time[chat_id]
        if time_passed < MESSAGE_INTERVAL:
            # 如果消息间隔时间小于设定值，不发送消息
            await update.message.reply_text(
                f"请等待至少 {MESSAGE_INTERVAL} 秒后再发送消息。",
                reply_to_message_id=message_id  # 回复被删除的消息
            )
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

            return

    # 更新最后一条消息时间
    last_message_time[chat_id] = current_time
    # 执行你的消息处理逻辑
    # 这里只是一个回显示例
    # await update.messcat age.reply_text(update.message.text)


async def send_video_in_chunks(update: Update, context: ContextTypes.DEFAULT_TYPE, video_path: str,
                               chunk_size: int = 1024 * 1024* 10):
    try:
        file_size = os.path.getsize(video_path)
        with open(video_path, 'rb') as video_file:
            start_byte = 0
            while start_byte < file_size:
                end_byte = min(start_byte + chunk_size, file_size)
                print(end_byte)
                video_file.seek(start_byte)
                chunk_data = video_file.read(end_byte - start_byte)
                print(chunk_data)

                files = {'video': ('video_path', chunk_data)}

                response = requests.post(
                    url=f'https://api.telegram.org/bot{context.bot.token}/sendVideo',
                    data={'chat_id': update.message.chat_id, 'supports_streaming': True},
                    files=files
                )

                if response.status_code != 200:
                    raise Exception(f"Error sending video chunk: {response.content}")

                start_byte = end_byte

    except Exception as e:
        print(f"Error: {e}")
async def sendvideo(update: Update, context: ContextTypes.DEFAULT_TYPE):
        video_path = 'IMG_8711.MP4'
        with open(video_path, 'rb') as video_file:
            await context.bot.send_video(
                chat_id=update.message.chat_id,
                video=InputFile(video_file),
                supports_streaming=True,
                connect_timeout=120  # 增加超时时间
            )
if __name__ == '__main__':
    application = ApplicationBuilder().token('').build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('sendvideo', sendvideo))
    application.add_handler(CommandHandler('get_chat_history', get_chat_history))
    application.add_handler(CallbackQueryHandler(button_event))

    application.run_polling()
