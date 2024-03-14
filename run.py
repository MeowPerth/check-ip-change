import os
import requests
import re
import time
# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
# 构建邮件头
from email.header import Header

class ENV:
  def __init__(self):
    if(os.environ.get("FROM_EMAIL") == None):
      raise Exception("请配置发送邮箱账户！")
    if(os.environ.get("FROM_EMAIL_PASSWORD") == None):
      raise Exception("请配置发送邮箱授权密码！")
    api_str = "https://ddns.oray.com/checkip, https://ip.3322.net" if os.environ.get("API") == None else os.environ.get("API")
    api_list = api_str.split(",")
    # 对不符合规范添加 http请求头， 使 api 符合协议
    for i in range(len(api_list)):
      match = re.match("http", api_list[i])
      if(match == None):
        api_list[i] = "http://" + api_list[i]
    self.api_list = api_list
    self.from_name = '' if os.environ.get("FROM_NAME") == None else (os.environ.get("FROM_NAME"))
    self.from_email = os.environ.get("FROM_EMAIL")
    self.from_email_password = os.environ.get("FROM_EMAIL_PASSWORD")
    to_emails = self.from_email if os.environ.get("TO_EMAIL")  == None else os.environ.get("TO_EMAIL")
    to_email_list = to_emails.split(",")
    self.to_email_list = to_email_list
    self.smtp_server = "smtp.qq.com" if os.environ.get("SMTP_SERVER") == None else os.environ.get("SMTP_SERVER")
    self.smtp_port = 465 if os.environ.get("SMTP_PORT") == None else (int)(os.environ.get("SMTP_PORT"))
    self.interval = 60 if os.environ.get("INTERVAL") == None else (int)(os.environ.get("INTERVAL"))
    self.email_title = 'IP 地址改变提醒' if os.environ.get("EMAIL_TITLE") == None else (os.environ.get("EMAIL_TITLE"))
    self.email_header = '服务器检测到当前 ip 地址发生改变！' if os.environ.get("EMAIL_HEADER") == None else (os.environ.get("EMAIL_HEADER"))
    self.email_footer = '来自 Check IP Change' if os.environ.get("EMAIL_FOOTER") == None else (os.environ.get("EMAIL_FOOTER"))

def current_ip(api_list):
  headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"}
  for api in api_list:
    html = requests.get(api, headers=headers)
    if(html.status_code == 200):
      ocurrent_ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}',html.text)[0]
      return ocurrent_ip
  print("所有获取公网的 api 均不可用")

def sendmail(old_ip, ocurrent_ip, env):
  # 发信方的信息：发信邮箱，QQ 邮箱授权码
  from_name = env.from_name
  from_addr = env.from_email
  password = env.from_email_password
  email_header = env.email_header
  email_footer = env.email_footer
  # 发信服务器
  smtp_server = env.smtp_server
  smtp_port = env.smtp_port
  template = """
  <p>{0}</p>
  <p>原 ip 地址: {1}<br>现 ip 地址: {2}</p><br>
  <p>{3}</p>
  """
  html_msg = template.format(email_header, old_ip, ocurrent_ip, email_footer)
  # 创建一个带附件的实例msg
  msg = MIMEMultipart()
  msg['From'] = formataddr((from_name, from_addr))  # 发送者
  msg['To'] = ','.join(env.to_email_list)  #接受者
  msg['Subject'] = Header(env.email_title, 'utf-8')  # 邮件主题
  # 邮件正文内容
  msg.attach(MIMEText(html_msg, 'html', 'utf-8'))
  try:
    smtpobj = smtplib.SMTP_SSL(smtp_server)
    smtpobj.connect(smtp_server, smtp_port)    # 建立连接--qq邮箱服务和端口号
    smtpobj.login(from_addr, password)   # 登录--发送者账号和口令
    for to_addr in env.to_email_list:    # 给所有接收者发信
    	smtpobj.sendmail(from_addr, to_addr, msg.as_string())
    print("邮件发送成功")
  except smtplib.SMTPException as e:
    print("无法发送邮件:", str(e))
  finally:
    # 关闭服务器
    smtpobj.quit()

if __name__ == '__main__':
  # 初始化变量
  env = ENV()
  ip_file = "/old_ip.txt"
  try:
    with open(ip_file, "r") as file:
      old_ip = file.read().strip()
  except FileNotFoundError:
      old_ip = "127.0.0.1"
  print("旧的 IP 地址：", old_ip)
  while True:
    ocurrent_ip = current_ip(env.api_list)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "---old_ip：" + old_ip + "，ocurrent_ip：" + ocurrent_ip)
    if(old_ip != ocurrent_ip):
      print("Ip 地址发生改变")
      sendmail(old_ip, ocurrent_ip, env)
      old_ip = ocurrent_ip
      with open(ip_file, "w") as file:
        file.write(old_ip)
    time.sleep(env.interval) 
