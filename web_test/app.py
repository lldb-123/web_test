import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
# 引入 Flask 自带的安全加密工具，生成和校验哈希密码
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'my_super_secret_key_2026'

# 定义一个获取数据库连接的辅助函数
def get_db_connection():
    conn = sqlite3.connect('database.db')
    # 让查询结果可以通过列名来访问（比如 user['username']），而不是只能用元组下标
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# 1. 页面路由
# ==========================================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login.html')
def login_page():
    return render_template('login.html')

@app.route('/register.html')
def register_page():
    return render_template('register.html')

@app.route('/dashboard.html')
def dashboard_page():
    return render_template('dashboard.html')

# ==========================================
# 2. 核心后端接口 (API)
# ==========================================

# 注册接口
@app.route('/api/register', methods=['POST'])
def api_register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # 1. 安全加固：将明文密码转化为哈希密文
    hashed_password = generate_password_hash(password)
    
    conn = get_db_connection()
    try:
        # 2. 尝试向数据库插入新用户
        conn.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, hashed_password)
        )
        conn.commit()
        flash("注册成功！请登录。", "success")
        return redirect(url_for('login_page'))
    except sqlite3.IntegrityError:
        # 如果违反了 UNIQUE 约束（用户名已存在），会抛出此异常
        flash("该用户名已被注册，请换一个名字。", "error")
        return "该用户名已被注册，请返回重试。"
    finally:
        conn.close()

# 登录接口
@app.route('/api/login', methods=['POST'])
def api_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = get_db_connection()
    # 1. 根据用户名查找用户记录
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?', 
        (username,)
    ).fetchone()
    conn.close()
    
    # 2. 验证用户是否存在，且哈希密码是否匹配
    if user and check_password_hash(user['password_hash'], password):
        print(f"✅ 登录成功：欢迎回来，{username}！")
        return redirect(url_for('dashboard_page'))
    else:
        flash("用户名或密码错误，请检查后重试！", "error")
        return redirect(url_for('login_page'))

# 退出登录接口
@app.route('/api/logout')
def api_logout():
    print("✅ 用户已退出登录")
    return redirect(url_for('home'))

if __name__ == '__main__':
    # host='0.0.0.0' 的意思是告诉服务器：不要只监听内部回环地址，
    # 请监听本台电脑上所有的网络接口（向整个局域网公开）
    app.run(host='0.0.0.0', debug=True, port=5000)