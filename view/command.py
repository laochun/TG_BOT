import asyncio
from aiohttp import ClientSession
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram bot token
TOKEN = 'your_bot_token_here'

# ���� /start ����ĺ���
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('��ã�����һ����Ϣ���������ҽ�������ȡ���ݡ�')

# �����û����͵���Ϣ�ĺ���
async def extract_link_content(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text.startswith('http'):
        try:
            async with ClientSession() as session:
                async with session.get(text) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        # ����ҳ������
                        # �������ʹ�� BeautifulSoup ��������ʽ����ҳ������
                        title = "Some Title"  # ʾ����ʹ�üٱ���
                        await update.message.reply_text(f'���ӱ��⣺{title}')
                    else:
                        await update.message.reply_text('�޷���ȡ�������ݡ�')
        except Exception as e:
            await update.message.reply_text(f'���ִ���{str(e)}')
    else:
        await update.message.reply_text('�뷢��һ���������ӵ���Ϣ��')

async def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, extract_link_content))

    await updater.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
