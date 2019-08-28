#!/usr/bin/env python
#coding:utf-8

#Author:sisul

import unittest
from libs.ddt import ddt, data
import json
from scripts.handle_excel import HandleExcel
from scripts.handle_config import do_config
from scripts.handle_log import do_logger
from scripts.constants import TESTS_DATAS_FILES
from scripts.handle_context import Context
from scripts.handle_request import HttpRequest
from scripts.handle_mysql import HandleMysql


do_excel = HandleExcel(TESTS_DATAS_FILES, 'add')
cases = do_excel.get_cases()

@ddt
class TestAdd(unittest.TestCase):
	'''测试加标接口'''
	@classmethod
	def setUpClass(cls):
		cls.do_request = HttpRequest()
		cls.handle_mysql = HandleMysql()   #创建HandleMysql对象
		do_logger.info('{}'.format('开始执行用例'))


	@classmethod
	def tearDownClass(cls):
		cls.do_request.close()
		cls.handle_mysql.close()
		do_logger.info('{}'.format('用例执行结束'))

	@data(*cases)
	def test_add(self,one_case):
		# data = one_case['data']           #需要进行参数化
		new_data = Context.admin_user_tel_pwd_replace(one_case['data'])     #需要实现
		new_url = do_config.get_value('api', 'prefix_url') + one_case['url']



		#向服务器发起请求
		res = self.do_request.to_request(method=one_case['method'],
										   url=new_url,
										   data=new_data)
		#期望值
		expect_result = one_case['expected']
		msg = "测试" + one_case['title']
		success_msg = do_config.get_value('msg', 'success_result')
		fail_msg = do_config.get_value('msg', 'fail_result')
		case_id = one_case['case_id']

		try:
			# self.assertEqual(str(expect_result), code, msg=msg)
			self.assertIn(str(expect_result), res.text, msg=msg)

			do_excel.write_result(case_id+1, res.text, success_msg)
			do_logger.debug('{},执行结果为：{}'.format(msg, success_msg))
		except AssertionError as e:
			do_excel.write_result(case_id+1, res.text, fail_msg)
			do_logger.error('{}, 执行结果为：{}具体异常为：{}'.format(msg, fail_msg, e))
			raise e

if __name__ == '__main__':
	unittest.main()
