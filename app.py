import logging.handlers
import os
import secrets

from flask import Flask, jsonify, redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)

# Configure logging
log_file = "app.log"
log_handler = logging.handlers.RotatingFileHandler(
    log_file, maxBytes=1024 * 1024, backupCount=5
)
log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)


class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256), unique=True, nullable=False)


def generate_api_key():
    return secrets.token_hex(128)


def verify_api_key(api_key):
    return ApiKey.query.filter_by(key=api_key).first()


with app.app_context():
    db.create_all()


@app.before_request
def authenticate():
    if request.path.startswith("/todos"):
        api_key = request.headers.get("Authorization")
        if not api_key or not verify_api_key(api_key):
            logger.warning(f"Unauthorized access attempt: {request.remote_addr}")
            abort(401)


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"message": "Unauthorized"}), 401


@app.route("/", methods=["GET"])
def root():
    logger.info("Root endpoint accessed")
    return redirect(url_for("health_check"))


@app.route("/health", methods=["GET"])
def health_check():
    logger.info("Health check endpoint accessed")
    return jsonify({"status": "ok"}), 200


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    new_todo = Todo(task=data["task"])
    db.session.add(new_todo)
    db.session.commit()
    logger.info(f"Todo created: {new_todo.id}")
    return jsonify({"message": "Todo created"}), 201


@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    todo_list = [{"id": todo.id, "task": todo.task} for todo in todos]
    logger.info(f"Todos retrieved: {len(todo_list)}")
    return jsonify({"todos": todo_list}), 200


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()
    todo = Todo.query.get_or_404(todo_id)
    todo.task = data["task"]
    db.session.commit()
    logger.info(f"Todo updated: {todo_id}")
    return jsonify({"message": "Todo updated"}), 200


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    logger.info(f"Todo deleted: {todo_id}")
    return jsonify({"message": "Todo deleted"}), 200


@app.route("/api-keys", methods=["POST"])
def create_api_key():
    new_key = ApiKey(key=generate_api_key())
    db.session.add(new_key)
    db.session.commit()
    logger.info("API key created")
    return jsonify({"api_key": new_key.key}), 201


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
