from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field is mandatory"
                        )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field is mandatory"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Item needs a store id"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            return item.json()
        else:
            return {"message": "item not found"}

    @jwt_required()
    def post(self, name):
        if ItemModel.get_item_by_name(name):
            return {"message": "item already exists"}

        data = Item.parser.parse_args()
        new_item = ItemModel(**data)
        new_item.save_to_db()
        return {"message": "item inserted!"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.get_item_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
            return {"message": "item inserted!"}
        else:
            item.price = data["price"]

        item.save_to_db()
        return item.json()

    @jwt_required()
    def delete(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item succesfully deleted'}


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
