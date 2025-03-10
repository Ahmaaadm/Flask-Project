from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt


from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

# Create a Blueprint for item-related operations.
blp = Blueprint("Items", __name__, description="Operations on items")


# Define a route for handling individual items using item_id.
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    # GET request to retrieve an item by its ID.
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)  # Fetch the item or return a 404 error if not found.
        return item  # Return the item in the response.

    # DELETE request to remove an item by its ID.
    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        item = ItemModel.query.get_or_404(item_id)  # Fetch the item or return a 404 error if not found.
        db.session.delete(item)  # Delete the item from the database.
        db.session.commit()  # Commit the transaction.
        return {"message": "Item deleted."}  # Return a success message.

    # PUT request to update an existing item or create a new one if it doesn't exist.
    @blp.arguments(ItemUpdateSchema)  # Parse request data based on ItemUpdateSchema.
    @blp.response(200, ItemSchema)  # Respond with the updated item using ItemSchema.
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)  # Try to fetch the item by ID.

        if item:
            # Update existing item fields.
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            # Create a new item if it doesn't exist.
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)  # Add the item to the session.
        db.session.commit()  # Commit the transaction.

        return item  # Return the updated or newly created item.


# Define a route for handling a collection of items.
@blp.route("/item")
class ItemList(MethodView):
    # GET request to retrieve all items.
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))  # Return a list of items using ItemSchema.
    def get(self):
        return ItemModel.query.all()  # Fetch and return all items from the database.

    # POST request to create a new item.
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)  # Parse request data based on ItemSchema.
    @blp.response(201, ItemSchema)  # Respond with the created item using ItemSchema.
    def post(self, item_data):
        item = ItemModel(**item_data)  # Create a new item instance.

        try:
            db.session.add(item)  # Add the item to the database session.
            db.session.commit()  # Commit the transaction.
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")  # Handle database errors.

        return item  # Return the created item.
