from flask import Flask, request, jsonify
from db import DatabaseHandler

import string
import random

app = Flask(__name__)
app.config['DB_NAME'] = "url.db"

db = DatabaseHandler(app.config['DB_NAME'])
db.drop_tables()
db.init()

def generate_key(url: str) -> str:
	letters = string.ascii_letters
	return ''.join(random.choice(letters) for i in range(10))


# API

@app.route('/api/add', methods=['POST'])
def add_url():
	if 'url' in request.args:
		url = request.args['url']
		key = generate_key(url)
		db.add(url=url, key=key)
		return jsonify(dict(url=url, key=key))


@app.route('/api/get', methods=['GET'])
def get_url():
	if 'key' in request.args:
		key = request.args['key']
		url = db.search_url(key)
		return jsonify(dict(url=url[0]))


@app.route('/api/delete', methods=['DELETE'])
def delete_url(id):
	if 'id' in request.args:
		url_id = int(request.args['id'])
		db.delete_url(url_id)
		return jsonify(dict(status='success'))
	else:
		return jsonify(dict(status='failed'))


@app.route('/api/all', methods=['GET'])
def show_urls():
	urls = db.fetch_urls()
	data = [dict(id=url[0], url=url[1], key=url[2]) for url in urls]
	return jsonify(dict(data=data))

# REDIRECT SERVER

@app.route("/route/<url>")
def index_page():
   return render_templates('index.html')

if __name__ == '__main__':
	app.run(port=2000)