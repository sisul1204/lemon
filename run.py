#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : sisul

import unittest
import os

import HTMLTestRunnerNew
from scripts.constants import REPORTS_DIR
from scripts.handle_config import do_config
from datetime import datetime
from scripts.constants import USER_ACCOUNTS_FILE_PATH, CASES_DIR
from scripts.handle_user import generate_users_config

if not os.path.exists(USER_ACCOUNTS_FILE_PATH):    #如果用户账号所在文件不存在，则创建用户账号
	generate_users_config()

#1.创建套件
# one_suite = unittest.TestSuite()

#2.加载用例
#创建加载器对象
# one_loader = unittest.TestLoader()
# one_suite.addTest(one_loader.loadTestsFromModule(register))

one_suite = unittest.defaultTestLoader.discover(CASES_DIR, pattern='test*.py')


#3.运行用例

report_name = do_config.get_value('report', 'report_html_name') + \
			  datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") +'.html'
report_full_path = os.path.join(REPORTS_DIR, report_name)
# print(report_full_path)
with open(report_full_path, mode='wb') as save_to_file:
	one_runner = HTMLTestRunnerNew.HTMLTestRunner(
		stream=save_to_file,
		verbosity=do_config.get_int('report', 'verbosity'),
		title=do_config.get_value('report', 'title'),
		description=do_config.get_value('report', 'description'),
		tester=do_config.get_value('report', 'tester')
	)
	one_runner.run(one_suite)









