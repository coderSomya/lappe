"""
Loan Categories API Module
Handles all CRUD operations for Loan Categories
"""
from flask import Blueprint, request, jsonify
from utils import make_frappe_request, url_encode_doctype, url_encode_docname, build_query_string

loan_categories_bp = Blueprint('loan_categories', __name__)
DOCTYPE = "Loan Category"
ENCODED_DOCTYPE = url_encode_doctype(DOCTYPE)
BASE_ENDPOINT = f'/api/resource/{ENCODED_DOCTYPE}'


@loan_categories_bp.route('/api/loan-categories', methods=['POST'])
def create_loan_category():
    """
    Create a new loan category
    
    Request body:
    {
        "loan_category_code": "PL-FINAL-01",
        "loan_category_name": "Personal Loan Final",
        "disabled": 0
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    # Validate required fields
    required_fields = ['loan_category_code', 'loan_category_name']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing_fields': missing_fields
        }), 400
    
    # Set default for disabled if not provided
    if 'disabled' not in data:
        data['disabled'] = 0
    
    # Make request to Frappe
    status_code, response_data = make_frappe_request('POST', BASE_ENDPOINT, data)
    
    return jsonify(response_data), status_code


@loan_categories_bp.route('/api/loan-categories', methods=['GET'])
def get_loan_categories():
    """
    Get list of loan categories
    
    Query parameters:
    - fields: Comma-separated list of fields to retrieve (optional)
    - filters: JSON string of filters (optional)
    - limit_start: Starting index for pagination (optional)
    - limit_page_length: Number of records per page (optional)
    """
    # Build query parameters
    params = {}
    if request.args.get('fields'):
        params['fields'] = request.args.get('fields')
    if request.args.get('filters'):
        params['filters'] = request.args.get('filters')
    if request.args.get('limit_start'):
        params['limit_start'] = request.args.get('limit_start')
    if request.args.get('limit_page_length'):
        params['limit_page_length'] = request.args.get('limit_page_length')
    
    # Build endpoint with query string
    endpoint = BASE_ENDPOINT + build_query_string(params)
    status_code, response_data = make_frappe_request('GET', endpoint)
    
    return jsonify(response_data), status_code


@loan_categories_bp.route('/api/loan-categories/<category_name>', methods=['GET'])
def get_loan_category(category_name: str):
    """
    Get a specific loan category by name/code
    """
    encoded_name = url_encode_docname(category_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('GET', endpoint)
    
    return jsonify(response_data), status_code


@loan_categories_bp.route('/api/loan-categories/<category_name>', methods=['PUT'])
def update_loan_category(category_name: str):
    """
    Update a loan category
    
    Request body should contain the fields to update
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    encoded_name = url_encode_docname(category_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('PUT', endpoint, data)
    
    return jsonify(response_data), status_code


@loan_categories_bp.route('/api/loan-categories/<category_name>', methods=['DELETE'])
def delete_loan_category(category_name: str):
    """
    Delete a loan category
    """
    encoded_name = url_encode_docname(category_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('DELETE', endpoint)
    
    return jsonify(response_data), status_code
