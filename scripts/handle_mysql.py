#!/usr/bin/env python
#coding:utf-8

#Author:sisul

import pymysql
from scripts.handle_config import do_config
import string
import random

class HandleMysql:
	'''
	处理mysql
	'''
	def __init__(self):
		self.conn = pymysql.connect(host=do_config.get_value('mysql','host'),
							   user=do_config.get_value('mysql','user'),
							   password=do_config.get_value('mysql','password'),
							   db=do_config.get_value('mysql','db'),
							   port=do_config.get_int('mysql','port'),
							   charset=do_config.get_value('mysql','charset'),
							   cursorclass=pymysql.cursors.DictCursor)
		self.cursor = self.conn.cursor()

	def get_value(self,sql,args=None):
		self.cursor.execute(sql,args)
		self.conn.commit()

		return self.cursor.fetchone()

	def to_run(self,sql,args=None, is_more=False):
		self.cursor.execute(sql, args)
		self.conn.commit()

		if is_more:
			return self.cursor.fetchall()
		else:
			return self.cursor.fetchone()

	def close(self):
		self.cursor.close()
		self.conn.close()

	@staticmethod
	def create_mobile():
		start_mobile = ['130', '151', '182', '156']
		area_8 =  ''.join([str(x) for x in random.sample(string.digits, 8)])
		new_phone = start_mobile[random.randint(0,3)] + area_8
		return new_phone

	def is_existed_mobile(self, mobile):

		sql = 'select MobilePhone from member where MobilePhone=%s;'
		if self.to_run(sql, args=(mobile,)):
			return True
		else:
			return False

	def create_not_existed_mobile(self):
		while True:
			one_mobile = self.create_mobile()
			if not self.is_existed_mobile(one_mobile):
				break

		return one_mobile

	def get_existed_mobile(self):
		# sql = 'select MobilePhone from member limit 0,1;'                       #随机的
		sql = 'select MobilePhone from member where MobilePhone="18252061003";'  #自己用的
		one_mobile = self.to_run(sql)
		return one_mobile['MobilePhone']



if __name__ == '__main__':
	sql1 = 'select * from member limit 0,10;'
	sql2 = 'select RegName, LeaveAmount from member where MobilePhone=%s'

	do_mysql = HandleMysql()
	result = do_mysql.to_run(sql1)
	print(result)

	result2 = do_mysql.to_run(sql2, args=('18252061003',))
	print(result2)

	p = do_mysql.create_mobile()
	print(p)

	mobile = do_mysql.get_existed_mobile()
	print(mobile)



