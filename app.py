from flask import Flask, request, redirect, jsonify, send_from_directory
import hashlib
import os
import time
import threading
import json

app = Flask(__name__, static_folder='static')

# In-memory storage
url_mappings = {}

# Try to connect to Redis, but fall back to in-memory storage
redis_available = False
try:
    import redis
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    print(f"Attempting to connect to Redis at {redis_host}:6379")
    
    # Test the connection
    redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True, socket_connect_timeout=2.0)
    redis_available = redis_client.ping()
    print(f"Redis connection successful: {redis_available}")
except Exception as e:
    print(f"Redis connection failed: {str(e)}")
    print("Using in-memory storage instead")
    redis_available = False

def save_url_mapping(short_code, long_url):
    if redis_available:
        try:
            redis_client.set(short_code, long_url)
            return True
        except Exception as e:
            print(f"Redis error when saving: {str(e)}")
            url_mappings[short_code] = long_url
            return False
    else:
        url_mappings[short_code] = long_url
        # Persist to a simple JSON file
        threading.Thread(target=save_to_file).start()
        return True

def get_url_mapping(short_code):
    if redis_available:
        try:
            return redis_client.get(short_code)
        except Exception as e:
            print(f"Redis error when retrieving: {str(e)}")
            return url_mappings.get(short_code)
    else:
        return url_mappings.get(short_code)

def save_to_file():
    try:
        with open('url_mappings.json', 'w') as f:
            json.dump(url_mappings, f)
    except Exception as e:
        print(f"Error saving to file: {str(e)}")

def load_from_file():
    try:
        with open('url_mappings.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Load existing mappings from file if Redis is not available
if not redis_available:
    url_mappings = load_from_file()
    print(f"Loaded {len(url_mappings)} URLs from local storage")

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
    save_url_mapping(short_code, long_url)
    short_url = f"http://{request.host}/{short_code}"
    return {'short_url': short_url}, 201

@app.route('/<short_code>')
def redirect_url(short_code):
    if short_code == 'favicon.ico':
        return '', 404
        
    long_url = get_url_mapping(short_code)
    if long_url:
        return redirect(long_url)
    return {'error': 'URL not found'}, 404

@app.route('/')
def homepage():
    return send_from_directory('static', 'index.html')

@app.route('/api')
def api_info():
    storage_info = "Redis" if redis_available else "In-memory (Redis unavailable)"
    return jsonify({
        "message": "URL Shortener API",
        "storage": storage_info,
        "endpoints": {
            "POST /shorten": "Shorten a URL (requires JSON with 'url' field)",
            "GET /<short_code>": "Redirect to original URL"
        },
        "url_count": len(url_mappings) if not redis_available else "Unknown (Redis)"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 