#!/usr/bin/env python
#coding:utf-8

#Author:sisul
import re
from scripts.handle_mysql import HandleMysql
from scripts.handle_config import HandleConfig
from scripts.constants import USER_ACCOUNTS_FILE_PATH

class Context:
	'''

	'''
	not_existed_tel_parttern = r'\$\{not_exited_tel\}'
	existed_tel_parttern = r'\$\{invest_user_tel\}'
	existed_pwd_pattern = r'\$\{invest_user_pwd\}'
	borrow_user_pattern = r'\$\{borrow_user_id\}'
	admin_user_pattern = r'\$\{admin_user_tel\}'
	admin_pwd_pattern = r'\$\{admin_user_pwd\}'
	load_id_parttern = r'\$\{loan_id\}'
	invest_user_id = r'\$\{invest_user_id\}'

	do_config = HandleConfig(USER_ACCOUNTS_FILE_PATH)

	@classmethod
	def not_existed_tel_replace(cls, data):
		'''
		:param data:待替换的原始字符串
		:return:
		'''
		handle_mysql = HandleMysql()
		if re.search(cls.not_existed_tel_parttern, data):
			not_exist_tel = handle_mysql.create_not_existed_mobile()
			data = re.sub(cls.not_existed_tel_parttern, not_exist_tel, data)
		handle_mysql.close()
		return data

	@classmethod
	def existed_tel_replace(cls, data):
		handle_mysql = HandleMysql()
		if re.search(cls.existed_tel_parttern, data):
			exist_tel = handle_mysql.get_existed_mobile()
			data = re.sub(cls.existed_tel_parttern, exist_tel, data)
		handle_mysql.close()
		return data

	'''
		=左边的data是已经替换后的字符串，
		在第二次和exist模式匹配的时候不会匹配上，所以返回第一次已替换的字符串
	'''

	@classmethod
	def invest_mobile_replace(cls, data):
		if re.search(cls.existed_tel_parttern, data):
			invest_tel = cls.do_config.get_value('invest_user', 'mobilephone')
			data = re.sub(cls.existed_tel_parttern, invest_tel, data)
		return data

	@classmethod
	def invest_pwd_replace(cls, data):
		if re.search(cls.existed_pwd_pattern, data):
			invest_pwd = cls.do_config.get_value('invest_user', 'pwd')
			data = re.sub(cls.existed_pwd_pattern, invest_pwd, data)
		return data

	@classmethod
	def invest_id_replace(cls, data):
		if re.search(cls.invest_user_id, data):
			invest_id = cls.do_config.get_value('invest_user', 'id')
			data = re.sub(cls.invest_user_id, invest_id, data)
		return data

	@classmethod
	def borrow_user_replace(cls, data):
		if re.search(cls.borrow_user_pattern, data):
			borrow_user_id = cls.do_config.get_value('browser_user', 'id')
			data = re.sub(cls.borrow_user_pattern, borrow_user_id, data)
		return data

	@classmethod
	def admin_user_tel_pwd_replace(cls, data):
		if re.search(cls.admin_user_pattern, data):
			admin_user_mobile = cls.do_config.get_value('admin_user', 'mobilephone')
			data = re.sub(cls.admin_user_pattern, admin_user_mobile, data)

		if re.search(cls.admin_pwd_pattern, data):
			admin_user_pwd = cls.do_config.get_value('admin_user', 'pwd')
			data = re.sub(cls.admin_pwd_pattern, admin_user_pwd, data)

		if re.search(cls.borrow_user_pattern, data):
			borrow_user_id = cls.do_config.get_value('browser_user', 'id')
			data = re.sub(cls.borrow_user_pattern, borrow_user_id, data)
		return data

	@classmethod
	def register_parameterization(cls,data):
		data = cls.not_existed_tel_replace(data)
		#第二个，再来替换已注册的手机号码
		data = cls.existed_tel_replace(data)     #需要实现
		return data

	@classmethod
	def recharge_parameterization(cls,data):
		data = cls.invest_mobile_replace(data)
		data = cls.invest_pwd_replace(data)
		data = cls.invest_id_replace(data)
		return data

	@classmethod
	def add_parameterization(cls,data):
		data = cls.borrow_user_replace(data)
		return data

	@classmethod
	def loan_id_replace(cls, data):
		print(data, type(data))
		loan_id = getattr(cls, 'loan_id')
		print('handle里面动态获取loan_id',loan_id, type(loan_id))
		# loan_id = cls.loan_id
		if re.search(cls.load_id_parttern, data):
			print('if找到了')
			data = re.sub(cls.load_id_parttern, str(loan_id), data)
			print('handle处理后的data值', data)
		return  data


	@classmethod
	def invest_parameterization(cls, data):
		# loan_id = getattr(cls, 'loan_id')
		print('-----------------')
		print(data)
		if 'loan_id' in data:
			data = cls.loan_id_replace(data)
			print('handle处理后的data值2222222', data)
		data = cls.admin_user_tel_pwd_replace(data)
		data = cls.borrow_user_replace(data)
		data = cls.recharge_parameterization(data)
		data = cls.existed_tel_replace(data)
		return data



if __name__ =='__main__':
	data1 = '{"mobilephone":"${not_exited_tel}", "pwd":"123456", "regname":"sisul"}'
	data2 = '{"mobilephone":"${not_exited_tel}", "pwd":"123456"}'
	data3 = '{"mobilephone":"${invest_user_tel}", "pwd":"123456", "regname":"sisul"}'
	data4 = '{"mobilephone":"${invest_user_tel}","pwd":"${invest_user_pwd}"}'
	data5 = '{"id":"${loan_id}","status":4}'

	print(Context.not_existed_tel_replace(data1))
	print(Context.not_existed_tel_replace(data2))
	print(Context.existed_tel_replace(data3))
	print(Context.register_parameterization(data1))
	print(Context.register_parameterization(data2))
	print(Context.register_parameterization(data3))
	print(Context.recharge_parameterization(data4))
	print(Context.invest_parameterization(data5))
