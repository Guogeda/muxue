# _*_ coding:utf-8 _*_
__author__ = 'geda'
__date__ = '2020/1/31 20:23'
import string
import random

from django.core.mail import send_mail

from users.models import EmailVerfyRecode
from muxue.settings import EMAIL_FROM


def gene_code_email(random_code_length=8):
	"""生成随机邮箱验证码，作为验证链接的一部分"""
	random_code = ''
	chars = string.ascii_letters + str(string.digits)
	chars_length = len(chars)
	for i in range(random_code_length - 1):
		random_code += chars[random.randint(0, chars_length - 1)]
	return random_code


def send_code_email(email, send_type='register'):
	email_record = EmailVerfyRecode()
	if send_type == 'update':
		code = gene_code_email(5)
	else:
		code = gene_code_email(8)
	email_record.email = email
	email_record.code = code
	email_record.type = send_type

	if send_type == 'register':
		email_subject = '在线学习网激活邮件（请勿回复）'
		email_message = '欢迎您注册在线学习网账号，请点击下面的链接完成激活:\nhttp://127' \
						'.0.0.1:8000/active/' + email_record.code
		send_mail(email_subject, email_message, EMAIL_FROM, [email])
		email_record.save()

	elif send_type == 'forget':
		email_subject = '在线学习网重置密码邮件（请勿回复）'
		email_message = '请点击下面重置密码的链接:\nhttp://127' \
						'.0.0.1:8000/reset/' + email_record.code
		send_mail(email_subject, email_message, EMAIL_FROM, [email])
		email_record.save()

	elif send_type == 'update':
		email_subject = '在线学习网重置密码邮件（请勿回复）'
		email_message = '瓜皮，您的重置邮箱验证码是{}' .format(email_record.code)
		send_mail(email_subject, email_message, EMAIL_FROM, [email])
		email_record.save()
	else:
		pass


