"""
Companies API Module
Handles all CRUD operations for Companies
"""
from flask import Blueprint, request, jsonify
from utils import make_frappe_request, url_encode_doctype, url_encode_docname, build_query_string

companies_bp = Blueprint('companies', __name__)
DOCTYPE = "Company"
ENCODED_DOCTYPE = url_encode_doctype(DOCTYPE)
BASE_ENDPOINT = f'/api/resource/{ENCODED_DOCTYPE}'


@companies_bp.route('/api/companies', methods=['POST'])
def create_company():
    """
    Create a new company
    
    Request body:
    {
        "company_name": "Acme Corporation",
        "abbr": "ACME",
        "default_currency": "INR",
        "country": "India",
        "default_bank_account": "Bank Account - ACME",
        "default_cash_account": "Cash - ACME",
        "default_payable_account": "Creditors - ACME",
        "default_receivable_account": "Debtors - ACME",
        "default_expense_account": "Expenses - ACME",
        "default_income_account": "Income - ACME",
        "default_payable_party_type": "Supplier",
        "default_receivable_party_type": "Customer"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    # Validate required fields
    required_fields = ['company_name', 'abbr']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing_fields': missing_fields
        }), 400
    
    # Set defaults if not provided
    if 'default_currency' not in data:
        data['default_currency'] = 'INR'
    if 'country' not in data:
        data['country'] = 'India'
    
    # Important: Don't include account fields if they don't exist yet
    # ERPNext will try to validate these and may fail if accounts don't exist
    # Only include account fields if they are explicitly provided and exist
    account_fields = [
        'default_bank_account', 'default_cash_account', 'default_payable_account',
        'default_receivable_account', 'default_expense_account', 'default_income_account'
    ]
    
    # Remove account fields that are empty or None
    for field in account_fields:
        if field in data and (not data[field] or data[field] == ''):
            del data[field]
    
    # Use custom method that bypasses warehouse creation issue
    # This method uses ignore_chart_of_accounts flag to skip warehouse creation
    custom_endpoint = '/api/method/lending.api.company.create_company_without_warehouses'
    
    # Try custom method first (bypasses warehouse creation)
    status_code, response_data = make_frappe_request('POST', custom_endpoint, data)
    
    # Custom method returns data in 'message' field
    if status_code == 200 and 'message' in response_data:
        company_data = response_data.get('message', {})
        return jsonify({'data': company_data}), 200
    
    # If custom method failed, check if it's a method not found error
    # In that case, fall back to standard API (but it will likely fail with Warehouse error)
    if status_code == 404 or 'method' in str(response_data).lower():
        # Custom method not found - fall back to standard API
        status_code, response_data = make_frappe_request('POST', BASE_ENDPOINT, data)
    else:
        # Custom method returned an error - return it
        return jsonify(response_data), status_code
    
    # If we're here, we tried standard API - return its response
    
    # If there's an error about Warehouse, provide helpful message and solution
    if status_code != 200:
        error_msg = str(response_data.get('exception', ''))
        server_messages = response_data.get('_server_messages', [])
        
        if 'Warehouse' in error_msg or any('Warehouse' in str(msg) for msg in server_messages):
            return jsonify({
                'error': 'Company creation requires Warehouse doctype',
                'message': 'ERPNext automatically tries to create default warehouses when creating a company, but the Warehouse doctype is not installed in the database.',
                'solutions': [
                    {
                        'method': 'Run migrations',
                        'command': 'bench --site lending.localhost migrate',
                        'description': 'This will install all missing doctypes including Warehouse'
                    },
                    {
                        'method': 'Create via UI',
                        'url': 'http://lending.localhost:8000/desk/company/view/List',
                        'description': 'The UI may handle warehouse creation differently'
                    },
                    {
                        'method': 'Complete setup wizard',
                        'url': 'http://lending.localhost:8000/setup-wizard',
                        'description': 'Complete ERPNext setup to install all required doctypes'
                    }
                ],
                'working_operations': [
                    'GET /api/companies - List all companies',
                    'GET /api/companies/<name> - Get specific company',
                    'PUT /api/companies/<name> - Update company',
                    'DELETE /api/companies/<name> - Delete company'
                ],
                'frappe_error': response_data.get('exception', '')[:500] if response_data.get('exception') else None
            }), status_code
    
    return jsonify(response_data), status_code


@companies_bp.route('/api/companies', methods=['GET'])
def get_companies():
    """
    Get list of companies
    
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


@companies_bp.route('/api/companies/<company_name>', methods=['GET'])
def get_company(company_name: str):
    """
    Get a specific company by name
    """
    encoded_name = url_encode_docname(company_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('GET', endpoint)
    
    return jsonify(response_data), status_code


@companies_bp.route('/api/companies/<company_name>', methods=['PUT'])
def update_company(company_name: str):
    """
    Update a company
    
    Request body should contain the fields to update
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    encoded_name = url_encode_docname(company_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('PUT', endpoint, data)
    
    return jsonify(response_data), status_code


@companies_bp.route('/api/companies/<company_name>', methods=['DELETE'])
def delete_company(company_name: str):
    """
    Delete a company
    """
    encoded_name = url_encode_docname(company_name)
    endpoint = f'{BASE_ENDPOINT}/{encoded_name}'
    status_code, response_data = make_frappe_request('DELETE', endpoint)
    
    return jsonify(response_data), status_code

