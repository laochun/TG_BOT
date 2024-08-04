import asyncio
from aiohttp import ClientSession
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram bot token
TOKEN = 'your_bot_token_here'

# 处理 /start 命令的函数
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('你好！发送一个消息包含链接我将帮你提取内容。')

# 处理用户发送的消息的函数
async def extract_link_content(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text.startswith('http'):
        try:
            async with ClientSession() as session:
                async with session.get(text) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        # 处理页面内容
                        # 这里可以使用 BeautifulSoup 或其他方式解析页面内容
                        title = "Some Title"  # 示例中使用假标题
                        await update.message.reply_text(f'链接标题：{title}')
                    else:
                        await update.message.reply_text('无法获取链接内容。')
        except Exception as e:
            await update.message.reply_text(f'出现错误：{str(e)}')
    else:
        await update.message.reply_text('请发送一个包含链接的消息。')

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
