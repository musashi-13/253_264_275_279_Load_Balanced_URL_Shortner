from flask import Flask, request, redirect
import redis
import hashlib
import os

app = Flask(__name__)
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

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
    redis_client.set(short_code, long_url)
    short_url = f"http://{request.host}/{short_code}"
    return {'short_url': short_url}, 201

@app.route('/<short_code>')
def redirect_url(short_code):
    long_url = redis_client.get(short_code)
    if long_url:
        return redirect(long_url)
    return {'error': 'URL not found'}, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)