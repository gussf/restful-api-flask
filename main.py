from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from secret import auth, identity

app = Flask(__name__)
app.secret_key = 'gustavo'
api = Api(app)
items = []

jwt = JWT(app, authentication_handler=auth, identity_handler=identity) # /auth

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item =  next(filter(lambda x: x['name'] == name, items), None)
        return {'item' : item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f'An item with name {name} already exists'}, 400

        data = request.get_json()
        item = {'name':data['name'], 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return '', 204


    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x: x['name'] != name, items), None)
        if item:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items/')


app.run(port=5000, debug=True)


