
import datetime
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)


class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updateDatetime = db.Column(db.DateTime, default=datetime.datetime.now)

    def json(self):
        return {'id': str(self.id), 'name': self.name, 'description': self.description, 'quantity': self.quantity, 'price': self.price }

db.create_all()


# get all items
@app.route('/items', methods=['GET'])
@cross_origin()
def get_items():
    try:
        items = Item.query.all()
        return make_response(jsonify( [item.json() for item in items]), 200)
        #return make_response(jsonify({'message': 'no items found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'no items found'}), 500)

    
# get a user by id
@app.route('/items/<int:id>', methods=['GET']) 
@cross_origin()
def get_item(id):
    try:
        item = Item.query.filter_by(id=id).first()
        return make_response(jsonify({'item': item.json() }), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting item'}), 500)   


# craete  an item
@app.route('/items', methods=['POST'])
@cross_origin()
def craete_item():
    try:
        data = request.get_json()
        print("data is " + format(data))
        #if data is not None:
        #    return make_response(jsonify({'name': format(data)}), 200)
        #else:
        #    return make_response(jsonify({'message': 'data not found'}), 400)
       
        new_item = Item(name=data['name'], description=data['description'], quantity=data['quantity'], price=data['price'])
        #new_item = Item(name=data['name'], description=data['description'])
        db.session.add(new_item)
        db.session.commit()
        # return make_response(jsonify({'message': 'item created'}), 201)
        items = Item.query.all()
        return make_response(jsonify( [item.json() for item in items]), 200)
    except Exception as e:
        return make_response(jsonify({'message', 'error createing item'}), 500)


# update an item
@app.route('/items/<int:id>', methods=['PUT'])
@cross_origin()
def update_user(id):
    try:
        item = Item.query.filter_by(id=id).first()
        if item:
            data = request.get_json()
            item.name = data['name']
            item.description = data['description']
            item.quantity = data['quantity']
            item.price = data['price']
            db.session.commit()
            return make_response(jsonify({'message': 'item updated'}), 200)
        return make_response(jsonify({'message': 'item not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'error updating item'}), 500)
    
# delete an item
@app.route('/items/<int:id>', methods=['DELETE'])
@cross_origin()
def delete_user(id):
    try:
        item = Item.query.filter_by(id=id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return make_response(jsonify({'message': 'item deleted'}))
        return make_response(jsonify({'message': 'item not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating item'}), 500)
    
