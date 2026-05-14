from flask import Blueprint, request, jsonify
import random

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/estimate-price', methods=['POST'])
def estimate_price():
    """
    接收 JSON 格式的商品資訊 (category, brand, condition)，
    回傳 AI 估價結果區間 { "min_price": int, "max_price": int } (F-02)。
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    category = data.get('category', '')
    brand = data.get('brand', '')
    condition = data.get('condition', '')

    if not category or not condition:
        return jsonify({"error": "Category and condition are required"}), 400

    # Mock AI Pricing Logic
    base_prices = {
        'Books': 300,
        'Electronics': 3000,
        'Dorm Life': 500
    }
    
    multipliers = {
        'New': 0.9,
        'Like New': 0.75,
        'Good': 0.6,
        'Fair': 0.4
    }

    base = base_prices.get(category, 1000)
    mult = multipliers.get(condition, 0.5)
    
    # Adding some randomness based on brand presence
    brand_bonus = 1.2 if brand else 1.0

    estimated_value = int(base * mult * brand_bonus)
    
    # Create a range
    min_price = max(0, int(estimated_value * 0.85))
    max_price = int(estimated_value * 1.15)

    return jsonify({
        "min_price": min_price,
        "max_price": max_price
    }), 200
