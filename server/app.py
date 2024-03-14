from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['POST'])
def create_message():
    if request.method == 'POST':
        # Create a new message object from the request data
        new_message = Message(
            body=request.form.get("body"),
            username=request.form.get("username"),
        )

        # Add the new message to the database session
        db.session.add(new_message)

        # Commit the changes to the database
        db.session.commit()
        
        # Convert the new message to a dictionary
        message_dict = new_message.to_dict()

        # Create a response containing the message dictionary
        response = make_response(
            jsonify(message_dict),
            201
        )

        # Return the response
        return response

@app.route('/messages', methods=['GET'])
def get_messages():

    if request.method == 'GET':
        messages = []
        for message in Message.query.all():
            message_dict = message.to_dict()
            messages.append(message_dict)

        response = make_response(
            messages,
            200
        )

        return response

@app.route('/messages/<int:id>')
def get_message_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    message_dict = message.to_dict()

    response = make_response(
        message_dict,
        200
    )

    return response

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    # Get the request data
    data = request.json

    # Find the message with the given ID
    # message = next((m for m in messages if m['id'] == id), None)
    message = Message.query.filter(Message.id == id).first()

    # If message not found, return 404 Not Found
    if message is None:
        return jsonify({'error': 'Message not found'}), 404

    # Update the message with the new data
    if 'body' in data:
        message['body'] = data['body']

    # Return the updated message
    return jsonify(message)

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "message": "Review deleted."
        }
        response = make_response(
            response_body,
            200
        )
        return response

if __name__ == '__main__':
    app.run(port=5555)