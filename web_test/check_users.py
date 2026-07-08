import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
# 查询users表所有账号数据
cursor.execute("SELECT id, username, password_hash FROM users;")
user_list = cursor.fetchall()

print("=== 当前所有注册账号 ===")
if not user_list:
    print("暂无任何注册账号")
else:
    for uid, name, pwd_hash in user_list:
        print(f"用户ID：{uid} | 用户名：{name} | 密码哈希：{pwd_hash}")

conn.close()