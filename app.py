from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def show_ip():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    return f'<html><body><h1>Your public IP is: {ip}</h1></body></html>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

