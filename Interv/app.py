from flask import Flask, request, jsonify
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes to allow requests from other ports

@app.route('/run_code', methods=['POST'])
def run_code():
    try:
        # Get the Python code sent from the frontend
        code = request.json.get('code')

        # Run the Python code
        result = subprocess.run(
            ['python3', '-c', code],  # Use 'python3' to run Python code
            text=True,
            capture_output=True,
            timeout=10  # Timeout after 10 seconds
        )

        # If there's an error, return stderr (standard error)
        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 400
        else:
            return jsonify({"output": result.stdout}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
