from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory database (simple store)
users_db = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]

# ==================== STEP 1: BASIC HTTP ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    STEP 1: Basic HTTP GET request
    Shows how a simple GET request works
    Test in Postman: GET http://localhost:5000/api/health
    """
    logger.info(f"Health check called from {request.remote_addr}")
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "protocol": "HTTP",
        "message": "Server is running"
    }), 200


@app.route('/api/users', methods=['GET'])
def get_users():
    """
    STEP 1: GET request with data
    Demonstrates retrieving data from backend
    Test in Postman: GET http://localhost:5000/api/users
    """
    logger.info(f"Fetching users - Request from {request.remote_addr}")
    logger.info(f"Headers: {dict(request.headers)}")
    return jsonify({
        "status": "success",
        "data": users_db,
        "count": len(users_db),
        "transport": "HTTP"
    }), 200


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    STEP 1: GET request with path parameter
    Shows URL routing
    Test in Postman: GET http://localhost:5000/api/users/1
    """
    user = next((u for u in users_db if u["id"] == user_id), None)
    if user:
        return jsonify({
            "status": "success",
            "data": user
        }), 200
    return jsonify({
        "status": "error",
        "message": f"User {user_id} not found"
    }), 404


@app.route('/api/users', methods=['POST'])
def create_user():
    """
    STEP 1: POST request - sending data to server
    Shows how to accept and process data
    Test in Postman: 
    POST http://localhost:5000/api/users
    Body (JSON): {"name": "Alice", "email": "alice@example.com"}
    """
    data = request.get_json()
    logger.info(f"Creating user with data: {data}")
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({
            "status": "error",
            "message": "Name and email are required"
        }), 400
    
    new_user = {
        "id": max([u["id"] for u in users_db]) + 1,
        "name": data["name"],
        "email": data["email"]
    }
    users_db.append(new_user)
    
    return jsonify({
        "status": "success",
        "message": "User created",
        "data": new_user
    }), 201


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    STEP 1: PUT request - updating data
    Shows how to modify existing data
    Test in Postman:
    PUT http://localhost:5000/api/users/1
    Body (JSON): {"name": "Updated Name", "email": "newemail@example.com"}
    """
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        return jsonify({
            "status": "error",
            "message": f"User {user_id} not found"
        }), 404
    
    data = request.get_json()
    user.update(data)
    
    return jsonify({
        "status": "success",
        "message": "User updated",
        "data": user
    }), 200


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    STEP 1: DELETE request - removing data
    Test in Postman: DELETE http://localhost:5000/api/users/1
    """
    global users_db
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        return jsonify({
            "status": "error",
            "message": f"User {user_id} not found"
        }), 404
    
    users_db = [u for u in users_db if u["id"] != user_id]
    
    return jsonify({
        "status": "success",
        "message": "User deleted"
    }), 200


# ==================== STEP 2: RESPONSE HEADERS & CACHING ====================

@app.route('/api/cache-demo', methods=['GET'])
def cache_demo():
    """
    STEP 2: CDN & Caching concepts
    Shows cache headers that CDN would use
    Headers help CDN decide how long to cache content
    Test in Postman: GET http://localhost:5000/api/cache-demo
    """
    response = jsonify({
        "status": "success",
        "message": "This response is cacheable",
        "data": {
            "timestamp": datetime.now().isoformat(),
            "content": "Static data that can be cached"
        }
    })
    
    # These headers tell CDN to cache for 1 hour
    response.headers['Cache-Control'] = 'public, max-age=3600'
    response.headers['ETag'] = '"abc123"'
    response.headers['X-Cache-Strategy'] = 'CDN-Friendly'
    
    return response, 200


@app.route('/api/no-cache', methods=['GET'])
def no_cache():
    """
    STEP 2: Non-cacheable content
    Shows headers that prevent caching
    Test in Postman: GET http://localhost:5000/api/no-cache
    """
    response = jsonify({
        "status": "success",
        "message": "This response should NOT be cached",
        "data": {
            "timestamp": datetime.now().isoformat(),
            "random": __import__('random').random()
        }
    })
    
    # These headers tell CDN NOT to cache
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['X-Cache-Strategy'] = 'No-Cache'
    
    return response, 200


# ==================== STEP 3: REQUEST HEADERS & SECURITY ====================

@app.route('/api/request-headers', methods=['GET'])
def show_request_headers():
    """
    STEP 3: Understanding request headers
    Shows all headers sent by the client
    Important for security and debugging
    Test in Postman: GET http://localhost:5000/api/request-headers
    """
    return jsonify({
        "status": "success",
        "message": "Your request headers:",
        "headers": dict(request.headers),
        "method": request.method,
        "remote_addr": request.remote_addr,
        "user_agent": request.user_agent.string
    }), 200


@app.route('/api/secure-endpoint', methods=['POST'])
def secure_endpoint():
    """
    STEP 3: Security check - validating requests
    Shows how to check API keys/tokens
    Test in Postman: 
    POST http://localhost:5000/api/secure-endpoint
    Headers: x-api-key: secret123
    Body: {"data": "some data"}
    """
    api_key = request.headers.get('x-api-key')
    
    if not api_key or api_key != 'secret123':
        logger.warning(f"Unauthorized access attempt from {request.remote_addr}")
        return jsonify({
            "status": "error",
            "message": "Invalid or missing API key",
            "security": "HTTPS recommended for sensitive endpoints"
        }), 401
    
    data = request.get_json()
    return jsonify({
        "status": "success",
        "message": "Authenticated request received",
        "data": data,
        "security_level": "API Key validation passed"
    }), 200


# ==================== STEP 4: PROTOCOL INFO ====================

@app.route('/api/protocol-info', methods=['GET'])
def protocol_info():
    """
    Shows current protocol being used (HTTP or HTTPS)
    Test in Postman: GET http://localhost:5000/api/protocol-info
    """
    protocol = 'HTTPS' if request.is_secure else 'HTTP'
    
    return jsonify({
        "status": "success",
        "current_protocol": protocol,
        "is_secure": request.is_secure,
        "scheme": request.scheme,
        "message": f"You are using {protocol} - More secure requests use HTTPS"
    }), 200


# ==================== ERROR HANDLING ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {error}")
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("BACKEND API STARTING")
    print("=" * 60)
    print("\nStep 1: Start with HTTP")
    print("  Run: python app.py")
    print("  Visit: http://localhost:5000/api/health")
    print("\nStep 2: Test with Postman")
    print("  Import: system-design-learning/postman/collection.json")
    print("\nStep 3: Add HTTPS (TLS/SSL)")
    print("  Run: python app-https.py")
    print("\nStep 4: Test DNS & CDN")
    print("  Edit /etc/hosts for local DNS")
    print("=" * 60 + "\n")
    
    # Start with HTTP first
    app.run(host='0.0.0.0', port=5000, debug=True)
