from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

# Sample route to test CORS
@app.route('/test', methods=['GET'])
def test():
    data = {'message': 'test'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)