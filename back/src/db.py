import pymysql

from DBUtils.PooledDB import PooledDB


class DbManager(object):
    
    def __init__(self, conn_args):
        cmds = ["set names utf8mb4;"]
        self._pool = PooledDB(pymysql, mincached=5, maxcached=20, setsession=cmds, **conn_args)
    
    def connection(self):
        return self._pool.connection()

    def execute_query(self, sql, as_dict=True):
        """
        查询语句
        :param sql: 
        :param as_dict: 
        :return: 
        """
        conn = None
        cur = None
        try:
            conn = self._pool.connection()
            cur = conn.cursor()
            cur.execute(sql)
            rst = cur.fetchall()
            if rst:
                if as_dict:
                    fields = [tup[0] for tup in cur._cursor.description]
                    return [dict(zip(fields, row)) for row in rst]
                return rst
            return rst

        except Exception as e:
            print('sql:[{}]meet error'.format(sql))
            print(e.args[-1])
            return ()
        finally:
            if conn:
                conn.close()
            if cur:
                cur.close()
                
    def execute_manay(self, sql, data):
        """
        执行多条语句
        :param sql:
        :param data:
        :return:
        """
        conn = None
        cur = None
        try:
            conn = self._pool.connection()
            cur = conn.cursor()
            cur.executemany(sql, data)
            conn.commit()
            return True
        except Exception as e:
            print('[{}]meet error'.format(sql))
            print(e.args[-1])
            conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
            if cur:
                cur.close()