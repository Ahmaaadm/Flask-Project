from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema

# Create a Blueprint for store-related operations.
blp = Blueprint("Stores", __name__, description="Operations on stores")


# Define a route for handling individual stores using store_id.
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    # GET request to retrieve a store by its ID.
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)  # Fetch the store or return a 404 error if not found.
        return store  # Return the store in the response.

    # DELETE request to remove a store by its ID.
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)  # Fetch the store or return a 404 error if not found.
        db.session.delete(store)  # Delete the store from the database.
        db.session.commit()  # Commit the transaction.
        return {"message": "Store deleted"}, 200  # Return a success message.


# Define a route for handling a collection of stores.
@blp.route("/store")
class StoreList(MethodView):
    # GET request to retrieve all stores.
    @blp.response(200, StoreSchema(many=True))  # Return a list of stores using StoreSchema.
    def get(self):
        return StoreModel.query.all()  # Fetch and return all stores from the database.

    # POST request to create a new store.
    @blp.arguments(StoreSchema)  # Parse request data based on StoreSchema.
    @blp.response(201, StoreSchema)  # Respond with the created store using StoreSchema.
    def post(self, store_data):
        store = StoreModel(**store_data)  # Create a new store instance.

        try:
            db.session.add(store)  # Add the store to the database session.
            db.session.commit()  # Commit the transaction.
        except IntegrityError:
            # Handle unique constraint violations (e.g., store name already exists).
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            # Handle general database errors.
            abort(500, message="An error occurred creating the store.")

        return store  # Return the created store.
