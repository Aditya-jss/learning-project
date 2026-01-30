#!/bin/bash

# Generate self-signed SSL certificate for learning
# Run this ONCE to create certificates

echo "=========================================="
echo "Generating Self-Signed SSL Certificate"
echo "=========================================="

cd "$(dirname "$0")"

# Generate private key (2048-bit RSA)
openssl genrsa -out server.key 2048

# Generate certificate (valid for 365 days)
openssl req -new -x509 -key server.key -out server.crt -days 365 \
  -subj "/C=US/ST=State/L=City/O=Learning/CN=localhost"

echo ""
echo "✅ Certificate generated successfully!"
echo ""
echo "Files created:"
echo "  - server.key  → Private key (keep secret!)"
echo "  - server.crt  → Public certificate"
echo ""
echo "For HTTPS testing:"
echo "  1. Run: python app-https.py"
echo "  2. In Postman: Settings → General"
echo "  3. Disable 'SSL certificate verification'"
echo "  4. Test on https://localhost:5443"
echo ""
echo "⚠️  WARNING:"
echo "  - Self-signed certificates are NOT trusted by browsers"
echo "  - Only use for LOCAL TESTING & LEARNING"
echo "  - In production: Use Let's Encrypt or paid CA"
echo ""
