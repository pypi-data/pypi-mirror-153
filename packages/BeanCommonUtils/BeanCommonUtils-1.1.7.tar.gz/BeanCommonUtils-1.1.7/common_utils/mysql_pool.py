# -*- coding: UTF-8 -*-

import pymysql
from DBUtils.PooledDB import PooledDB


class MysqlPool(object):

    pool = None

    # 数据库连接池连接
    def init_mysql_pool(self, mysql_info):
        if self.pool is None:
            self.pool = PooledDB(creator=pymysql, mincached=10,
                                 host=mysql_info['host'], user=mysql_info['user'], passwd=mysql_info['passwd'],
                                 db=mysql_info['db'], port=mysql_info['port'],
                                 maxcached=20,  # 链接池中最多闲置的链接，0和None不限制
                                 blocking=True,
                                 ping=0,
                                 charset=mysql_info.get('charset', 'utf8'),
                                 maxconnections=6)

    def get_mysql_conn(self):
        mysql_conn = self.pool.connection()
        cur = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)
        return cur, mysql_conn

    # 插入\更新\删除sql
    @staticmethod
    def op_insert(sql, cur, mysql_conn, sql_type):
        mysql_conn.ping()
        try:
            insert_num = cur.execute(sql)
            mysql_conn.commit()
        except Exception as e:
            raise Exception("%s sql execute error, err_msg: %s" % (sql_type, e))

        return insert_num, True

    # 查询
    @staticmethod
    def op_select(sql, cur, mysql_conn):
        mysql_conn.ping()
        cur.execute(sql)
        try:
            select_res = cur.fetchall()
        except Exception as e:
            return e, False

        return select_res, True

    def sql_operate(self, sql, cur, mysql_conn, sql_type):
        sql_operate_list = ["insert", "update", "delete", "select"]
        if not isinstance(sql_type, str) and sql_type not in sql_operate_list:
            raise ValueError("input sql_type error, sql_type may be: %s" % sql_operate_list)

        if sql_type == "select":
            return self.op_select(sql, cur, mysql_conn)
        else:
            return self.op_insert(sql, cur, mysql_conn, sql_type)

    # 释放资源
    @staticmethod
    def dispose(mysql_conn):
        mysql_conn.close()
