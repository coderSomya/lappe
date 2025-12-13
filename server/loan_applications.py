"""
Loan Applications API Module
Handles all CRUD operations for Loan Applications
"""
from flask import Blueprint, request, jsonify
from utils import make_frappe_request, url_encode_doctype, url_encode_docname, build_query_string

loan_applications_bp = Blueprint('loan_applications', __name__)
DOCTYPE = "Loan Application"
ENCODED_DOCTYPE = url_encode_doctype(DOCTYPE)
BASE_ENDPOINT = f'/api/resource/{ENCODED_DOCTYPE}'


@loan_applications_bp.route('/api/loan-applications', methods=['POST'])
def create_loan_application():
    """Create a new loan application"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    status_code, response_data = make_frappe_request('POST', BASE_ENDPOINT, data)
    return jsonify(response_data), status_code


@loan_applications_bp.route('/api/loan-applications', methods=['GET'])
def get_loan_applications():
    """Get list of loan applications"""
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


@loan_applications_bp.route('/api/loan-applications/<app_name>', methods=['GET'])
def get_loan_application(app_name: str):
    """Get a specific loan application"""
    encoded_name = url_encode_docname(app_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('GET', endpoint)
    return jsonify(response_data), status_code


@loan_applications_bp.route('/api/loan-applications/<app_name>', methods=['PUT'])
def update_loan_application(app_name: str):
    """Update a loan application"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    encoded_name = url_encode_docname(app_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('PUT', endpoint, data)
    return jsonify(response_data), status_code


@loan_applications_bp.route('/api/loan-applications/<app_name>', methods=['DELETE'])
def delete_loan_application(app_name: str):
    """Delete a loan application"""
    encoded_name = url_encode_docname(app_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('DELETE', endpoint)
    return jsonify(response_data), status_code

