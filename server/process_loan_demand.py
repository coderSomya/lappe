"""
Process Loan Demand API Module
Handles all CRUD operations for Process Loan Demand
"""
from flask import Blueprint, request, jsonify
from utils import make_frappe_request, url_encode_doctype, url_encode_docname, build_query_string

process_loan_demand_bp = Blueprint('process_loan_demand', __name__)
DOCTYPE = "Process Loan Demand"
ENCODED_DOCTYPE = url_encode_doctype(DOCTYPE)
BASE_ENDPOINT = f'/api/resource/{ENCODED_DOCTYPE}'


@process_loan_demand_bp.route('/api/process-loan-demand', methods=['POST'])
def create_process_loan_demand():
    """Create a new process loan demand"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    status_code, response_data = make_frappe_request('POST', BASE_ENDPOINT, data)
    return jsonify(response_data), status_code


@process_loan_demand_bp.route('/api/process-loan-demand', methods=['GET'])
def get_process_loan_demand():
    """Get list of process loan demand records"""
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


@process_loan_demand_bp.route('/api/process-loan-demand/<process_name>', methods=['GET'])
def get_one_process_loan_demand(process_name: str):
    """Get a specific process loan demand"""
    encoded_name = url_encode_docname(process_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('GET', endpoint)
    return jsonify(response_data), status_code


@process_loan_demand_bp.route('/api/process-loan-demand/<process_name>', methods=['PUT'])
def update_process_loan_demand(process_name: str):
    """Update a process loan demand"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    encoded_name = url_encode_docname(process_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('PUT', endpoint, data)
    return jsonify(response_data), status_code


@process_loan_demand_bp.route('/api/process-loan-demand/<process_name>', methods=['DELETE'])
def delete_process_loan_demand(process_name: str):
    """Delete a process loan demand"""
    encoded_name = url_encode_docname(process_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('DELETE', endpoint)
    return jsonify(response_data), status_code

