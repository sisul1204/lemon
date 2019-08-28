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


do_excel = HandleExcel(TESTS_DATAS_FILES, 'recharge')
cases = do_excel.get_cases()

@ddt
class TestRecharge(unittest.TestCase):
	'''测试充值接口'''
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
	def test_recharge(self,one_case):
		# data = one_case['data']           #需要进行参数化
		new_data = Context.recharge_parameterization(one_case['data'])     #需要实现
		new_url = do_config.get_value('api', 'prefix_url') + one_case['url']

		check_sql = one_case['check_sql']
		if check_sql:
			check_sql = Context.recharge_parameterization(check_sql)
			mysql_data = self.handle_mysql.to_run(check_sql)          #decimal.Decimal类型
			amount_before_recharge = float(mysql_data['LeaveAmount'])
			amount_before_recharge = round(amount_before_recharge, 2)
			dict_data = json.loads(new_data, encoding='utf-8')
			recharge_number = dict_data['amount']

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
		code = res.json().get('code')

		try:
			self.assertEqual(str(expect_result), code, msg=msg)
			# self.assertIn(str(expect_result), res.text, msg=msg)
			if check_sql:
				mysql_data = self.handle_mysql.to_run(check_sql)  # decimal.Decimal类型
				amount_after_recharge = float(mysql_data['LeaveAmount'])
				amount_after_recharge = round(amount_after_recharge, 2)
				self.assertEqual(recharge_number, (amount_after_recharge-amount_before_recharge), msg=msg)
			do_excel.write_result(case_id+1, res.text, success_msg)
			do_logger.debug('{},执行结果为：{}'.format(msg, success_msg))
		except AssertionError as e:
			do_excel.write_result(case_id+1, res.text, fail_msg)
			do_logger.error('{}, 执行结果为：{}具体异常为：{}'.format(msg, fail_msg, e))
			raise e

if __name__ == '__main__':
	unittest.main()
