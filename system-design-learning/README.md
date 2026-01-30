# 🚀 System Design Learning Lab
## Understanding DNS, CDN, Transport, Security & TLS/SSL

A **hands-on learning project** that teaches you real system design concepts through a **simple full-stack application**. Learn one concept at a time with practical examples and tests.

---

## 📚 What You'll Learn

This project teaches these concepts **step-by-step**:

| Step | Concept | What You'll Do |
|------|---------|----------------|
| 1️⃣ | **HTTP Protocol** | Make GET requests, understand request/response |
| 2️⃣ | **Request Headers** | See what headers are sent and why they matter |
| 3️⃣ | **CRUD Operations** | Create, Read, Update, Delete users from database |
| 4️⃣ | **HTTPS & TLS/SSL** | Encrypt data, use self-signed certificates |
| 5️⃣ | **DNS** | Map domain names to IP addresses locally |
| 6️⃣ | **CDN** | Understand caching headers and content delivery |
| 7️⃣ | **Postman Testing** | Test APIs like a professional developer |

---

## 🏗️ Project Structure

```
system-design-learning/
├── backend/                    # Flask API server
│   ├── app.py                 # HTTP server (port 5000)
│   ├── app-https.py           # HTTPS server (port 5443)
│   ├── requirements.txt        # Python dependencies
│   └── README.md
├── frontend/                   # Web interface
│   ├── index.html             # Beautiful UI with all tests
│   └── README.md
├── certificates/              # SSL/TLS certificates
│   ├── server.key             # Private key
│   ├── server.crt             # Public certificate
│   ├── generate-cert.sh       # Script to generate certs
│   └── README.md
├── postman/                   # API testing
│   ├── collection.json        # Postman collection (import this!)
│   └── README.md
└── README.md                  # This file
```

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start the HTTP Server
```bash
python app.py
```

You should see:
```
=====================================
BACKEND API STARTING
=====================================
 * Running on http://127.0.0.1:5000
```

### Step 3: Open Frontend in Browser
```bash
# Option A: Just open the file
open frontend/index.html

# Option B: Run a simple web server (better)
python -m http.server 8000
# Then visit: http://localhost:8000
```

### Step 4: Start Testing!
Click the tabs in the frontend and test endpoints. That's it! 🎉

---

## 📖 Detailed Learning Path

### **STEP 1: Understand HTTP Protocol**

**What is HTTP?**
- HTTP = HyperText Transfer Protocol
- It's how browsers talk to servers
- Uses **request → response** model
- Runs on **port 80**

**Test it:**
1. In frontend, click **"Step 1: HTTP"** tab
2. Click **"Test Health Check"** button
3. Look at the response:
   ```json
   {
     "status": "healthy",
     "protocol": "HTTP",
     "timestamp": "2024-01-15T10:30:45"
   }
   ```

**What happened:**
- Browser sent: `GET /api/health HTTP/1.1`
- Server received and processed it
- Server sent back JSON response
- Browser displayed the result

**In Postman:**
- Import collection: `postman/collection.json`
- Go to "Step 1: HTTP Basics"
- Click "Health Check (GET)" → **Send**

---

### **STEP 2: Request Headers & Response Headers**

**What are headers?**
- Metadata about the request/response
- Like "metadata about the metadata"
- Examples: `Content-Type`, `Cache-Control`, `Authorization`

**Common Request Headers:**
```
GET /api/health HTTP/1.1
Host: localhost:5000              ← Which server
User-Agent: Mozilla/5.0           ← What client is asking
Accept: application/json          ← What format you want
Accept-Language: en-US            ← Preferred language
Authorization: Bearer token123    ← Authentication
Custom-Header: custom-value       ← You can add your own!
```

**Common Response Headers:**
```
HTTP/1.1 200 OK
Content-Type: application/json         ← Format of response
Content-Length: 245                    ← Size of response
Cache-Control: max-age=3600            ← How long to cache (CDN!)
ETag: "abc123def"                      ← Content version
Set-Cookie: session=xyz                ← Store in browser
X-Custom-Header: value                 ← Custom info
```

**Test it:**
1. Frontend → **Step 2: Request Headers**
2. Click **"View Your Request Headers"**
3. See all headers your browser sends!

**In Postman:**
- Test: "Step 2: Request Headers & Response"
- Look at **Response → Headers** tab to see all headers
- Add custom header and see it in the response

---

### **STEP 3: CRUD Operations (Create, Read, Update, Delete)**

**What is CRUD?**
- Basic operations on any data
- **C**reate (POST) - add new data
- **R**ead (GET) - retrieve data
- **U**pdate (PUT) - modify existing data
- **D**elete (DELETE) - remove data

**Test CRUD:**

#### **READ (GET all users)**
```bash
GET /api/users
Response:
{
  "status": "success",
  "data": [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
  ]
}
```

#### **CREATE (POST new user)**
```bash
POST /api/users
Body: {"name": "Alice", "email": "alice@example.com"}

Response (201 Created):
{
  "status": "success",
  "data": {"id": 3, "name": "Alice", "email": "alice@example.com"}
}
```

#### **UPDATE (PUT existing user)**
```bash
PUT /api/users/1
Body: {"name": "John Updated", "email": "john.new@example.com"}

Response:
{
  "status": "success",
  "data": {"id": 1, "name": "John Updated", ...}
}
```

#### **DELETE (DELETE user)**
```bash
DELETE /api/users/2

Response:
{
  "status": "success",
  "message": "User deleted"
}
```

**Test in frontend:**
1. Click **Step 3: Users API** tab
2. Click **"Fetch All Users"**
3. Enter name and email, click **"Create User"**
4. See the new user appear!
5. Click **"Update"** or **"Delete"**

**In Postman:**
- Use "Step 3: Users API - CRUD"
- Try each request
- Modify user IDs and data
- See how responses change

---

### **STEP 4: HTTPS & TLS/SSL Security**

**Why do we need HTTPS?**
- HTTP sends data in **plain text** 😱
- Anyone on WiFi can read it
- Passwords, credit cards, etc. visible
- HTTPS **encrypts** the data 🔒

**HTTP vs HTTPS:**

| Feature | HTTP | HTTPS |
|---------|------|-------|
| **Encryption** | None (plain text) | TLS/SSL encrypted |
| **Port** | 80 | 443 |
| **URL** | `http://` | `https://` |
| **Certificate** | None | Required |
| **Safe for** | Public data | Sensitive data |

**How HTTPS Works:**
```
1. Browser: "Connect securely"
2. Server: Sends SSL certificate
3. Browser: "Is this certificate valid?"
4. Both agree on encryption: AES-256
5. Data is now encrypted!
6. Anyone intercepting sees: "🔐🔐🔐" (gibberish)
```

**Setup HTTPS:**

First, generate self-signed certificate:
```bash
cd certificates
bash generate-cert.sh
```

Then run HTTPS server:
```bash
cd backend
python app-https.py
```

Visit: `https://localhost:5443/api/health`

⚠️ **Browser Warning:** You'll see "Not Secure" because certificate is self-signed. That's OK for learning!

**Test in Postman:**
1. Go to **Settings** → **General**
2. Turn OFF "SSL certificate verification" (only for testing!)
3. Go to "Step 5: HTTPS & TLS/SSL"
4. Click "Secure Health Check"
5. See it works even with self-signed cert!

**Important Security Points:**
```
✅ Self-signed: Good for LOCAL learning only
❌ Never in production: Use Let's Encrypt (free!)
🔒 Always: Use HTTPS in production
🗝️ Private key: Never share server.key
```

**Generate Real Certificates (for production):**
```bash
# Let's Encrypt (free)
certbot certonly --standalone -d yourdomain.com

# Creates:
# - /etc/letsencrypt/live/yourdomain.com/fullchain.pem
# - /etc/letsencrypt/live/yourdomain.com/privkey.pem
```

---

### **STEP 5: DNS (Domain Name System)**

**What is DNS?**
- DNS = Domain Name System
- Translates human-readable names → IP addresses
- Example: `google.com` → `142.250.80.46`

**How DNS Works:**
```
You: "What's the IP of google.com?"
    ↓
DNS Server 1 → Root nameserver
    ↓
DNS Server 2 → TLD nameserver (.com)
    ↓
DNS Server 3 → Authoritative nameserver
    ↓
Response: "142.250.80.46"
    ↓
Your browser connects to that IP
```

**Local DNS Testing:**

For this learning project, use **local DNS** via `/etc/hosts`:

**On macOS/Linux:**
```bash
sudo nano /etc/hosts

# Add this line:
127.0.0.1  myapp.local
127.0.0.1  api.local
127.0.0.1  cdn.local

# Save: Ctrl+O → Enter → Ctrl+X
```

**Verify it works:**
```bash
ping myapp.local
nslookup myapp.local
```

**Now test:**
```
In browser:
http://myapp.local:5000/api/health    ← Works!
http://myapp.local:5000               ← Shows frontend!
```

**DNS in System Design:**
- **Performance**: Caches IP addresses (TLL=3600s)
- **Failover**: Route to backup server if primary fails
- **Load Balancing**: One domain → Multiple IPs
- **Geographic Routing**: Route to nearest server

---

### **STEP 6: CDN (Content Delivery Network)**

**What is CDN?**
- CDN = Content Delivery Network
- Caches content in multiple locations worldwide
- Users get content from nearest location
- Makes websites **much faster** ⚡

**CDN Benefits:**
```
Before CDN:
User in Tokyo → Request to server in New York
         ↓
    12,000km away
    200ms latency
    😠 Slow!

After CDN:
User in Tokyo → Request to CDN in Tokyo
         ↓
    1km away
    5ms latency
    😊 Fast!
```

**How CDN Uses Cache Headers:**

The server sends headers telling CDN **how long to cache**:

```
Response Headers:
Cache-Control: public, max-age=3600
```

This means:
- `public`: Anyone can cache this
- `max-age=3600`: Cache for 1 hour (3600 seconds)

**Static content (fast to cache):**
```
Cache-Control: public, max-age=86400   ← Cache 1 day
```
- JavaScript files
- CSS files
- Images
- PDFs

**Dynamic content (don't cache):**
```
Cache-Control: no-cache, no-store, must-revalidate
```
- User login pages
- Real-time data
- API responses with user data

**Test Caching:**
1. Frontend → **Step 6: CDN**
2. Click **"View Cacheable Content"** → See `Cache-Control: public, max-age=3600`
3. Click **"View Non-Cacheable Content"** → See `Cache-Control: no-cache`

**In Postman:**
- Test: "Step 4: Security & API Keys"
- Go to Response → Headers
- Look for `Cache-Control` header
- See the difference!

**Real CDNs in Production:**
- **Cloudflare** - Fastest growing, $20/month
- **AWS CloudFront** - Amazon's CDN
- **Akamai** - Enterprise, very expensive
- **Fastly** - Real-time CDN

---

### **STEP 7: Testing with Postman**

**What is Postman?**
- Tool for testing APIs
- Like "browser for APIs"
- Great for debugging
- Essential for developers

**Install Postman:**
1. Go to: https://www.postman.com/downloads/
2. Download and install
3. Create free account

**Import Collection:**
1. Open Postman
2. Click **Import** button (top left)
3. Choose file: `postman/collection.json`
4. See all endpoints organized!

**Collection Structure:**
```
System Design Learning
├── Step 1: HTTP Basics
│   ├── Health Check (GET)
│   └── Protocol Info (GET)
├── Step 2: Request Headers
│   └── View Your Headers (GET)
├── Step 3: CRUD Operations
│   ├── Get All Users (GET)
│   ├── Get Single User (GET)
│   ├── Create User (POST)
│   ├── Update User (PUT)
│   └── Delete User (DELETE)
├── Step 4: Security & Caching
│   ├── Cache Demo (GET)
│   ├── No Cache (GET)
│   ├── Secure Endpoint Wrong Key (POST)
│   └── Secure Endpoint Correct Key (POST)
└── Step 5: HTTPS & TLS/SSL
    ├── Secure Health Check (GET)
    └── Certificate Info (GET)
```

**Using Postman:**

1. **Send a Request:**
   - Click any request
   - See the method (GET, POST, etc)
   - See the URL
   - See the Body (if POST/PUT)
   - Click **Send** button

2. **View Response:**
   - See Status Code (200=OK, 404=Not Found)
   - Click **Headers** to see response headers
   - Click **Body** to see the data

3. **Try Different Things:**
   - Change the URL
   - Add headers
   - Modify request body
   - See how server responds

**Important Postman Settings:**

For HTTPS with self-signed certificates:
1. Click **Settings** (gear icon)
2. Go to **General** tab
3. Find **SSL certificate verification**
4. Turn it **OFF** (only for local testing!)
5. Now HTTPS requests will work

**Example: Test User Creation**

```
Method: POST
URL: http://localhost:5000/api/users
Headers:
  Content-Type: application/json

Body (raw JSON):
{
  "name": "Bob Smith",
  "email": "bob@example.com"
}

Response (201 Created):
{
  "status": "success",
  "message": "User created",
  "data": {
    "id": 4,
    "name": "Bob Smith",
    "email": "bob@example.com"
  }
}
```

---

## 🎯 Learning Exercises

### Exercise 1: HTTP Basics
- [ ] Test health check endpoint
- [ ] See the full HTTP request/response
- [ ] Understand GET method

### Exercise 2: Request Headers
- [ ] View all request headers
- [ ] Add custom header and see it echoed back
- [ ] Understand what each header means

### Exercise 3: CRUD Operations
- [ ] Create 3 new users
- [ ] Read all users
- [ ] Update one user's email
- [ ] Delete one user
- [ ] Create again (IDs will be new)

### Exercise 4: Error Handling
- [ ] Try creating user without email (see 400 error)
- [ ] Try updating user that doesn't exist (see 404 error)
- [ ] Try deleting with wrong ID (see 404 error)

### Exercise 5: Caching
- [ ] Test cacheable content
- [ ] Test non-cacheable content
- [ ] Understand difference in headers

### Exercise 6: Security & API Keys
- [ ] Test secure endpoint WITHOUT key (see 401 Unauthorized)
- [ ] Test secure endpoint WITH correct key (see 200 OK)
- [ ] Understand API key validation

### Exercise 7: HTTPS/TLS
- [ ] Start HTTPS server on port 5443
- [ ] Test HTTPS endpoint
- [ ] See how data is encrypted
- [ ] Disable SSL verification in Postman

### Exercise 8: DNS
- [ ] Edit `/etc/hosts` to add `myapp.local`
- [ ] Ping `myapp.local` from terminal
- [ ] Visit `http://myapp.local:5000` in browser
- [ ] Understand DNS mapping

---

## 📊 Key Concepts Summary

### HTTP Protocol
```
Request:
GET /api/users HTTP/1.1
Host: localhost:5000
Accept: application/json

Response:
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 256

[JSON data here]
```

### Request Methods
- **GET**: Retrieve data (no body)
- **POST**: Create new data (with body)
- **PUT**: Update existing (with body)
- **DELETE**: Remove data (no body)
- **PATCH**: Partial update

### HTTP Status Codes
| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Request successful |
| 201 | Created | New resource created |
| 400 | Bad Request | Invalid data |
| 401 | Unauthorized | Need authentication |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Something broke |

### Headers
- **Request**: Client → Server info
- **Response**: Server → Client info
- **Cache-Control**: How long to cache
- **ETag**: Content version/identifier
- **Content-Type**: Format of data
- **Authorization**: Auth credentials

### HTTPS/TLS/SSL
- **HTTP**: Plain text (insecure)
- **HTTPS**: Encrypted (secure)
- **TLS/SSL**: Encryption protocol
- **Port 443**: HTTPS default port
- **Certificate**: Proves server identity

### DNS
- Maps domain names → IP addresses
- Caches results for performance
- Routes traffic geographically
- Enables failover/load balancing

### CDN
- Caches content worldwide
- Serves from nearest location
- Uses Cache-Control headers
- Makes sites faster ⚡

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 5000 is already in use
lsof -i :5000

# Kill the process using port 5000
kill -9 <PID>

# Or use different port
python app.py --port 5001
```

### HTTPS certificate error
```bash
# Regenerate certificate
cd certificates
rm server.* 
bash generate-cert.sh

# Or disable SSL verification in Postman Settings
```

### Frontend requests fail
```bash
# Make sure backend is running
python app.py

# Check CORS is enabled (it is in app.py)
# Try localhost instead of 127.0.0.1
```

### DNS not resolving (macOS)
```bash
# Flush DNS cache
sudo dscacheutil -flushcache

# Verify hosts file
cat /etc/hosts | grep myapp
```

---

## 💡 Pro Tips

1. **Always check response headers** → Teaches you about caching, security, etc
2. **Try to break things** → Change user IDs, remove required fields, etc
3. **Read error messages** → They tell you exactly what's wrong
4. **Use Postman** → Better than browser for understanding APIs
5. **Monitor network traffic** → See real requests/responses
6. **Start simple** → HTTP before HTTPS, then add features

---

## 🎓 Next Steps After Learning

Once you master this project:

1. **Real Databases** → PostgreSQL, MongoDB instead of in-memory
2. **Authentication** → JWT tokens, OAuth2
3. **Microservices** → Multiple backends, communication
4. **Docker & K8s** → Containerization, orchestration
5. **Load Balancing** → Nginx, HAProxy
6. **Monitoring** → Prometheus, Grafana
7. **CI/CD** → GitHub Actions, Jenkins

---

## 📚 Resources

### Official Docs
- [HTTP Spec](https://tools.ietf.org/html/rfc7231)
- [DNS RFC](https://tools.ietf.org/html/rfc1035)
- [TLS 1.3 Spec](https://tools.ietf.org/html/rfc8446)

### Learning Sites
- [MDN Web Docs](https://developer.mozilla.org/)
- [Postman Learning Center](https://learning.postman.com/)
- [System Design Primer](https://github.com/donnemartin/system-design-primer)

### Tools
- [Postman](https://www.postman.com/) - API testing
- [Insomnia](https://insomnia.rest/) - Alternative to Postman
- [curl](https://curl.se/) - Command line API testing

---

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | HTTP API server (port 5000) |
| `app-https.py` | HTTPS API server (port 5443) |
| `index.html` | Beautiful testing UI (frontend) |
| `collection.json` | Postman collection with all tests |
| `server.crt` | SSL certificate (public) |
| `server.key` | SSL private key (secret) |
| `generate-cert.sh` | Script to generate certificates |

---

## 🤝 Learning Tips

- **Don't memorize** → Understand concepts
- **Experiment** → Break things safely
- **Read errors** → They're helpful
- **Use Postman** → Easier than curl
- **Check headers** → Where the magic is
- **Start simple** → HTTP → HTTPS → DNS → CDN

---

## ⭐ Project Goals

✅ Understand how web communication works
✅ Learn security with HTTPS/TLS
✅ Master CRUD operations
✅ Understand DNS and CDN
✅ Practice with professional tools (Postman)
✅ Be ready for system design interviews

---

## 📄 License

This project is for educational purposes. Use it to learn!

---

## 🎉 You're Ready!

Start with Step 1, take your time, experiment, and enjoy learning! 🚀

Questions? Check the step-by-step explanations in each tab of the frontend!
