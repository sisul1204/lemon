#!/usr/bin/env python
#coding:utf-8

#Author:sisul
from configparser import ConfigParser
from scripts.constants import CONFIG_FILE_PATH


class HandleConfig:
    """

    """
    def __init__(self, filename=None):
        self.filename = filename
        self.config = ConfigParser()
        self.config.read(self.filename, encoding='utf-8')

    def get_value(self, section, option):
        """

        :param section:
        :param option:
        :return:
        """
        return self.config.get(section, option)

    def get_int(self, section, option):
        """

        :param section:
        :param option:
        :return:
        """
        return self.config.getint(section, option)

    def get_float(self, section, option):
        """

        :param section:
        :param option:
        :return:
        """
        return self.config.getfloat(section, option)

    def get_boolean(self, section, option):
        """

        :param section:
        :param option:
        :return:
        """
        return self.config.getboolean(section, option)

    def get_eval_data(self, section, option):
        """

        :param section:
        :param option:
        :return:
        """
        return eval(self.get_value(section, option))

    @staticmethod
    def write_config(datas, filename):
        """

        :param data:
        :param filename:
        :return:
        """
        config = ConfigParser()
        for key in datas:
            config[key] = datas[key]

        # 3. 保存到文件
        with open(filename, 'w') as file:
            config.write(file)


do_config = HandleConfig(CONFIG_FILE_PATH)

if __name__ == '__main__':
    # do_config = HandleConfig("testcase.conf")
    # print(do_config.get_eval_data("excel", "seven_var"))
    datas = {
        "file path": {'cases_path': 'cases.xlsx', 'log_path': 'record_run_result.txt'},
        "msg": {'success_result': 'Pass', 'fail_result': 'Fail'}
    }
    write_filename = "write_config2.ini"
    HandleConfig.write_config(datas, write_filename)
