
from flask import Blueprint, request, jsonify
from utils import make_frappe_request

proxy_bp = Blueprint('proxy', __name__)

@proxy_bp.route('/api/proxy/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_request(subpath):
    """Generic proxy to Frappe"""
    method = request.method
    endpoint = f'/api/{subpath}'
    
    # Forward query params
    if request.query_string:
        endpoint += f'?{request.query_string.decode("utf-8")}'
        
    data = request.get_json() if method in ['POST', 'PUT'] else None
    
    status_code, response_data = make_frappe_request(method, endpoint, data)
    return jsonify(response_data), status_code
