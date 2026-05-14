from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.models.item import Item

items_bp = Blueprint('items', __name__)

@items_bp.route('/')
def index():
    """
    首頁：顯示所有商品，並提供關鍵字、分類、價格區間的搜尋與過濾功能 (F-04)。
    渲染模板：items/index.html
    """
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')

    items = Item.search_and_filter(
        query=query,
        category=category,
        min_price=min_price,
        max_price=max_price
    )

    return render_template('items/index.html', items=items)

@items_bp.route('/items/new', methods=['GET', 'POST'])
def new_item():
    """
    GET: 顯示發布商品表單 (items/new.html)
    POST: 接收商品資料並存入 DB
    """
    if 'user_id' not in session:
        flash('請先登入才能發布商品。', 'warning')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description'].strip()
        category = request.form['category']
        brand = request.form.get('brand', '').strip()
        condition = request.form['condition']
        price = request.form['price']
        ai_price_min = request.form.get('ai_price_min')
        ai_price_max = request.form.get('ai_price_max')

        if not title or not category or not condition or not price:
            flash('請填寫所有必填欄位。', 'danger')
            return render_template('items/new.html')

        try:
            price = int(price)
            ai_price_min = int(ai_price_min) if ai_price_min else None
            ai_price_max = int(ai_price_max) if ai_price_max else None
        except ValueError:
            flash('價格必須是數字。', 'danger')
            return render_template('items/new.html')

        item_id = Item.create(
            seller_id=session['user_id'],
            title=title,
            description=description,
            category=category,
            brand=brand,
            condition=condition,
            price=price,
            ai_price_min=ai_price_min,
            ai_price_max=ai_price_max
        )

        if item_id:
            flash('商品發布成功！', 'success')
            return redirect(url_for('items.item_detail', item_id=item_id))
        else:
            flash('發布失敗，請稍後再試。', 'danger')

    return render_template('items/new.html')

@items_bp.route('/items/<int:item_id>')
def item_detail(item_id):
    """顯示單一商品詳細資訊 (items/detail.html)"""
    item = Item.get_by_id(item_id)
    if not item:
        flash('找不到該商品。', 'danger')
        return redirect(url_for('items.index'))
    return render_template('items/detail.html', item=item)

@items_bp.route('/items/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    """刪除指定商品 (僅限發布者操作)"""
    if 'user_id' not in session:
        flash('請先登入。', 'warning')
        return redirect(url_for('auth.login'))

    item = Item.get_by_id(item_id)
    if not item:
        flash('找不到該商品。', 'danger')
        return redirect(url_for('items.index'))

    if item['seller_id'] != session['user_id']:
        flash('您沒有權限刪除此商品。', 'danger')
        return redirect(url_for('items.item_detail', item_id=item_id))

    if Item.delete(item_id, session['user_id']):
        flash('商品已成功刪除。', 'success')
    else:
        flash('刪除失敗。', 'danger')

    return redirect(url_for('items.index'))
