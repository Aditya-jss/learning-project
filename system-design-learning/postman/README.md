# Postman Collection

Complete API testing collection for the System Design Learning project.

## How to Import

1. **Open Postman**
2. Click **Import** button (top left)
3. Select **File** tab
4. Choose: `collection.json` from this folder
5. Click **Import**

Done! All endpoints are now organized in Postman.

## Collection Structure

```
System Design Learning
├── Step 1: HTTP Basics
│   ├── Health Check (GET)
│   └── Check Protocol (GET)
├── Step 2: Request Headers & Response
│   └── View Your Request Headers (GET)
├── Step 3: Users API - CRUD
│   ├── Get All Users (GET)
│   ├── Get Single User (GET)
│   ├── Create User (POST)
│   ├── Update User (PUT)
│   └── Delete User (DELETE)
├── Step 4: Security & API Keys
│   ├── Cache Demo (GET)
│   ├── No Cache Demo (GET)
│   ├── Secure Endpoint (POST) - Wrong Key
│   └── Secure Endpoint (POST) - Correct Key
├── Step 5: HTTPS & TLS/SSL
│   ├── Secure Health Check (GET) - HTTPS
│   └── Certificate Info (GET) - HTTPS
└── Learning Guide
    └── README - Start Here
```

## Quick Start

1. **Start Backend:**
   ```bash
   python app.py
   ```

2. **Import Collection** (see steps above)

3. **Test Requests:**
   - Go to "Step 1: HTTP Basics"
   - Click "Health Check (GET)"
   - Click **Send**
   - See response!

## Important Settings

### For HTTPS Testing

1. Click **Settings** (gear icon)
2. Go to **General** tab
3. Find **SSL certificate verification**
4. Toggle to **OFF** (disable)
5. Now HTTPS requests work!

⚠️ Only disable for local testing with self-signed certs!

## Testing Path

Follow this order:

1. ✅ **HTTP Basics** - GET requests
2. ✅ **Request Headers** - See what client sends
3. ✅ **CRUD Operations** - Create, Read, Update, Delete
4. ✅ **Security** - API keys and caching
5. ✅ **HTTPS** - Encrypted connections

## Common Tests

### Test 1: Basic GET
```
Method: GET
URL: http://localhost:5000/api/health
→ Send
→ Look at Response → Body
```

### Test 2: Create User
```
Method: POST
URL: http://localhost:5000/api/users
Body (raw JSON):
{
  "name": "Your Name",
  "email": "your@email.com"
}
→ Send
→ See 201 Created with new user ID
```

### Test 3: Update User
```
Method: PUT
URL: http://localhost:5000/api/users/1
Body (raw JSON):
{
  "name": "Updated Name",
  "email": "new@email.com"
}
→ Send
→ See 200 OK with updated data
```

### Test 4: API Key Security
```
Method: POST
URL: http://localhost:5000/api/secure-endpoint

Headers:
x-api-key: secret123

Body (raw JSON):
{
  "data": "test"
}
→ Send
→ See 200 OK (correct key)
```

### Test 5: Wrong API Key
```
Same as Test 4, but use:
x-api-key: wrong-key

→ Send
→ See 401 Unauthorized
```

### Test 6: HTTPS Connection
```
Method: GET
URL: https://localhost:5443/api/health

Note:
- Must run: python app-https.py (port 5443)
- Disable SSL verification in Settings
→ Send
→ See encrypted connection works!
```

## Viewing Response Details

Every response shows:

**Status Code**
- 200 = OK ✅
- 201 = Created ✅
- 400 = Bad Request ❌
- 401 = Unauthorized ❌
- 404 = Not Found ❌
- 500 = Server Error ❌

**Headers Tab**
- `Cache-Control` - How long to cache
- `Content-Type` - Format of response
- `ETag` - Content version
- `X-Custom-Header` - Custom headers

**Body Tab**
- The actual response data
- Usually JSON

**Tests Tab** (advanced)
- Automated test scripts
- Validate responses
- Assert expected values

## Tips & Tricks

1. **Duplicate Request:**
   - Right-click → Duplicate
   - Modify for different test

2. **Save Response:**
   - Hover over response
   - Click save icon
   - For comparison later

3. **Environment Variables:**
   - Use {{baseUrl}} instead of full URL
   - Can switch between HTTP/HTTPS

4. **Pre-request Script:**
   - Set up data before request
   - Generate timestamps
   - Calculate signatures

5. **Tests:**
   - Automate validations
   - Check status codes
   - Verify response content

## Export/Share

Export collection:
1. Right-click collection
2. Export
3. Share with team

Import someone else's:
1. File → Import
2. Select collection.json
3. Use together!

## API Base URLs

| Protocol | URL | Port |
|----------|-----|------|
| HTTP | `http://localhost:5000` | 5000 |
| HTTPS | `https://localhost:5443` | 5443 |

## Troubleshooting

**Can't connect to backend:**
- Make sure `python app.py` is running
- Check port 5000 is available

**HTTPS fails:**
- Run `python app-https.py`
- Disable SSL verification in Settings
- Port must be 5443

**Status code issues:**
- 400: Check request body format (JSON)
- 401: Check API key header
- 404: Check URL and user ID

**Responses are empty:**
- Check backend console for errors
- Verify headers are correct
- Try simpler request first

---

Happy testing! 🚀

Remember: Postman is your best friend for API development!
