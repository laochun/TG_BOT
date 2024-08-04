import platform
mysql_config={
    'user': 'root',
    'password': '123456',
    'host': 'localhost',
    'port': 3306,
    'database': 'tg_bot',
    'pool_size': 20,

}
last_message_time = {}
MESSAGE_INTERVAL = 0.5  # 设置消息间隔为3秒
# def check_windows():
#     system = platform.system()
#     if system == 'Windows':
#         host = 'localhost'
#         user = 'root'
#         password = '123456'
#         database = 'tg_bot'
#         return host, user, password, database
#     else:
#         host = 'localhost'
#         user = 'root'
#         password = '123456'
#         database = 'tg_bot'
#         return host, user, password, database
# CREATE TABLE chat_message (
#     message_id INT PRIMARY KEY,
#     message_type VARCHAR(50),
#     file_name VARCHAR(255)
# );


# CREATE TABLE chat_user (
#     chat_id INT UNIQUE,
#     username VARCHAR(50),
#     full_name VARCHAR(100)
# );

