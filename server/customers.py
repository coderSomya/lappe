"""
Customers API Module
Handles all CRUD operations for Customers (Loan Applicants)
In Frappe Lending, borrowers are represented as Customers
"""
from flask import Blueprint, request, jsonify
from utils import make_frappe_request, url_encode_doctype, url_encode_docname, build_query_string

customers_bp = Blueprint('customers', __name__)
DOCTYPE = "Customer"
ENCODED_DOCTYPE = url_encode_doctype(DOCTYPE)
BASE_ENDPOINT = f'/api/resource/{ENCODED_DOCTYPE}'


@customers_bp.route('/api/customers', methods=['POST'])
def create_customer():
    """
    Create a new customer (loan applicant)
    
    Request body:
    {
        "customer_name": "John Doe",
        "customer_type": "Individual",
        "customer_group": "Individual",
        "territory": "India",
        "custom_employee_id": "EMP001",
        "custom_company_id": "COMP001",
        "custom_phone_number": "9876543210",
        "custom_email": "john@example.com",
        "custom_aadhar_number": "123456789012",
        "custom_pan_number": "ABCDE1234F"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    # Validate required fields
    required_fields = ['customer_name']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing_fields': missing_fields
        }), 400
    
    # Set defaults if not provided
    if 'customer_type' not in data:
        data['customer_type'] = 'Individual'
    if 'customer_group' not in data:
        data['customer_group'] = 'Individual'
    if 'territory' not in data:
        data['territory'] = 'India'
    
    status_code, response_data = make_frappe_request('POST', BASE_ENDPOINT, data)
    return jsonify(response_data), status_code


@customers_bp.route('/api/customers', methods=['GET'])
def get_customers():
    """
    Get list of customers
    
    Query parameters:
    - fields: Comma-separated list of fields to retrieve (optional)
    - filters: JSON string of filters (optional)
    - limit_start: Starting index for pagination (optional)
    - limit_page_length: Number of records per page (optional)
    """
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


@customers_bp.route('/api/customers/<customer_name>', methods=['GET'])
def get_customer(customer_name: str):
    """Get a specific customer by name"""
    encoded_name = url_encode_docname(customer_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('GET', endpoint)
    return jsonify(response_data), status_code


@customers_bp.route('/api/customers/<customer_name>', methods=['PUT'])
def update_customer(customer_name: str):
    """Update a customer"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    encoded_name = url_encode_docname(customer_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('PUT', endpoint, data)
    return jsonify(response_data), status_code


@customers_bp.route('/api/customers/<customer_name>', methods=['DELETE'])
def delete_customer(customer_name: str):
    """Delete a customer"""
    encoded_name = url_encode_docname(customer_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('DELETE', endpoint)
    return jsonify(response_data), status_code


@customers_bp.route('/api/customers/by-employee/<employee_id>', methods=['GET'])
def get_customer_by_employee_id(employee_id: str):
    """
    Get customer by custom employee ID
    This is useful to find the Frappe customer linked to your internal employee
    """
    import json
    filters = json.dumps([["Customer", "custom_employee_id", "=", employee_id]])
    params = {'filters': filters}
    endpoint = BASE_ENDPOINT + build_query_string(params)
    status_code, response_data = make_frappe_request('GET', endpoint)
    return jsonify(response_data), status_code
