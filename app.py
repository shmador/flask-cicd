from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Tell Flask to trust the first X-Forwarded-For header (from your LB)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

@app.route('/health')
def health():
    return "", 200

@app.route('/')   # bind the “show_ip” handler to your root path
def show_ip():
    # ProxyFix makes request.remote_addr = the real client IP
    ip = request.remote_addr
    return f'<html><body><h1>Your public IP is: {ip}</h1></body></html>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

