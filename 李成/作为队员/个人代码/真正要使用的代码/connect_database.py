import pymysql

class Mysql:
    def __init__(self):
        self.content = pymysql.Connect(
            host='pc-bp18rn0tqu85a1600-public.rwlb.rds.aliyuncs.com',  # mysql的主机ip
            port=3306,  # 端口
            user='lab_2124374516',  # 用户名
            passwd='4302921e96cf_#@Aa',  # 数据库密码
            db='codechecker',  # 数据库名
            charset='utf8',  # 字符集
        )
        self.cursor = self.content.cursor()

    def query(self,sql):
        self.cursor.execute(sql)
        # for row in self.cursor.fetchall():
            # print(row)
        # print(f"一共查找到：{self.cursor.rowcount}")
        return  self.cursor.fetchall()

    def delete_db(self,sql_delete):
        '''删除操作'''
        # 打开数据库连接

        # 使用cursor()方法获取操作游标
        cur = self.cursor()

        try:
            cur.execute(sql_delete)  # 执行
            # 提交
            self.content.commit()
        except Exception as e:
            print("操作异常：%s" % str(e))
            # 错误回滚
            self.content.rollback()
        finally:
            self.content.close()

    def insert_db(self,sql_insert):
        '''插入操作'''
        try:
            self.cursor.execute(sql_insert)
            # 提交
            self.content.commit()
        except Exception as e:
            print("错误信息：%s" % str(e))
            # 错误回滚
            self.content.rollback()

    def update_db(self,sql_update):

        try:
            self.cursor.execute(sql_update)
            # 提交
            self.content.commit()
        except Exception as e:
            print("错误信息：%s" % str(e))
            # 错误回滚
            self.content.rollback()


    def end(self):
        self.cursor.close()
        self.content.close()


if __name__ == '__main__':
    mysql = Mysql()
    mysql.insert_db("insert into students values (10,\"licheng\",1,2)")
    mysql.end()
