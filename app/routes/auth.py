from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.models.user import User
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: 顯示註冊表單 (auth/register.html)
    POST: 接收 email, password, confirm_password，建立新帳號
    """
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not email or not password:
            flash('信箱和密碼皆為必填。', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('兩次輸入的密碼不一致。', 'danger')
            return render_template('auth/register.html')

        user_id = User.create(email, password)
        if user_id is None:
            flash('該信箱已被註冊或發生錯誤。', 'danger')
            return render_template('auth/register.html')
        
        flash('註冊成功！請登入。', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 顯示登入表單 (auth/login.html)
    POST: 驗證帳號密碼，登入並重導向至首頁
    """
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password']

        user = User.get_by_email(email)

        if user is None or not check_password_hash(user['password_hash'], password):
            flash('信箱或密碼錯誤。', 'danger')
            return render_template('auth/login.html')
        
        # 登入成功，設定 session
        session.clear()
        session['user_id'] = user['id']
        session['user_email'] = user['email']
        
        flash('登入成功！', 'success')
        return redirect(url_for('items.index'))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """清除 session 並重導向至首頁"""
    session.clear()
    flash('已登出。', 'info')
    return redirect(url_for('items.index'))
