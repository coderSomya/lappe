"""
Loan Products API Module
Handles all CRUD operations for Loan Products
"""
from flask import Blueprint, request, jsonify
from utils import make_frappe_request, url_encode_doctype, url_encode_docname, build_query_string

loan_products_bp = Blueprint('loan_products', __name__)
DOCTYPE = "Loan Product"
ENCODED_DOCTYPE = url_encode_doctype(DOCTYPE)
BASE_ENDPOINT = f'/api/resource/{ENCODED_DOCTYPE}'


@loan_products_bp.route('/api/loan-products', methods=['POST'])
def create_loan_product():
    """Create a new loan product"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    status_code, response_data = make_frappe_request('POST', BASE_ENDPOINT, data)
    return jsonify(response_data), status_code


@loan_products_bp.route('/api/loan-products', methods=['GET'])
def get_loan_products():
    """Get list of loan products"""
    params = {}
    if request.args.get('fields'):
        params['fields'] = request.args.get('fields')
    if request.args.get('filters'):
        params['filters'] = request.args.get('filters')
    if request.args.get('limit_start'):
        params['limit_start'] = request.args.get('limit_start')
    if request.args.get('limit_page_length'):
        params['limit_page_length'] = request.args.get('limit_page_length')
    
    endpoint = BASE_ENDPOINT + build_query_string(params)
    status_code, response_data = make_frappe_request('GET', endpoint)
    return jsonify(response_data), status_code


@loan_products_bp.route('/api/loan-products/<product_name>', methods=['GET'])
def get_loan_product(product_name: str):
    """Get a specific loan product"""
    encoded_name = url_encode_docname(product_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('GET', endpoint)
    return jsonify(response_data), status_code


@loan_products_bp.route('/api/loan-products/<product_name>', methods=['PUT'])
def update_loan_product(product_name: str):
    """Update a loan product"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    encoded_name = url_encode_docname(product_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('PUT', endpoint, data)
    return jsonify(response_data), status_code


@loan_products_bp.route('/api/loan-products/<product_name>', methods=['DELETE'])
def delete_loan_product(product_name: str):
    """Delete a loan product"""
    encoded_name = url_encode_docname(product_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('DELETE', endpoint)
    return jsonify(response_data), status_code

