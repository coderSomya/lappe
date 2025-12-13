"""
Shared utility functions for all API modules
"""
import requests
import os
from urllib.parse import quote, urlencode
from typing import Dict, Optional, Tuple

# Frappe Configuration
FRAPPE_BASE_URL = os.getenv('FRAPPE_BASE_URL', 'http://127.0.0.1:8000')
FRAPPE_SITE_NAME = os.getenv('FRAPPE_SITE_NAME', 'lending.localhost')
FRAPPE_API_KEY = os.getenv('FRAPPE_API_KEY', '64726967de821d4')
FRAPPE_API_SECRET = os.getenv('FRAPPE_API_SECRET', '18fe12924de8f23')


def get_frappe_headers() -> Dict[str, str]:
    """
    Generate headers for Frappe API requests
    Includes authentication token and site name
    """
    return {
        'Authorization': f'token {FRAPPE_API_KEY}:{FRAPPE_API_SECRET}',
        'Content-Type': 'application/json',
        'Host': FRAPPE_SITE_NAME
    }


def make_frappe_request(method: str, endpoint: str, data: Optional[Dict] = None) -> Tuple[int, Dict]:
    """
    Make a request to Frappe API
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path
        data: Request body data (optional)
    
    Returns:
        tuple: (status_code, response_data)
    """
    url = f"{FRAPPE_BASE_URL}{endpoint}"
    headers = get_frappe_headers()
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, json=data, timeout=30)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=30)
        elif method.upper() == 'PUT':
            response = requests.put(url, headers=headers, json=data, timeout=30)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=30)
        else:
            return 405, {'error': 'Method not allowed'}
        
        # Try to parse JSON response
        try:
            response_data = response.json()
        except ValueError:
            response_data = {'message': response.text, 'status_code': response.status_code}
        
        return response.status_code, response_data
    
    except requests.exceptions.ConnectionError:
        return 503, {'error': 'Cannot connect to Frappe server. Make sure it is running.'}
    except requests.exceptions.Timeout:
        return 504, {'error': 'Request timeout. Frappe server took too long to respond.'}
    except requests.exceptions.RequestException as e:
        return 500, {'error': f'Request failed: {str(e)}'}


def url_encode_doctype(doctype: str) -> str:
    """
    URL encode doctype name (handles spaces)
    Example: "Loan Category" -> "Loan%20Category"
    """
    return doctype.replace(' ', '%20')


def url_encode_docname(docname: str) -> str:
    """
    URL encode document name to handle special characters
    Example: "DOC-001" -> "DOC-001" (no change)
    Example: "DOC 001" -> "DOC%20001"
    """
    return quote(docname, safe='')


def build_query_string(params: Dict) -> str:
    """
    Build properly URL-encoded query string from parameters
    """
    if not params:
        return ''
    return '?' + urlencode(params)


def cancel_document(doctype: str, docname: str) -> Tuple[int, Dict]:
    """
    Cancel a submitted Frappe document
    Uses Frappe's method API: /api/method/frappe.client.cancel
    """
    endpoint = '/api/method/frappe.client.cancel'
    
    # Cancel requires doctype and name in the data
    data = {
        'doctype': doctype,
        'name': docname
    }
    
    return make_frappe_request('POST', endpoint, data)


def submit_document(doctype: str, docname: str) -> Tuple[int, Dict]:
    """
    Submit a Frappe document
    Uses Frappe's method API endpoint: /api/method/frappe.client.submit
    """
    endpoint = '/api/method/frappe.client.submit'
    
    # First get the document
    encoded_doctype = url_encode_doctype(doctype)
    encoded_name = url_encode_docname(docname)
    get_endpoint = f'/api/resource/{encoded_doctype}/{encoded_name}'
    get_status, get_response = make_frappe_request('GET', get_endpoint)
    
    if get_status != 200:
        return get_status, get_response
    
    # Submit requires the full document
    doc_data = get_response.get('data', {})
    data = {'doc': doc_data}
    
    return make_frappe_request('POST', endpoint, data)

