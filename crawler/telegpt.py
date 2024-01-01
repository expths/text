import logging
import asyncio
import pyotp
import sqlite3
import configparser
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,NoSuchWindowException,WebDriverException

# API文档：https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API

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

cookie_db =  sqlite3.connect("data/cookies.db")
cur = cookie_db.cursor()


cookies_file = "cookies/binance.json"
Authenticator = pyotp.parse_uri("")


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
    # context.job_queue.run_once(callback_alarm, 60, data=context.job.data, chat_id=context.job.chat_id)
 
 
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


async def get_my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    获取浏览器当前的页面标题和会话句柄。
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"ID: {update.effective_chat.id}")



def async_decorator(func):
    """
    异步程序装饰器。
    """
    async def f(update: Update, context: ContextTypes.DEFAULT_TYPE):
        return await func(update, context)
    return f

async def get_window(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    获取浏览器当前的页面标题和会话句柄。
    """
    window = driver.title
    handle = driver.current_window_handle
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"当前页面{window}\n{handle}")


class Tabdriver:
    """
    浏览器标签页对象类。

    负责给每一个应用提供一个标签页。
    自动检查浏览器是否存活，标签页是否存活。
    """

    driver:webdriver # 所有对象共享一个浏览器实例
    logger:logging.Logger = logging.getLogger('BroxserDriver')
    tabs:set = set()

    @classmethod
    def broxser_open(cls):
        """
        启动浏览器。
        """
        # 配置浏览器
        options = webdriver.FirefoxOptions()
        options.add_argument("--auto-open-devtools-for-tabs")
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(2)
        cls.driver = driver

        # 将初始标签页标记为初始供使用。
        cls.tabs[driver.current_window_handle] = 'init'

    @classmethod
    def is_opened(cls):
        """
        检查浏览器是否正在运行？
        """
        try:
            # 测试检索标签页是否发生异常
            cls.driver.window_handles
            return True
        except WebDriverException:
            # 输出日志
            cls.logger("浏览器异常关闭！")
            return False
        
        
    def __init__(self,name) -> None:

        # 申请一个标签页句柄
        for handle,app in self.tabs:
            if app == "init":
                self.window_handle = handle # 保存标签页句柄
                self.tabs[handle] = name # 将标签页标记为已用
        if self.window_handle:
            # 创建新标签页
            pass
        
    def save_cookie(self):
        """
        持久化保存浏览器中的cookie数据。
        使用telegramBot库中的DictPersistence类。
        """
        pass

    @staticmethod
    def application(func):
        """
        注册一个应用。
        将标签页对象封装到context中传入回调函数。
        """
        # 创建标签页对象
        # 使用入口函数作为应用的名称
        tab = Tabdriver(func.__name__)

        # 将它们包装起来以便用于注册到jobqueue
        async def f(context: ContextTypes.DEFAULT_TYPE):
            context.job_queue.run_once(func,1,data=tab)
        return f

async def broxser_opened(context: ContextTypes.DEFAULT_TYPE):
    """
    检查浏览器是否关闭
    """
    try:
        await context.bot.send_message(chat_id='6011203042', text=f"浏览器正常")
    except WebDriverException:
        await context.bot.send_message(chat_id='6011203042', text=f"浏览器已关闭！")


@Tabdriver.application
async def binance(context: ContextTypes.DEFAULT_TYPE):
    
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=f"当前处于{window}")
    context.job.data



async def webdriver_cli(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    通过命令访问webdriver
    """
    sh = update.message.text[5:]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"命令{sh}")




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
    application.add_handlers([
        CommandHandler('win',get_window),
        CommandHandler('cli',webdriver_cli),
        CommandHandler('id',get_my_id)
    ])
    
    # application.job_queue.run_repeating(Fdriver.broxser_opened, interval=60, first=10)
    application.run_polling()