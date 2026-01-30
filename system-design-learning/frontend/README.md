# Frontend - System Design Learning Lab

## Open in Browser

**Option A: Direct File**
```bash
open index.html
# or just double-click the file
```

**Option B: Python Web Server (Better)**
```bash
# From the project root:
python -m http.server 8000
# Then visit: http://localhost:8000
```

**Option C: Live Server (VS Code)**
```bash
# Install extension: Live Server
# Right-click → Open with Live Server
```

## Features

✅ Beautiful modern UI with dark/light friendly design
✅ 7 interactive learning steps
✅ Test all endpoints directly in browser
✅ See live responses
✅ Create/Read/Update/Delete users
✅ Understand HTTP headers
✅ Test caching behavior
✅ Learn HTTPS/TLS
✅ DNS and CDN concepts

## Learning Tabs

1. **Step 1: HTTP Protocol**
   - Test basic GET requests
   - Understand HTTP fundamentals

2. **Step 2: Request Headers**
   - See what headers your browser sends
   - Understand header importance

3. **Step 3: Users API**
   - Full CRUD operations
   - Create, read, update, delete users
   - Practice with real API

4. **Step 4: HTTPS & TLS/SSL**
   - Learn encryption
   - Understand security
   - Compare HTTP vs HTTPS

5. **Step 5: DNS**
   - How domain names work
   - Local DNS setup
   - /etc/hosts configuration

6. **Step 6: CDN**
   - Content delivery networks
   - Cache headers
   - Geographic distribution

7. **Step 7: Postman**
   - Professional API testing
   - Import collection
   - Learn best practices

## How to Use

1. **Start Backend First**
   ```bash
   cd backend
   python app.py
   ```

2. **Open Frontend**
   - Double-click `index.html`
   - Or use Python web server

3. **Click Tabs and Test**
   - Each tab has explanations
   - Click buttons to test endpoints
   - See live responses

4. **Read the Explanations**
   - Each section explains the concept
   - Code examples are provided
   - Learn at your pace

## Response Format

All responses show:
- ✅ Status code and message
- 📊 Response data (JSON)
- ⏱️ Request timing
- 📋 Headers (in Postman)

## Troubleshooting

**Requests fail?**
- Make sure `python app.py` is running
- Check port 5000 is available
- No CORS errors (already enabled)

**HTTPS requests fail?**
- Run `python app-https.py` on port 5443
- It's disabled by default (only HTTP)

**Can't see responses?**
- Check browser console (F12)
- Make sure backend is running

## Next Steps

After learning here:
1. Try with **curl** in terminal
2. Test with **Postman**
3. Try **Node.js/JavaScript** backend
4. Add real **database** (PostgreSQL)
5. Deploy to **cloud** (AWS/Azure)

---

**Pro Tip:** Open browser DevTools (F12) → Network tab to see real HTTP requests! 🚀
