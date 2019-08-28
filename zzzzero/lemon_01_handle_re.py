#!/usr/bin/env python
#coding:utf-8

#Author:sisul

import re

one_str = '{"mobilephone":"${not_exited_tel}", "pwd":"123456", "regname":"sisul"}'
#match方法，第一个参数，为字符串或者pattern对象
#第二个参数一定为字符串(原始字符串)
#match是从头开始查找
#如果匹配不上，那么返回None对象
#如果能匹配，那么返回match对象
# 2.使用match方法匹配
# mtch = re.match(r'{"mobile', one_str)       #模板 模子
# mtch.group()     #获取匹配到的结果


#3.search方法
# res = re.search(r'exited', one_str)

#4.sub方法
res = re.sub(r'\$\{not_exited_tel\}', '18252061000', one_str)

pass