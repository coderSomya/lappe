"""
Accounts API Module
Handles all CRUD operations for Accounts (Chart of Accounts)
"""
from flask import Blueprint, request, jsonify
from utils import make_frappe_request, url_encode_doctype, url_encode_docname, build_query_string

accounts_bp = Blueprint('accounts', __name__)
DOCTYPE = "Account"
ENCODED_DOCTYPE = url_encode_doctype(DOCTYPE)
BASE_ENDPOINT = f'/api/resource/{ENCODED_DOCTYPE}'


@accounts_bp.route('/api/accounts', methods=['POST'])
def create_account():
    """Create a new account"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    status_code, response_data = make_frappe_request('POST', BASE_ENDPOINT, data)
    return jsonify(response_data), status_code


@accounts_bp.route('/api/accounts', methods=['GET'])
def get_accounts():
    """Get list of accounts"""
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


@accounts_bp.route('/api/accounts/<account_name>', methods=['GET'])
def get_account(account_name: str):
    """Get a specific account"""
    encoded_name = url_encode_docname(account_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('GET', endpoint)
    return jsonify(response_data), status_code


@accounts_bp.route('/api/accounts/<account_name>', methods=['PUT'])
def update_account(account_name: str):
    """Update an account"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    encoded_name = url_encode_docname(account_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('PUT', endpoint, data)
    return jsonify(response_data), status_code


@accounts_bp.route('/api/accounts/<account_name>', methods=['DELETE'])
def delete_account(account_name: str):
    """Delete an account"""
    encoded_name = url_encode_docname(account_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('DELETE', endpoint)
    return jsonify(response_data), status_code
