from flask import Flask, jsonify
from flask_cors import CORS

from algorithms.Midcap_Algorithm import MidcapAlgorithm

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

# Sample route to test CORS
@app.route('/test', methods=['GET'])
def test():
    stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
    mid_cap_algo = MidcapAlgorithm(stocks)
    mid_cap_algo.rank_stocks_by_ema_difference()
    ans = mid_cap_algo.filter_stocks()
    data = {'message': ans}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)