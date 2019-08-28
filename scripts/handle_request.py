#!/usr/bin/env python
#coding:utf-8

#Author:sisul

import requests
import json

class HttpRequest:

	'''处理请求'''
	def __init__(self):
		self.one_session = requests.Session()

	def to_request(self, method, url, data=None, is_json=False, **kwargs):
		method = method.upper()
		if isinstance(data, str):
			try:
				data = json.loads(data)
			except Exception as e:
				print('异常为:{}'.format(e))
				data = eval(data)


		if method == 'GET':
			res = self.one_session.request(method=method, url=url, params=data, **kwargs)

		elif method == 'POST':
			if is_json:
				res = self.one_session.request(method=method, url=url, json=data, **kwargs)
			else:
				res = self.one_session.request(method=method, url=url, data=data, **kwargs)
		else:
			res = None
			print('次请求方法【{}】，不允许')
		return res
	def close(self):
		self.one_session.close()


if __name__ == '__main__':
	#1.构造请求url
	register_url = 'http://tj.lemonban.com/futureloan/mvc/api/member/register'
	login_url = 'http://tj.lemonban.com/futureloan/mvc/api/member/login'
	recharge_url = 'http://tj.lemonban.com/futureloan/mvc/api/member/recharge'

	#2.创建请求参数
	# login_params = {
	# 	'mobilephone':'18252061003',
	# 	'pwd':'123456'
	# }

	#注册参数
	register_params = {
		'mobilephone':'18252061003',
	 	'pwd':'123456',
		'regname':'sisul'
	}


	#登录参数
	login_params = '{"mobilephone":"18252061003", "pwd":"123456"}'
	#充值参数
	recharge_params = {
		'mobilephone':'18252061003',
		'amount':2000
	}
	headers = {
		'User-Agent':'Mozilla/5.0 sisul'
	}
	do_request = HttpRequest()

	#注册
	register_res = do_request.to_request('post', url=register_url, data=register_params, headers=headers)

	#先登录，
	login_res = do_request.to_request('post', url=login_url, data=login_params, headers=headers)

	#再充值
	recharge_res = do_request.to_request('post', url=recharge_url, data=recharge_params, headers=headers)