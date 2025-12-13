"""
Process Loan Classification API Module
Handles all CRUD operations for Process Loan Classification
"""
from flask import Blueprint, request, jsonify
from utils import (
    make_frappe_request, 
    url_encode_doctype, 
    url_encode_docname, 
    build_query_string,
    cancel_document
)

process_loan_classification_bp = Blueprint('process_loan_classification', __name__)
DOCTYPE = "Process Loan Classification"
ENCODED_DOCTYPE = url_encode_doctype(DOCTYPE)
BASE_ENDPOINT = f'/api/resource/{ENCODED_DOCTYPE}'


@process_loan_classification_bp.route('/api/process-loan-classification', methods=['POST'])
def create_process_loan_classification():
    """Create a new process loan classification"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    status_code, response_data = make_frappe_request('POST', BASE_ENDPOINT, data)
    return jsonify(response_data), status_code


@process_loan_classification_bp.route('/api/process-loan-classification', methods=['GET'])
def get_process_loan_classification():
    """Get list of process loan classification records"""
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


# More specific routes (with /cancel and /submit) must be defined before general <process_name> routes
@process_loan_classification_bp.route('/api/process-loan-classification/<process_name>/cancel', methods=['POST'])
def cancel_process_loan_classification(process_name: str):
    """
    Cancel a submitted process loan classification
    
    Note: Only submitted documents (docstatus=1) can be cancelled.
    Draft documents (docstatus=0) don't need cancellation.
    """
    # First, get the document to check its status
    encoded_name = url_encode_docname(process_name)
    get_endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    get_status, get_response = make_frappe_request('GET', get_endpoint)
    
    if get_status != 200:
        return jsonify(get_response), get_status
    
    # Check if document is submitted
    doc_data = get_response.get('data', {})
    docstatus = doc_data.get('docstatus', 0)
    
    if docstatus == 0:
        return jsonify({
            'message': 'Document is already in draft status',
            'docstatus': docstatus,
            'note': 'Only submitted documents (docstatus=1) can be cancelled. This document is already a draft.'
        }), 200
    
    if docstatus == 2:
        return jsonify({
            'message': 'Document is already cancelled',
            'docstatus': docstatus,
            'note': 'This document has already been cancelled.'
        }), 200
    
    # Document is submitted (docstatus=1), proceed with cancellation
    status_code, response_data = cancel_document(DOCTYPE, process_name)
    return jsonify(response_data), status_code


@process_loan_classification_bp.route('/api/process-loan-classification/<process_name>/submit', methods=['POST'])
def submit_process_loan_classification(process_name: str):
    """Submit a process loan classification"""
    from utils import submit_document
    status_code, response_data = submit_document(DOCTYPE, process_name)
    return jsonify(response_data), status_code


@process_loan_classification_bp.route('/api/process-loan-classification/<process_name>', methods=['GET'])
def get_one_process_loan_classification(process_name: str):
    """Get a specific process loan classification"""
    encoded_name = url_encode_docname(process_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('GET', endpoint)
    return jsonify(response_data), status_code


@process_loan_classification_bp.route('/api/process-loan-classification/<process_name>', methods=['PUT'])
def update_process_loan_classification(process_name: str):
    """
    Update a process loan classification
    
    Note: Cannot update certain fields (like posting_date) after submission.
    If document is submitted, you may need to cancel it first.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    # First, get the document to check its status
    encoded_name = url_encode_docname(process_name)
    get_endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    get_status, get_response = make_frappe_request('GET', get_endpoint)
    
    if get_status != 200:
        return jsonify(get_response), get_status
    
    # Check if document is submitted
    doc_data = get_response.get('data', {})
    docstatus = doc_data.get('docstatus', 0)
    
    if docstatus == 1:
        # Document is submitted - check if trying to update restricted fields
        restricted_fields = ['posting_date']
        updating_restricted = any(field in data for field in restricted_fields)
        
        if updating_restricted:
            return jsonify({
                'error': 'Cannot update restricted fields after submission',
                'message': 'Document is submitted. Cannot update posting_date after submission. You must cancel the document first.',
                'docstatus': docstatus,
                'restricted_fields': restricted_fields,
                'suggestion': 'Use DELETE endpoint which will automatically cancel and delete, or cancel first using: POST /api/process-loan-classification/<name>/cancel'
            }), 400
    
    # Proceed with update
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('PUT', endpoint, data)
    return jsonify(response_data), status_code


@process_loan_classification_bp.route('/api/process-loan-classification/<process_name>', methods=['DELETE'])
def delete_process_loan_classification(process_name: str):
    """
    Delete a process loan classification
    
    If document is submitted, it will be cancelled first, then deleted.
    """
    # First, get the document to check its status
    encoded_name = url_encode_docname(process_name)
    get_endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    get_status, get_response = make_frappe_request('GET', get_endpoint)
    
    if get_status != 200:
        return jsonify(get_response), get_status
    
    # Check if document is submitted
    doc_data = get_response.get('data', {})
    docstatus = doc_data.get('docstatus', 0)
    
    # If submitted, cancel it first
    if docstatus == 1:
        cancel_status, cancel_response = cancel_document(DOCTYPE, process_name)
        # Frappe method API returns success in 'message' field, errors in 'exception'
        if cancel_status not in [200, 202] or 'exception' in cancel_response:
            return jsonify({
                'error': 'Failed to cancel document',
                'message': 'Document is submitted and could not be cancelled',
                'cancel_response': cancel_response
            }), cancel_status if cancel_status != 200 else 400
        
        # Verify cancellation was successful by checking docstatus in response
        cancelled_doc = cancel_response.get('message', {})
        if isinstance(cancelled_doc, dict) and cancelled_doc.get('docstatus') != 2:
            return jsonify({
                'error': 'Cancellation may have failed',
                'message': 'Document cancellation did not complete successfully',
                'cancel_response': cancel_response
            }), 400
    
    # Now delete the document
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('DELETE', endpoint)
    return jsonify(response_data), status_code

