from flask import Flask, jsonify, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('health_check'))

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')