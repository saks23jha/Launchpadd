## API Defense & Input Control – Security Report

### Objective
This task focuses on protecting APIs from common attack vectors by enforcing strict input validation, sanitization, rate limiting, and security headers.

---

### Implemented Protections

#### 1. Payload Whitelisting
- Joi schemas ensure only allowed fields are accepted
- Unknown fields are stripped automatically

#### 2. Schema-Level Validation
- Strong validation for User and Product inputs
- Prevents malformed or malicious payloads

#### 3. Query & Payload Sanitization
- MongoDB operator injection prevented using express-mongo-sanitize
- XSS attacks prevented using xss-clean

#### 4. Rate Limiting
- Implemented using express-rate-limit
- Limits excessive API requests to prevent abuse

#### 5. Security Headers
- Helmet adds common security headers (CSP, HSTS, XSS protection)

---

### Manual Security Test Cases

#### SQL / NoSQL Injection
Payload:
```json
{ "email": { "$gt": "" } }
