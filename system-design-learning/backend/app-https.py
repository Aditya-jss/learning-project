from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

users_db = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]

# ==================== SAME ROUTES AS app.py ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """STEP 4: HTTPS/TLS Secure Health Check"""
    logger.info(f"Secure health check from {request.remote_addr}")
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "protocol": "HTTPS (Secure)",
        "security": "TLS/SSL enabled",
        "message": "Secure connection established"
    }), 200


@app.route('/api/protocol-info', methods=['GET'])
def protocol_info():
    """Shows HTTPS is being used"""
    protocol = 'HTTPS' if request.is_secure else 'HTTP'
    return jsonify({
        "status": "success",
        "current_protocol": protocol,
        "is_secure": request.is_secure,
        "scheme": request.scheme,
        "tls_enabled": True,
        "message": f"Connection is encrypted with TLS/SSL"
    }), 200


@app.route('/api/certificate-info', methods=['GET'])
def certificate_info():
    """
    STEP 4: Show certificate information
    Test: GET https://localhost:5443/api/certificate-info
    """
    return jsonify({
        "status": "success",
        "message": "Server is using TLS/SSL certificate",
        "certificate_info": {
            "type": "Self-signed certificate (for learning)",
            "location": "certificates/server.crt and certificates/server.key",
            "purpose": "Enables HTTPS encryption",
            "in_production": "Use certificates from trusted CA (Let's Encrypt, etc)"
        },
        "security_features": [
            "Data encrypted in transit",
            "Protected from man-in-the-middle attacks",
            "Verifies server authenticity"
        ]
    }), 200


@app.route('/api/users', methods=['GET'])
def get_users():
    """Secure GET users over HTTPS"""
    logger.info(f"Fetching users securely from {request.remote_addr}")
    return jsonify({
        "status": "success",
        "data": users_db,
        "count": len(users_db),
        "protocol": "HTTPS",
        "security": "Connection encrypted with TLS"
    }), 200


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get single user securely"""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if user:
        return jsonify({
            "status": "success",
            "data": user,
            "security": "HTTPS/TLS"
        }), 200
    return jsonify({
        "status": "error",
        "message": f"User {user_id} not found"
    }), 404


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create user with HTTPS encryption"""
    data = request.get_json()
    logger.info(f"Creating user securely: {data}")
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({
            "status": "error",
            "message": "Name and email required"
        }), 400
    
    new_user = {
        "id": max([u["id"] for u in users_db]) + 1,
        "name": data["name"],
        "email": data["email"]
    }
    users_db.append(new_user)
    
    return jsonify({
        "status": "success",
        "message": "User created securely",
        "data": new_user
    }), 201


@app.route('/api/secure-endpoint', methods=['POST'])
def secure_endpoint():
    """
    API key + HTTPS = Extra security
    Test: POST https://localhost:5443/api/secure-endpoint
    Headers: x-api-key: secret123
    """
    api_key = request.headers.get('x-api-key')
    
    if not api_key or api_key != 'secret123':
        return jsonify({
            "status": "error",
            "message": "Invalid API key"
        }), 401
    
    data = request.get_json()
    return jsonify({
        "status": "success",
        "message": "Secure request received",
        "data": data,
        "encryption": "TLS/SSL + API Key validation"
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Not found"}), 404


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("SECURE BACKEND API (HTTPS/TLS)")
    print("=" * 60)
    print("\nStep 4: Running with HTTPS/TLS/SSL")
    print("  Command: python app-https.py")
    print("  URL: https://localhost:5443")
    print("\nImportant:")
    print("  - You'll see SSL certificate warning (expected for self-signed)")
    print("  - In Postman: Disable 'SSL verification' in settings")
    print("  - In production: Use certificates from trusted CA")
    print("\nTest endpoints:")
    print("  GET https://localhost:5443/api/health")
    print("  GET https://localhost:5443/api/certificate-info")
    print("=" * 60 + "\n")
    
    # HTTPS with self-signed certificate
    app.run(
        host='0.0.0.0',
        port=5443,
        ssl_context=('certificates/server.crt', 'certificates/server.key'),
        debug=True
    )
