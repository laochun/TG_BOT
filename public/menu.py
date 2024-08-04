from telegram import ReplyKeyboardMarkup, Update, KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ContextTypes

def message_menu():
    keyboard = [
        [InlineKeyboardButton("点击分享", callback_data='1'),InlineKeyboardButton("点击使用", callback_data='2')],
        [InlineKeyboardButton("各种资源搜索🔍", callback_data='3'),InlineKeyboardButton("万能搜索群", callback_data='4')],

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # update.message.reply_text('Please choose:', reply_markup=reply_markup)
    return reply_markup
# 处理按钮点击的函数


def Default_menu():
    """# 创建 ReplyKeyboardMarkup 对象，参数说明:
    # - keyboard: 包含按钮的二维数组
    # - resize_keyboard: 自动调整键盘大小以适应按钮数量，默认为 True
    # - one_time_keyboard: 显示一次后自动隐藏键盘，默认为 False
    # - selective: 如果为 True，只有发送消息的用户可以看到键盘，默认为 False"""
    keyboard = [
            # 第一行按钮
            [KeyboardButton('📚使用方法')],
            # 第二行按钮
            [KeyboardButton('💴会员充值'), KeyboardButton('💻点击试用')],
            # 第三行按钮
            [KeyboardButton('🔥更多机器人', request_contact=True), KeyboardButton('🧠联系客服', request_location=True)],
            # #颜色按钮
            # [KeyboardButton('Button 3', callback_data='button3', color=telegram.KeyboardButtonColor.POSITIVE)],
            # [KeyboardButton('Button 4', callback_data='button4', color=telegram.KeyboardButtonColor.NEGATIVE)]
         ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False, selective=True)
    return reply_markup