from imbox import Imbox
import configparser


server = "outlook.office365.com"
try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    user = config.get('outlook','user')
    password = config.get('outlook','password')
except FileNotFoundError:
    print("[ERR]配置文件缺失")
except configparser.NoSectionError:
    print("缺失配置")
except configparser.NoOptionError:
    print("找不到字段")


# message对象方法
# message.sent_from
# message.sent_to
# message.subject
# message.headers
# message.message_id
# message.date
# message.body 包括plain和html

with Imbox(hostname=server,
           username=user,
           password=password,) as imbox:
    all_inbox_messages = imbox.messages()
    n = 0
    for uid,message in all_inbox_messages:
        n += 1
        print(n)
        if len(message.sent_from)>1:
            print(message.body)


