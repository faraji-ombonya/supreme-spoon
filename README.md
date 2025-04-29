# Harakisha 360 API

Welcome to the Harakisha 360 API documentation.

To interact with protected endpoints, you need to authenticate using OAuth2 **Client Credentials**.

## 🔐 Getting Started with OAuth2

To register a client application and obtain your **Client ID** and **Client Secret**, follow the steps outlined in the [Django OAuth Toolkit documentation](https://django-oauth-toolkit.readthedocs.io/en/latest/getting_started.html#client-credential).

These credentials are required to obtain an access token which you'll use to authenticate API requests.


# OAuth2 Client Credentials Flow – Django Project

This guide describes how to authenticate machine-to-machine using the **Client Credentials Grant** type in a Django application. It is useful for background services or workers that need to interact with your API securely without user intervention.

---

## 🚀 Step 1: Register a Client Application

Visit the following URL in your browser to register a new OAuth2 application:

```
http://127.0.0.1:8000/auth/applications/register/
```

When filling out the form:

- Choose **"Client Credentials"** as the **Authorization Grant Type**.
- Note down the generated `Client ID` and `Client Secret` after saving.

---

## 🔐 Step 2: Export Credentials to Your Environment

Export your `Client ID` and `Client Secret` as environment variables:

```bash
export ID=axXSSBVuvOyGVzh4PurvKaq5MHXMm7FtrHgDMi4u
export SECRET=1fuv5WVfR7A5BlF0o155H7s5bLgXlwWLhi3Y7pdJ9aJuCdl0XV5Cxgd0tri7nSzC80qyrovh8qFXFHgFAAc0ldPNn5ZYLanxSm1SI1rxlRrWUP591wpHDGa3pSpB6dCZ
```

---

## 🔐 Step 3: Encode Credentials for HTTP Basic Authentication

Use Python to generate a base64-encoded version of your client credentials:

```python
import base64

client_id = "axXSSBVuvOyGVzh4PurvKaq5MHXMm7FtrHgDMi4u"
secret = "1fuv5WVfR7A5BlF0o155H7s5bLgXlwWLhi3Y7pdJ9aJuCdl0XV5Cxgd0tri7nSzC80qyrovh8qFXFHgFAAc0ldPNn5ZYLanxSm1SI1rxlRrWUP591wpHDGa3pSpB6dCZ"

credentials = f"{client_id}:{secret}"
encoded = base64.b64encode(credentials.encode("utf-8"))
print(encoded.decode("utf-8"))
```

This will return a long base64 string, for example:

```
SUQzTEhGbUdUOGZwaWVDb2NiZmVpd2pSMU1IVTQ2Q2dnZ0tIeExZZzpwYmtkZjJfc2hhMjU2JDEwMDAwMDAkaGp0dlQ3dVNmRTdXNVhKQmNQM3F5QiRsTml3ZHZCWWlpaVh0TmNQYUthMklNeXFtRTcyekt6ZVdwbGRTZzNJbmJvPQ==
```

Export it as:

```bash
export CREDENTIAL=SUQzTEhGbUdUOGZwaWVDb2NiZmVpd2pSMU1IVTQ2Q2dnZ0tIeExZZzpwYmtkZjJfc2hhMjU2JDEwMDAwMDAkaGp0dlQ3dVNmRTdXNVhKQmNQM3F5QiRsTml3ZHZCWWlpaVh0TmNQYUthMklNeXFtRTcyekt6ZVdwbGRTZzNJbmJvPQ==
```

---

## 🎯 Step 4: Get an Access Token (Using Custom Token Endpoint)

Use `curl` to get an access token via your **custom token endpoint**:

```bash
curl -X POST \
  -H "Authorization: Basic ${CREDENTIAL}" \
  -H "Cache-Control: no-cache" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  "http://127.0.0.1:8000/api/auth/token/" \
  -d "grant_type=client_credentials"
```

> ✅ Make sure to use `/auth/token/` instead of the default `/o/token/`.

---

## ✅ Sample Response

The OAuth2 provider will respond with a JSON like this:

```json
{
  "access_token": "PaZDOD5UwzbGOFsQr34LQ7JUYOj3yK",
  "expires_in": 36000,
  "token_type": "Bearer",
  "scope": "read write"
}
```

You can now use this token to authenticate future API requests:

```http
Authorization: Bearer PaZDOD5UwzbGOFsQr34LQ7JUYOj3yK
```

---

## 📌 Summary

| Step            | Description                                        |
|-----------------|----------------------------------------------------|
| Register App    | `/o/applications/register/`                        |
| Token Endpoint  | `http://127.0.0.1:8000/auth/token/`                |
| Grant Type      | `client_credentials`                               |
| Token Type      | `Bearer`                                           |

---

