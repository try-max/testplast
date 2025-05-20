import os
from dotenv import load_dotenv
load_dotenv()


def getMysqlSetting():
    # 数据库相关配置
    # 用户名

    mysqldb_config = {
        'host': os.getenv('MYSQL_HOSTNAME'),  # 地址
        'port': int(os.getenv('MYSQL_PORT')),  # 端口
        # 数据库
        'database': os.getenv('MYSQL_DATABASE_NAME'),
        # 用户名和密码
        'user': os.getenv('MYSQL_USER_NAME'),
        'password': os.getenv('MYSQL_USER_PASSWORD'),
        # 数据库编码
        'charset': 'utf8'
    }

    return mysqldb_config

if __name__ == '__main__':
    mysqldb_config = getMysqlSetting()
    print(mysqldb_config)




