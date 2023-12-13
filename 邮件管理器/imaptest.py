import imaplib
import email
from email.header import decode_header
import configparser

# 官方文档：https://docs.python.org/zh-cn/3/library/imaplib.html
# 在最终解析之前，调用print函数只会显示一个莫名其妙的二进制字符，但实际上是列表等对象。

server = "outlook.office365.com"
try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    user = config.get('outlook','user')
    password = config.get('outlook','password')
except FileNotFoundError:
    print("[ERR]配置文件缺失")
    config['outlook'] = {'user':'','password':''}
    with open('config.ini',mode='w')as config_file:
        config.write(config_file)
except configparser.NoSectionError:
    config['outlook'] = {'user':'','password':''}
    with open('config.ini',mode='w')as config_file:
        config.write(config_file)


conn = imaplib.IMAP4_SSL(server)
conn.login(user,password)
a = conn.select()[1][0].split()
for i in a:
    status, msg_data = conn.fetch(i, '(RFC822)')
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)
    subject, encoding = decode_header(msg["Subject"])[0]
    # subject = subject.decode(encoding or "utf-8")
    from_ = msg.get("From")
    print(f"Subject: {subject}")
    print(f"From: {from_}")

conn.logout()