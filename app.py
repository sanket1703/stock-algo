from flask import Flask
from flask_cors import CORS


from DTS.Entry_Logic.buy_runner import start_buy_runner
from DTS.Entry_Logic.sell_runner import start_sell_runner
from DTS.Entry_Logic.sell_zone import start_sell_zone
from DTS.Entry_Logic.buy_zone import start_buy_zone

from Exit_Logic.exit_exe import exit_execute

from Verification import verification

app = Flask(__name__)
CORS(app)

path = "/Users/sanket/Documents/Sanket/Algo Trade/sky_trading"

# Define an API endpoint
@app.route('/keepAlive', methods=['GET'])
def keepAlive():
    return "I am Alive."

# Four Ways to Enter

@app.route('/DTS/buy', methods=['GET'])
def dayTradinng():
    return start_buy_runner()

@app.route('/DTS/sell', methods=['GET'])
def dayTradinng():
    return start_sell_runner()

@app.route('/DTS/buy_zone', methods=['GET'])
def dayTradinng():
    return start_buy_zone()

@app.route('/DTS/sell_zone', methods=['GET'])
def dayTradinng():
    return start_sell_zone()

# 1 Way to Exit

@app.route('/DTS/exit', methods=['GET'])
def dayTradinng():
    return exit_execute()

# Verification

@app.route('/DTS/verify', methods=['GET'])
def dayTradinng():
    return verification()

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)