from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import asc, desc

from models import db, Message

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

cors = CORS()
migrate = Migrate(app, db)

db.init_app(app)
cors.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        m_list = []
        messages = Message.query.order_by(asc('created_at'))
        for message in messages:
            m_list.append(message.to_dict())
        return make_response(m_list, 200)
    elif request.method == 'POST':
        data = json.loads(request.data)
        new_message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(new_message)
        db.session.commit()

        return make_response(new_message.to_dict(), 201)

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = db.session.get(Message, id)
    if request.method == 'GET':
        response = message.to_dict()
        status = 200
    elif request.method == 'PATCH':
        data = json.loads(request.data)
        for key in data:
            setattr(message, key, data[key])
        db.session.add(message)
        db.session.commit()
        response = message.to_dict()
        status = 200
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response = {}
        status = 204
    return make_response(response, status)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
