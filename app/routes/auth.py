from flask import Blueprint, request, render_template, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: 顯示註冊表單 (auth/register.html)
    POST: 接收 email, password, confirm_password，建立新帳號
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 顯示登入表單 (auth/login.html)
    POST: 驗證帳號密碼，登入並重導向至首頁
    """
    pass

@auth_bp.route('/logout')
def logout():
    """清除 session 並重導向至首頁"""
    pass
