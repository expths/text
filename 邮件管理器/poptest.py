import poplib
from email import parser

# Gmail不再接受pop请求。


pop_server = 'pop.gmail.com'
email_address = 'your.email@gmail.com'
email_password = 'your_password'

# 连接到 Gmail POP3 服务器
pop_conn = poplib.POP3_SSL(pop_server, 995)
pop_conn.user(email_address)
pop_conn.pass_(email_password)

# 获取邮箱中的邮件数量和占用空间
num_messages = len(pop_conn.list()[1])
print(f"Total emails: {num_messages}")

# 获取最新一封邮件
latest_email_index = num_messages
resp, raw_email, octets = pop_conn.retr(latest_email_index)
raw_email = b'\n'.join(raw_email)
email_message = parser.BytesParser().parsebytes(raw_email)

# 打印邮件主题和发件人
print(f"Subject: {email_message['subject']}")
print(f"From: {email_message['from']}")

# 关闭连接
pop_conn.quit()
