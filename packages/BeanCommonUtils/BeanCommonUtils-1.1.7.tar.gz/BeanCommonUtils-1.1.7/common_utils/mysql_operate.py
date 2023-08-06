# -*- coding: utf-8 -*-

import pymysql
from pymysql.cursors import DictCursor


class MysqlOperate:

    @classmethod
    def mysql_conn(cls, mysql_info, dict_flag=False):
        host = mysql_info['host']
        user_name = mysql_info['user_name']
        passwd = mysql_info['passwd']
        dbname = mysql_info['dbname']
        if mysql_info.__contains__('port'):
            port = mysql_info['port']
        else:
            port = 3306
        db = pymysql.connect(host, user_name, passwd, dbname, port, charset="utf8")
        if dict_flag:
            cursor = db.cursor(DictCursor)
        else:
            cursor = db.cursor()
        return db, cursor

    @classmethod
    def mysql_insert(cls, mysql_info, query):
        db, cursor = cls.mysql_conn(mysql_info)
        cursor.execute(query)
        db.commit()
        db.close()

    @classmethod
    def mysql_insert_mul(cls, mysql_info, queries):
        db, cursor = cls.mysql_conn(mysql_info)
        for query in queries:
            cursor.execute(query)
            db.commit()

        db.close()

    @classmethod
    def new_mysql_insert(cls, mysql_info, sql_template, params=None):
        """
        替换原有的mysql_insert/update/delete方法，该方法的主要目的是防止sql注入
        :param mysql_info:
        :param sql_template: sql的模板
        :param params: 替换sql模板中的动态参数  parameters used with sql_template. (optional)
        :type params: tuple, list or dict
        :return:
        """
        db, cursor = cls.mysql_conn(mysql_info)
        cursor.execute(sql_template, params)
        res_id = db.insert_id()
        db.commit()
        db.close()
        return res_id

    @classmethod
    def new_mysql_query(cls, mysql_info, query_template, params=None):
        """
        替换原有的mysql_query方法，该方法的主要目的是防止sql注入
        :param mysql_info:
        :param query_template: 查询sql的模板
        :param params: 替换sql模板中的动态参数
        :return:
        """
        db, cursor = cls.mysql_conn(mysql_info)
        cursor.execute(query_template, params)

        # 获取所有字段名称
        col_name_list = [tuple_data[0] for tuple_data in cursor.description]
        results = cursor.fetchall()
        result_list = []
        for row in results:
            result_list.append(row)

        db.close()
        return result_list, col_name_list

    @classmethod
    def new_mysql_query_return_dict(cls, mysql_info, query_template, params=None):
        """
        替换原有的mysql_query方法，该方法的主要目的是防止sql注入
        :param mysql_info:
        :param query_template: 查询sql的模板
        :param params: 替换sql模板中的动态参数
        :return:
        """
        db, cursor = cls.mysql_conn(mysql_info, dict_flag=True)
        cursor.execute(query_template, params)
        results = cursor.fetchall()

        db.close()
        return results

    @classmethod
    def new_mysql_batch_update(cls, mysql_info, update_templates, params_list=None):
        """
        批量执行SQL, 并且保证在同一个事务中执行
        :param mysql_info:
        :param update_templates: insert/update 相关的sql的模板
        :param params_list: 替换sql模板中的动态参数
        :return:
        """
        db, cursor = cls.mysql_conn(mysql_info, dict_flag=True)
        try:
            for template_index in range(0, len(update_templates)):
                cursor.execute(update_templates[template_index], params_list[template_index])
        except Exception as e:
            db.rollback()  # 事务回滚
            raise Exception(e)
        else:
            db.commit()  # 事务提交

        db.close()
        return "操作成功"
