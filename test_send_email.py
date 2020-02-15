# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/2/1 17:46'

import smtplib
import datetime
from email.mime.text import MIMEText
from email.header import Header

from users.models import  EmailVerfyRecode

def test_send_email():
	EMAIL_HOST = 'smtp.qq.com'  # 使用SMTP服务器，需要在邮箱中开启此服务
	EMAIL_PORT = 587
	EMAIL_HOST_USER = '1725128685@qq.com'
	EMAIL_HOST_PASSWORD = 'axmoyvogwnfqfdcb'

	EMAIL_FROM = '1725128685@qq.com'  # 自定义配置，使用时需要引入

	receivers = ['1725128685@qq.com']

	message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
	message['From'] = Header("菜鸟教程", 'utf-8')
	message['To'] = Header("测试", 'utf-8')

	subject = 'Python SMTP 邮件测试'
	message['Subject'] = Header(subject, 'utf-8')
	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(EMAIL_HOST, EMAIL_PORT)
		smtpObj.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
		smtpObj.sendmail(EMAIL_FROM, receivers, message.as_string())
		print("邮件发送成功")
	except smtplib.SMTPException:
		print("Error: 无法发送邮件")


def test_datetime():
	now_time = datetime.datetime.now()
	email_date = EmailVerfyRecode.objects.get(id = 12)
	send_time = email_date.get_send_time()
	print(type((send_time-now_time).seconds))


if __name__ == '__main__':
	test_datetime()
