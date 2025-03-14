import logging.handlers
import os
import secrets
import sys

from flask import Flask, jsonify, redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)

# Configure logging to file
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

# Add console logging so messages still appear in the console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)


class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256), unique=True, nullable=False)


class TodoSchema(Schema):
    id = fields.Integer(dump_only=True)
    task = fields.String(required=True)


class ApiKeySchema(Schema):
    key = fields.String(dump_only=True)


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
apikey_schema = ApiKeySchema()


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


@app.errorhandler(400)
def handle_validation_error(error):
    logger.warning(f"Validation error: {error.description}")
    return jsonify({"message": error.description}), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"message": "Unauthorized"}), 401


@app.errorhandler(500)
def handle_database_error(error):
    logger.error(f"Database error: {error}")
    db.session.rollback()  # Rollback the session to a clean state
    return jsonify({"message": "Internal Server Error"}), 500


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
    try:
        data = todo_schema.load(request.get_json())
    except ValidationError as err:
        abort(400, description=err.messages)  # Use abort with description

    new_todo = Todo(task=data["task"])
    try:
        db.session.add(new_todo)
        db.session.commit()
        logger.info(f"Todo created: {new_todo.id}")
        return todo_schema.dump(new_todo), 201
    except SQLAlchemyError as e:
        logger.exception("Error creating todo:")
        db.session.rollback()
        abort(500)


@app.route("/todos", methods=["GET"])
def get_todos():
    try:
        todos = Todo.query.all()
        logger.info(f"Todos retrieved: {len(todos)}")
        return jsonify(todos_schema.dump(todos)), 200
    except SQLAlchemyError as e:
        logger.exception("Error getting todos:")
        db.session.rollback()
        abort(500)


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    try:
        data = todo_schema.load(request.get_json())
    except ValidationError as err:
        abort(400, description=err.messages)

    try:
        todo = Todo.query.get_or_404(todo_id)
        todo.task = data["task"]
        db.session.commit()
        logger.info(f"Todo updated: {todo_id}")
        return todo_schema.dump(todo), 200
    except SQLAlchemyError as e:
        logger.exception(f"Error updating todo {todo_id}:")
        db.session.rollback()
        abort(500)


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    try:
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        logger.info(f"Todo deleted: {todo_id}")
        return jsonify({"message": "Todo deleted"}), 200
    except SQLAlchemyError as e:
        logger.exception(f"Error deleting todo {todo_id}:")
        db.session.rollback()
        abort(500)


@app.route("/api-keys", methods=["POST"])
def create_api_key():
    try:
        new_key = ApiKey(key=generate_api_key())
        db.session.add(new_key)
        db.session.commit()
        logger.info("API key created")
        return apikey_schema.dump(new_key), 201
    except SQLAlchemyError as e:
        logger.exception("Error creating API key:")
        db.session.rollback()
        abort(500)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
