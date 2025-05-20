import pymysql

from app.dbutil.DbConnectionPool import dbconnectionpool

# create_conn = dbconnectionpool.create_conn()
# close_conn = dbconnectionpool.close_conn()


# 查询一条
# def select_one(sql, args):
#     conn, cur = create_conn()
#     cur.execute(sql, args)
#     result = cur.fetchone()
#     close_conn(conn, cur)
#     return result
def select_one(sql, args=()):
    conn, cur = None, None
    try:
        conn, cur = dbconnectionpool.create_conn()
        cur.execute(sql, args)
        return cur.fetchone()
    except pymysql.MySQLError as e:
        print(f"SQL Error: {e}")
        raise
    finally:
        if conn or cur:
            dbconnectionpool.close_conn(conn, cur)  # 显式传递当前连接


# 根据条件查询所有
# def select_all(sql, args=()):
#     conn, cur = create_conn()
#     cur.execute("")
#     result = cur.fetchall()
#     close_conn(conn, cur)
#     return result

def select_all(sql, args=()):
    conn, cur = None, None
    try:
        conn, cur = dbconnectionpool.create_conn()
        cur.execute(sql, args)
        return cur.fetchall()
    except pymysql.MySQLError as e:
        print(f"SQL Error: {e}")
        raise
    finally:
        if conn or cur:
            dbconnectionpool.close_conn(conn, cur)  # 显式传递当前连接


# 新增一条记录
# def insert_one(sql, args):
#     conn, cur = create_conn()
#     result = cur.execute(sql, args)
#     conn.commit()
#     close_conn(conn, cur)
#     return result


def insert_one(sql, args=()):
    conn, cur = None, None
    try:
        conn, cur = dbconnectionpool.create_conn()
        cur.execute(sql, args)
        return conn.commit()
    except pymysql.MySQLError as e:
        print(f"SQL Error: {e}")
        raise
    finally:
        if conn or cur:
            dbconnectionpool.close_conn(conn, cur)  # 显式传递当前连接


# 新增一条纪录 并返回主键id
# sql = "INSERT INTO users (username) VALUES (%s)"
# args = ("Alice",)
# insert_one_pk(sql, args)
def insert_one_pk(sql, args=()):
    conn, cur = None, None
    try:
        conn, cur = dbconnectionpool.create_conn()
        cur.execute(sql, args)
        conn.commit()
        return cur.lastrowid
    except pymysql.MySQLError as e:
        print(f"SQL Error: {e}")
        raise
    finally:
        if conn or cur:
            dbconnectionpool.close_conn(conn, cur)  # 显式传递当前连接


# 删除一条记录

def delete_one(sql, args=()):
    conn, cur = None, None
    try:
        conn, cur = dbconnectionpool.create_conn()
        cur.execute(sql, args)
        return conn.commit()
    except pymysql.MySQLError as e:
        print(f"SQL Error: {e}")
        raise
    finally:
        if conn or cur:
            dbconnectionpool.close_conn(conn, cur)  # 显式传递当前连接


# 更新一条记录
# sql = "UPDATE users SET status = %s WHERE id = %s"
# args_list = [("active", 1), ("inactive", 2)]
# update_one(sql,args_list)
def update_one(sql, args=()):
    conn, cur = None, None
    try:
        conn, cur = dbconnectionpool.create_conn()
        cur.execute(sql, args)
        return conn.commit()
    except pymysql.MySQLError as e:
        print(f"SQL Error: {e}")
        raise
    finally:
        if conn or cur:
            dbconnectionpool.close_conn(conn, cur)  # 显式传递当前连接

