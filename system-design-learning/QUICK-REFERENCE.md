# 🚀 Quick Reference Guide

## 30-Second Setup

```bash
cd backend
python app.py
```

Open in browser: `frontend/index.html`

Done! Start clicking tabs to learn. 🎉

---

## HTTP Methods Cheat Sheet

```
GET     → Read data        (no body needed)
POST    → Create data      (send JSON body)
PUT     → Update data      (send JSON body)
DELETE  → Remove data      (no body needed)
```

### Examples with curl

```bash
# GET - Retrieve
curl http://localhost:5000/api/users

# POST - Create
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'

# PUT - Update  
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Bob","email":"bob@example.com"}'

# DELETE - Remove
curl -X DELETE http://localhost:5000/api/users/1
```

---

## Status Codes Reference

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Request successful |
| 201 | Created | New resource created |
| 400 | Bad Request | Invalid data |
| 401 | Unauthorized | Need API key/auth |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Something broke |

---

## Headers Explained

### Request Headers (Client → Server)

```
User-Agent: Mozilla/5.0        Who's asking?
Content-Type: application/json  Format of body
Authorization: Bearer xyz       Authentication
x-api-key: secret123           API key
```

### Response Headers (Server → Client)

```
Content-Type: application/json       Format of response
Cache-Control: max-age=3600          Cache for 1 hour
ETag: "abc123"                       Content version
Set-Cookie: session=xyz              Store in browser
X-RateLimit-Remaining: 99            Rate limit info
```

---

## HTTP vs HTTPS

| Feature | HTTP | HTTPS |
|---------|------|-------|
| Encryption | ❌ None | ✅ TLS/SSL |
| Port | 80 | 443 |
| URL Prefix | `http://` | `https://` |
| Certificate | ❌ Not needed | ✅ Required |
| Secure? | ❌ No | ✅ Yes |

**Use HTTP for**: Learning, local testing
**Use HTTPS for**: Everything with data

---

## DNS Lookup

```
You: "What's the IP of google.com?"
     ↓
Browser checks cache
     ↓
If not found → Ask ISP DNS server
     ↓
ISP asks root nameserver
     ↓
Get IP: 142.250.80.46
     ↓
Connect to that IP
```

### Local DNS Setup (macOS)

```bash
# Edit hosts file
sudo nano /etc/hosts

# Add:
127.0.0.1  myapp.local

# Save: Ctrl+O, Enter, Ctrl+X

# Test
ping myapp.local
nslookup myapp.local
```

---

## CDN Cache Headers

### Cacheable (store this!)
```
Cache-Control: public, max-age=86400
```
✅ CDN caches for 1 day
✅ Fastest response

### Non-cacheable (always fresh!)
```
Cache-Control: no-cache, no-store, must-revalidate
```
❌ CDN won't cache
❌ Always fetch from server

---

## Testing Commands

### With curl

```bash
# Health check
curl http://localhost:5000/api/health

# Get all users
curl http://localhost:5000/api/users

# Create user
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"test","email":"test@test.com"}'

# HTTPS (self-signed)
curl --insecure https://localhost:5443/api/health

# Show response headers
curl -i http://localhost:5000/api/health

# Show all headers (request & response)
curl -v http://localhost:5000/api/health
```

### With Postman

1. Import: `postman/collection.json`
2. Select request
3. Click **Send**
4. View **Body** and **Headers**

### With Python

```python
import requests

# GET
resp = requests.get('http://localhost:5000/api/users')
print(resp.json())

# POST
data = {'name': 'test', 'email': 'test@test.com'}
resp = requests.post('http://localhost:5000/api/users', json=data)
print(resp.json())
```

---

## Troubleshooting Quick Fixes

### Backend Won't Start

```bash
# Check if port is already in use
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use different port
python app.py --port 5001
```

### HTTPS Certificate Error

```bash
# In Postman Settings → General
# Disable "SSL certificate verification"

# Or regenerate certificate
cd certificates
bash generate-cert.sh
```

### Can't Reach Backend

```bash
# Is backend running?
python app.py

# Is port correct?
# HTTP: localhost:5000
# HTTPS: localhost:5443

# Check firewall
# Usually not needed for localhost
```

### DNS Not Resolving

```bash
# Edit /etc/hosts
sudo nano /etc/hosts

# Verify entry exists
cat /etc/hosts | grep myapp

# Flush DNS cache (macOS)
sudo dscacheutil -flushcache

# Test
ping myapp.local
```

---

## API Testing Flow

```
1. Identify endpoint
2. Choose HTTP method (GET, POST, etc)
3. Set URL
4. Add body (if POST/PUT)
5. Add headers (if needed)
6. Click Send
7. Check status code
8. Read response
9. Check response headers
```

---

## Security Best Practices

✅ Always use HTTPS in production
✅ Use API keys for authentication
✅ Validate all input data
✅ Return generic error messages
✅ Rate limit API calls
✅ Log all access attempts
✅ Keep private keys secret
✅ Update dependencies regularly

---

## Performance Tips

| Tip | Benefit |
|-----|---------|
| Gzip compression | 80% smaller responses |
| Caching | 1000x faster (from cache) |
| Pagination | Less bandwidth |
| CDN | Globally fast |
| Async tasks | Faster response |
| Indexes | Faster queries |

---

## Project Endpoints

### HTTP Server (5000)

```
GET  /api/health              Health check
GET  /api/protocol-info       Current protocol
GET  /api/users               All users
GET  /api/users/<id>          Single user
POST /api/users               Create user
PUT  /api/users/<id>          Update user
DELETE /api/users/<id>        Delete user
GET  /api/request-headers     See headers
GET  /api/cache-demo          Cacheable content
GET  /api/no-cache            Non-cacheable
POST /api/secure-endpoint     API key auth
```

### HTTPS Server (5443)

```
GET  /api/health              Health check (encrypted)
GET  /api/protocol-info       Protocol info (encrypted)
GET  /api/certificate-info    Certificate details
POST /api/secure-endpoint     API key auth (encrypted)
```

---

## Learning Checklist

- [ ] HTTP GET request works
- [ ] POST creates user
- [ ] PUT updates user
- [ ] DELETE removes user
- [ ] Headers are visible
- [ ] Caching headers understood
- [ ] HTTPS connection works
- [ ] API key validation works
- [ ] DNS setup complete
- [ ] Postman collection imported
- [ ] All 7 steps completed

---

## File Locations

```
system-design-learning/
├── README.md               ← Full guide (start here!)
├── ADVANCED-CONCEPTS.md    ← Deep dives
├── quickstart.sh           ← Auto setup
├── backend/
│   ├── app.py             ← HTTP server
│   ├── app-https.py       ← HTTPS server  
│   ├── requirements.txt    ← Python deps
│   └── README.md          ← Backend guide
├── frontend/
│   ├── index.html         ← Beautiful UI
│   └── README.md          ← Frontend guide
├── certificates/
│   ├── server.crt         ← Public cert
│   ├── server.key         ← Private key
│   ├── generate-cert.sh   ← Cert script
│   └── README.md          ← SSL guide
└── postman/
    ├── collection.json    ← All tests
    └── README.md          ← Postman guide
```

---

## Next Learning Goals

1. ✅ Understand HTTP/HTTPS
2. ✅ Understand DNS
3. ✅ Understand CDN/Caching
4. ✅ Understand TLS/SSL
5. 🎯 Learn real database (PostgreSQL)
6. 🎯 Learn authentication (JWT)
7. 🎯 Learn load balancing
8. 🎯 Learn containerization (Docker)
9. 🎯 Learn orchestration (Kubernetes)
10. 🎯 Master system design interviews

---

## Useful Links

- [HTTP Spec](https://tools.ietf.org/html/rfc7231)
- [DNS Spec](https://tools.ietf.org/html/rfc1035)  
- [TLS Spec](https://tools.ietf.org/html/rfc8446)
- [Postman Docs](https://learning.postman.com/)
- [Flask Docs](https://flask.palletsprojects.com/)

---

**Remember: The best way to learn is by doing. Start testing! 🚀**
