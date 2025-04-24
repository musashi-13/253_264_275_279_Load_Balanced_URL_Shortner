from flask import Flask, request, redirect, jsonify, send_from_directory
import redis
import hashlib
import os
import argparse
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, static_folder='static')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)

def generate_short_url(long_url):
    # Generate a short code using MD5 hash
    hash_object = hashlib.md5(long_url.encode())
    return hash_object.hexdigest()[:6]

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json.get('url')
    if not long_url:
        return {'error': 'URL is required'}, 400
    short_code = generate_short_url(long_url)
    
    # Store the URL in Redis with a 30-second expiration
    redis_client.setex(short_code, 30, long_url)
    
    # Use X-Forwarded-Host header if available, otherwise use request.host
    host = request.headers.get('X-Forwarded-Host', request.host)
    
    # Use X-Forwarded-Proto header if available, otherwise use request.scheme
    scheme = request.headers.get('X-Forwarded-Proto', request.scheme)
    
    short_url = f"{scheme}://{host}/{short_code}"
    return {'short_url': short_url}, 201

@app.route('/<short_code>')
def redirect_url(short_code):
    long_url = redis_client.get(short_code)
    if long_url:
        return redirect(long_url)
    return {'error': 'URL not found or expired'}, 404

@app.route('/')
def homepage():
    return send_from_directory('static', 'index.html')

@app.route('/api')
def api_info():
    return jsonify({
        "message": "URL Shortener API",
        "endpoints": {
            "POST /shorten": "Shorten a URL (requires JSON with 'url' field)",
            "GET /<short_code>": "Redirect to original URL"
        }
    })

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask URL shortener app')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the Flask app on')
    args = parser.parse_args()
    
    print(f"Starting Flask app on port {args.port}...")
    app.run(host='0.0.0.0', port=args.port, debug=True)