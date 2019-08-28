#!/usr/bin/env python
#coding:utf-8

#Author:sisul

from scripts.handle_mysql import HandleMysql
from scripts.handle_request import HttpRequest
from scripts.handle_config import do_config
from scripts.constants import USER_ACCOUNTS_FILE_PATH


def create_new_user(regname, pwd='123456'):
	'''创建一个账户'''
	handle_mysql = HandleMysql()
	send_request = HttpRequest()
	url = do_config.get_value('api', 'prefix_url') + '/member/register'
	sql = 'select id from member where MobilePhone=%s;'
	while True:
		mobilephone = handle_mysql.create_not_existed_mobile()
		data = {'mobilephone':mobilephone, 'pwd':pwd, 'regname':regname}
		send_request.to_request(method='post',
								url=url,
								data=data)
		result = handle_mysql.to_run(sql=sql, args=(mobilephone,))
		if result:
			user_id = result['id']
			break

	user_dict = {
		regname: {
			'Id': user_id,
			'regname': regname,
			'mobilephone': mobilephone,
			'pwd': pwd
		}
	}
	handle_mysql.close()
	send_request.close()

	return user_dict

def generate_users_config():
	'''
	生成三个用户信息
	:return:
	'''
	user_datas_dict = {}
	user_datas_dict.update(create_new_user('admin_user'))
	user_datas_dict.update(create_new_user('invest_user'))
	user_datas_dict.update(create_new_user('browser_user'))
	do_config.write_config(user_datas_dict, USER_ACCOUNTS_FILE_PATH)

if __name__ == '__main__':
	generate_users_config()