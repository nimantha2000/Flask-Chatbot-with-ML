from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from chat import get_response
import logging

app = Flask(__name__)

# Enable error logging
logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(filename="error.log", level=logging.ERROR)

# Configure rate limiting
limiter = Limiter(
    app,
    default_limits=["5 per minute"],  # Adjust the rate limit as needed
)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.route("/predict", methods=["POST"])
@limiter.limit("5 per minute")  # Adjust the rate limit as needed
def predict():
    try:
        data = request.json
        message = data.get("message")

        if not message:
            return jsonify({"error": "Invalid input"}), 400

        response = get_response(message)

        if response is None:
            app.logger.error("No response found for input: %s", message)
            return jsonify({"error": "Internal Server Error"}), 500

        return jsonify({"answer": response})

    except Exception as e:
        app.logger.exception("An error occurred during request processing: %s", str(e))
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/")
def index():
    return render_template("base.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
