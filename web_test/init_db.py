import sqlite3

def init_database():
    # 连接到数据库（如果文件不存在，会自动在当前目录下创建）
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # 创建用户表
    # id: 自增主键
    # username: 唯一（UNIQUE），不允许重复注册
    # password_hash: 存放加密后的密码密文
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # 提交事务并关闭连接
    conn.commit()
    conn.close()
    print("🎉 数据库初始化成功！'database.db' 文件已生成，'users' 表已就绪。")

if __name__ == '__main__':
    init_database()