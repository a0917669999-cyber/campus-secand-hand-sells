from flask import Blueprint, request, render_template, redirect, url_for, flash, session

items_bp = Blueprint('items', __name__)

@items_bp.route('/')
def index():
    """
    首頁：顯示所有商品，並提供關鍵字、分類、價格區間的搜尋與過濾功能 (F-04)。
    渲染模板：items/index.html
    """
    pass

@items_bp.route('/items/new', methods=['GET', 'POST'])
def new_item():
    """
    GET: 顯示發布商品表單 (items/new.html)
    POST: 接收商品資料並存入 DB
    """
    pass

@items_bp.route('/items/<int:item_id>')
def item_detail(item_id):
    """顯示單一商品詳細資訊 (items/detail.html)"""
    pass

@items_bp.route('/items/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    """刪除指定商品 (僅限發布者操作)"""
    pass
