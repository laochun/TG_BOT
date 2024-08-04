from mailbox import Message

from mysql.connector import connect,Error
from mysql.connector.pooling import MySQLConnectionPool
from config import *
from public.logger import LoggerConfig

logs=LoggerConfig('data', 'log/data.log').get_logger()

class Card:
    def __init__(self):
        self.pool = None
        self.connect = None
        self.create_connection_pool()
    def create_connection_pool(self):
        try:
            # 创建数据库连接池
            self.pool = MySQLConnectionPool(**mysql_config)
            logs.critical("数据库链接成功：")

        except Error as err:
            logs.error(f"create_connection_pool-Failed to create connection pool: {err}")
    def get_connection(self):
        try:
            # 从连接池获取数据库连接
            connection = self.pool.get_connection()
            if connection.is_connected():
                self.connect = connection
                return True
            else:
                return False
        except Error as err:
            logs.error(f"Failed to get database connection: {err}")
            return False
    def close_connection(self):
        if self.connect:
            self.connect.close()
    def execute_query(self, query, data=None):
        try:
            self.get_connection()
            with self.connect.cursor() as cursor:
                cursor.execute(query, data)
                results = cursor.fetchall()
                logs.critical(results)
                return results
        except Error as err:
            print(f"execute_query-Failed to execute query: {err}")
            self.connect.rollback()
            return []
        finally:
            self.close_connection()
    def execute_update(self, query, data=None):
        try:
            self.get_connection()
            with self.connect.cursor() as cursor:
                cursor.execute(query, data)
                self.connect.commit()
            return True
        except Error as err:
            print(f"execute_update-Failed to execute update: {err}")
            self.connect.rollback()
            return False
        finally:
            self.close_connection()
    def select(self, query, data=None):
        return self.execute_query(query, data)
    def update(self, query, data=None):
        return self.execute_update(query, data)
    def insert(self, query, data=None):
        return self.execute_update(query, data)
    def delete(self, query, data=None):
        return self.execute_update(query, data)
db = Card()

class ChatUser:
    '''用户表操作类'''
    # 用户操作
    def __init__(self, Msg: Message = None):
        self.msg = Msg
    def get(self,from_user):
        self.msg = from_user
        '''查询用户'''
        user= db.select("SELECT * FROM chat_user WHERE chat_id=%s",(from_user.id,))
        if user:
            print( f"数据查询成功")
            return user
        return False
    def post(self,from_user):
        # msg =self.msg
        full_name = f"{from_user.first_name or ''}{from_user.last_name or ''}"
        aad = "INSERT INTO chat_user (chat_id,username,full_name) " \
              "VALUES(%s,%s,%s)"
        data = (from_user.id, from_user.username or '无', full_name)
        if db.insert(aad, data):
            print( f"数据写入成功")
            return self.get(from_user=from_user)
        return []
    def get_or_create(self,from_user):
        user = self.get(from_user=from_user)
        if user:
            return user
        else:
            return self.post(from_user=from_user)
class ChatMessage:
    '''消息信息表'''
    # 查询操作
    def __init__(self, Msg: Message = None):
        self.msg = Msg
    def get(self,message_id):
        # self.msg = from_user
        '''查询用户'''
        message_id= db.select("SELECT * FROM chat_message WHERE message_id=%s",(message_id,))
        if message_id:
            return message_id
        return False
    def post(self,message):
        # msg =self.msg
        print(message)
        message_id, message_type,file_name = message['id'], message['type'] or '无', message['file']
        print(message_id, message_type,file_name)
        aad = "INSERT INTO chat_message (message_id,message_type,file_name) " \
              "VALUES(%s,%s,%s)"
        data = (message_id, message_type or '无', file_name)
        if db.insert(aad, data):
            return self.get(message_id)
        return []
    def get_or_create(self,from_user):
        user = self.get(from_user=from_user)
        if user:
            return user
        else:
            return self.post(from_user=from_user)





