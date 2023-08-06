# -*- coding: UTF-8 -*-

import os
import logging
import datetime


class NewLog:

    def __init__(self, file_name):
        filename = os.path.basename(file_name)
        self.log = logging.getLogger(filename)
        self.log_file_path = self.build_path()

        # level = INFO
        logging.basicConfig(level="DEBUG",
                            format='%(asctime)s [%(filename)s line:%(lineno)s] %(levelname)s %(message)s',
                            datefmt='%a %d %b %Y %H:%M:%S',
                            filename=self.log_file_path,
                            filemode='a')

    def get_log(self):
        return self.log

    @staticmethod
    def build_path():
        temp_path = os.path.dirname(os.path.realpath(__file__))
        # 项目中使用的ENV环境, 这时候需要去解析项目目录

        index_env = temp_path.find('ENV')
        if index_env > 0:
            project_path = temp_path[:index_env]
        else:
            project_path = temp_path

        log_path = project_path + "/static/log/"

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        log_file_path = "%sdata_factory_%s.log" % (
            log_path, datetime.datetime.now().strftime("%y%m%d"))
        return log_file_path
