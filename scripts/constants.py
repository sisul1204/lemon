#!/usr/bin/env python
#coding:utf-8

#Author:sisul

import os

#获取项目根路径
# one_path = os.path.abspath(__file__)
# two_path = os.path.dirname(one_path)
# three_path = os.path.dirname(two_path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

#获取测试数据datas所在目录的绝对路径
DATAS_DIR = os.path.join(BASE_DIR, 'datas')
#测试用例文件路径
TESTS_DATAS_FILES = os.path.join(DATAS_DIR, 'cases.xlsx')


#配置文件所在目录路径
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')
CONFIG_FILE_PATH = os.path.join(CONFIGS_DIR, 'testcase.conf')

LOGS_DIR = os.path.join(BASE_DIR, 'logs')

REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

USER_ACCOUNTS_FILE_PATH = os.path.join(CONFIGS_DIR, 'user_accounts.conf')

CASES_DIR = os.path.join(BASE_DIR, 'cases')