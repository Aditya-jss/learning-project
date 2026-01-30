# SSL/TLS Certificates

Self-signed certificates for local learning and testing.

## Files

- `server.crt` - Public certificate (safe to share)
- `server.key` - Private key (KEEP SECRET!)

## How to Use

1. **Certificates already generated** (run `generate-cert.sh` if needed)

2. **Start HTTPS server:**
   ```bash
   cd backend
   python app-https.py
   ```

3. **In Postman:**
   - Settings → General
   - Disable "SSL certificate verification" (self-signed only!)
   - Then test HTTPS endpoints

4. **In curl:**
   ```bash
   curl --insecure https://localhost:5443/api/health
   ```

5. **In browser:**
   - You'll see security warning (expected!)
   - Click "Advanced" and proceed
   - Connection is still encrypted

## Understanding Certificates

**What it contains:**
- Public key (shared with everyone)
- Certificate info (name, expiration, etc)
- Server signature

**Private key should:**
- Never be shared
- Never be committed to git
- Only on trusted servers
- Backed up securely

## Generate New Certificate

If you want to regenerate:

```bash
bash generate-cert.sh
```

This creates:
- Valid for 365 days
- Localhost only
- Self-signed (no CA authority)

## Production vs Learning

| Aspect | Learning | Production |
|--------|----------|------------|
| **Cert Source** | Self-signed | Let's Encrypt/CA |
| **Validity** | 365 days | 90 days (renewable) |
| **Cost** | Free | Free (Let's Encrypt) |
| **Trust** | Browsers warn | Browsers trust |
| **Where** | Local only | Real servers |

## Free Production Certificates

Get real certificates for free:

```bash
# Let's Encrypt (automatic)
certbot certonly --standalone -d yourdomain.com

# Creates valid certificate automatically!
```

## Common Issues

**Certificate expired:**
```bash
# Regenerate
bash generate-cert.sh
```

**Browser warning is normal:**
- Self-signed = no trusted authority
- Still encrypted though!
- Production uses trusted CAs

**Can't trust certificate:**
- Only for learning on localhost
- Production uses different cert

---

Start your HTTPS learning today! 🔒
