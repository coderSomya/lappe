"""
Loan Disbursements API Module
Handles all CRUD operations for Loan Disbursements
"""
from flask import Blueprint, request, jsonify
from utils import make_frappe_request, url_encode_doctype, url_encode_docname, build_query_string

loan_disbursements_bp = Blueprint('loan_disbursements', __name__)
DOCTYPE = "Loan Disbursement"
ENCODED_DOCTYPE = url_encode_doctype(DOCTYPE)
BASE_ENDPOINT = f'/api/resource/{ENCODED_DOCTYPE}'


@loan_disbursements_bp.route('/api/loan-disbursements', methods=['POST'])
def create_loan_disbursement():
    """Create a new loan disbursement"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    status_code, response_data = make_frappe_request('POST', BASE_ENDPOINT, data)
    return jsonify(response_data), status_code


@loan_disbursements_bp.route('/api/loan-disbursements', methods=['GET'])
def get_loan_disbursements():
    """Get list of loan disbursements"""
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


@loan_disbursements_bp.route('/api/loan-disbursements/<disbursement_name>', methods=['GET'])
def get_loan_disbursement(disbursement_name: str):
    """Get a specific loan disbursement"""
    encoded_name = url_encode_docname(disbursement_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('GET', endpoint)
    return jsonify(response_data), status_code


@loan_disbursements_bp.route('/api/loan-disbursements/<disbursement_name>', methods=['PUT'])
def update_loan_disbursement(disbursement_name: str):
    """Update a loan disbursement"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    encoded_name = url_encode_docname(disbursement_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('PUT', endpoint, data)
    return jsonify(response_data), status_code


@loan_disbursements_bp.route('/api/loan-disbursements/<disbursement_name>', methods=['DELETE'])
def delete_loan_disbursement(disbursement_name: str):
    """Delete a loan disbursement"""
    encoded_name = url_encode_docname(disbursement_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('DELETE', endpoint)
    return jsonify(response_data), status_code

