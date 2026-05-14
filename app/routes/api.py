from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/estimate-price', methods=['POST'])
def estimate_price():
    """
    接收 JSON 格式的商品資訊 (category, brand, condition)，
    回傳 AI 估價結果區間 { "min_price": int, "max_price": int } (F-02)。
    """
    pass
