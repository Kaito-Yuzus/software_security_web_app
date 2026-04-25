from flask import Flask
from flask.sessions import SecureCookieSessionInterface
import secrets

# Create a Flask app exactly like your real app
app = Flask(__name__)
app.secret_key = "PASSWORD"  # Must match your app's SECRET_KEY

# Data you want to store in the session
session_data = {'user_id': 2}

# Use Flask's session interface to generate a proper session cookie
session_interface = SecureCookieSessionInterface()
serializer = session_interface.get_signing_serializer(app)

cookie_value = serializer.dumps(session_data)

print("Set this as your 'session' cookie in the browser:")
print(cookie_value)
print(secrets.token_hex(32))