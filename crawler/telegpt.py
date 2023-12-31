import logging
import asyncio
import configparser
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,NoSuchWindowException,WebDriverException

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config.get("telegram","token")
except FileNotFoundError:
    print("[ERR]配置文件缺失")
except configparser.NoSectionError:
    print("[ERR]缺失token配置")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    update包含来自 Telegram 本身的所有信息和数据。 
    context包含有关库本身状态的信息和数据。 
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    回显它收到的所有非命令消息。 

    filters模块包含许多所谓的过滤器用于过滤传入消息的文本、图像、状态更新等。
    任何返回的消息对于至少一个传递给的过滤器 MessageHandler将被接受。
    如果需要，您还可以编写自己的过滤器。
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    将输入参数转换为大写字符。

    context.args是一个CallbackContext参数列表。
    """
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def callback_alarm(context: ContextTypes.DEFAULT_TYPE):
    """
    队列回调函数。在机器人中处理延迟任务、计划任务等应该使用队列功能，否则会产生阻塞。
    """
    # Beep the person who called this alarm:
    await context.bot.send_message(chat_id=context.job.chat_id, text=f'BEEP {context.job.data}!')

    # 可以递归
    context.job_queue.run_once(callback_alarm, 60, data=context.job.data, chat_id=context.job.chat_id)
 
 
async def callback_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler回调中context内部有一个job_queue对象。

    向回调函数中提供的id、data等数据可以通过job对象取得。
    """
    chat_id = update.message.chat_id
    name = update.effective_chat.full_name
    await context.bot.send_message(chat_id=chat_id, text='Setting a timer for 1 minute!')
    context.job_queue.run_once(callback_alarm, 60, data=name, chat_id=chat_id)


async def put(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Usage: /put value

    程序可以在上下文内部保存用户数据，这些数据将会在整个进程中共享。
    通过context.user_data访问。
    """
    # Generate ID and separate value from command
    key = str()#(uuid.uuid4())
    # We don't use context.args here, because the value may contain whitespaces
    value = update.message.text.partition(' ')[2]

    # Store value
    context.user_data[key] = value
    # Send the key to the user
    await update.message.reply_text(key)

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Usage: /get uuid"""
    # Separate ID from command
    key = context.args[0]

    # Load value and send it to the user
    value = context.user_data.get(key, 'Not found')
    await update.message.reply_text(value)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    timer_handler = CommandHandler('timer', callback_timer)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(timer_handler)
    
    application.run_polling()