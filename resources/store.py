from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field is mandatory"
                        )

    @jwt_required()
    def get(self, name):
        store = StoreModel.get_item_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": "Store not found"}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.get_item_by_name(name):
            return {"message": "Store '{}' already exists".format(name)}, 400

        data = StoreModel.parser.parse_args()
        store = StoreModel(**data)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred!'}

        return store.json(), 201

    def put(self, name):
        data = StoreModel.parser.parse_args()
        store = StoreModel.get_item_by_name(name)
        if store is None:
            store = StoreModel(name, **data)
            return {"message": "item inserted!"}
        else:
            store.price = data["price"]

        store.save_to_db()
        return store.json()

    @jwt_required()
    def delete(self, name):
        store = StoreModel.get_item_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Item succesfully deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
