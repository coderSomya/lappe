"""
Main API Gateway Server for Loan Management System
Acts as a proxy/gateway to Frappe backend
"""
from flask import Flask, jsonify

# Import all blueprints
from loan_categories import loan_categories_bp
from loan_products import loan_products_bp
from loan_applications import loan_applications_bp
from loans import loans_bp
from loan_restructures import loan_restructures_bp
from loan_disbursements import loan_disbursements_bp
from loan_security_deposits import loan_security_deposits_bp
from loan_repayment_schedules import loan_repayment_schedules_bp
from loan_interest_accruals import loan_interest_accruals_bp
from loan_demands import loan_demands_bp
from loan_repayments import loan_repayments_bp
from process_loan_security_shortfall import process_loan_security_shortfall_bp
from process_loan_interest_accrual import process_loan_interest_accrual_bp
from process_loan_demand import process_loan_demand_bp
from process_loan_classification import process_loan_classification_bp
from users import users_bp
from companies import companies_bp

app = Flask(__name__)

# Register all blueprints
app.register_blueprint(loan_categories_bp)
app.register_blueprint(loan_products_bp)
app.register_blueprint(loan_applications_bp)
app.register_blueprint(loans_bp)
app.register_blueprint(loan_restructures_bp)
app.register_blueprint(loan_disbursements_bp)
app.register_blueprint(loan_security_deposits_bp)
app.register_blueprint(loan_repayment_schedules_bp)
app.register_blueprint(loan_interest_accruals_bp)
app.register_blueprint(loan_demands_bp)
app.register_blueprint(loan_repayments_bp)
app.register_blueprint(process_loan_security_shortfall_bp)
app.register_blueprint(process_loan_interest_accrual_bp)
app.register_blueprint(process_loan_demand_bp)
app.register_blueprint(process_loan_classification_bp)
app.register_blueprint(users_bp)
app.register_blueprint(companies_bp)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Loan Management API Gateway',
        'modules': [
            'Loan Categories',
            'Loan Products',
            'Loan Applications',
            'Loans',
            'Loan Restructures',
            'Loan Disbursements',
            'Loan Security Deposits',
            'Loan Repayment Schedules',
            'Loan Interest Accruals',
            'Loan Demands',
            'Loan Repayments',
            'Process Loan Security Shortfall',
            'Process Loan Interest Accrual',
            'Process Loan Demand',
            'Process Loan Classification',
            'Users',
            'Companies'
        ]
    }), 200


if __name__ == '__main__':
    import os
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting Loan Management API Gateway on port {port}")
    print(f"📡 Registered {17} modules")
    print(f"✅ Server ready at http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
