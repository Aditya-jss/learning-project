# Backend API Server

## HTTP Server (Port 5000)
```bash
python app.py
```

Then test:
```bash
curl http://localhost:5000/api/health
```

## HTTPS Server (Port 5443)
```bash
python app-https.py
```

Then test in browser with self-signed cert warning:
```bash
# In Postman: Disable SSL verification in Settings
curl --insecure https://localhost:5443/api/health
```

## Setup
```bash
pip install -r requirements.txt
```

## Available Endpoints

### GET Requests (retrieve data)
- `GET /api/health` - Server health check
- `GET /api/protocol-info` - Current protocol (HTTP/HTTPS)
- `GET /api/users` - Get all users
- `GET /api/users/1` - Get user by ID
- `GET /api/request-headers` - See your request headers
- `GET /api/cache-demo` - Test cacheable content
- `GET /api/no-cache` - Test non-cacheable content

### POST Requests (create data)
- `POST /api/users` - Create new user
  ```json
  {"name": "Alice", "email": "alice@example.com"}
  ```
- `POST /api/secure-endpoint` - Secure endpoint with API key
  ```
  Header: x-api-key: secret123
  Body: {"data": "value"}
  ```

### PUT Requests (update data)
- `PUT /api/users/1` - Update user
  ```json
  {"name": "Updated Name", "email": "new@example.com"}
  ```

### DELETE Requests (delete data)
- `DELETE /api/users/1` - Delete user

## Testing

### With curl:
```bash
# GET
curl http://localhost:5000/api/health

# POST
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Bob","email":"bob@example.com"}'

# PUT
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated","email":"updated@example.com"}'

# DELETE
curl -X DELETE http://localhost:5000/api/users/1

# HTTPS with insecure flag (self-signed cert)
curl --insecure https://localhost:5443/api/health
```

### With Postman:
1. Import `postman/collection.json`
2. Send requests
3. View responses with headers

### With Python:
```python
import requests

# GET
response = requests.get('http://localhost:5000/api/users')
print(response.json())

# POST
data = {'name': 'Charlie', 'email': 'charlie@example.com'}
response = requests.post('http://localhost:5000/api/users', json=data)
print(response.json())
```

## Key Learning Points

1. **HTTP**: Plain text protocol
2. **HTTPS**: Encrypted version of HTTP
3. **Status Codes**: 200=OK, 201=Created, 400=Bad, 401=Unauthorized, 404=Not Found, 500=Error
4. **Headers**: Metadata about request/response
5. **Cache-Control**: Tells CDN how long to cache
6. **API Keys**: Simple authentication method

## Common Issues

**Port already in use:**
```bash
lsof -i :5000
kill -9 <PID>
```

**HTTPS certificate error:**
```bash
# In Postman Settings → General
# Disable "SSL certificate verification"
```

**ModuleNotFoundError:**
```bash
pip install -r requirements.txt
```

That's it! You're learning system design! 🚀
