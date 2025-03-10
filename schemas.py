from marshmallow import Schema, fields

# Schema for a basic item with an ID, name, and price.
class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)  # ID is only included in serialized output (not required for input).
    name = fields.Str(required=True)  # Name is required when deserializing input.
    price = fields.Float(required=True)  # Price is required when deserializing input.

# Schema for a basic store with an ID and name.
class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)  # ID is only included in serialized output.
    name = fields.Str()  # Name of the store.

# Extended Item schema that includes store-related fields.
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)  # Store ID is required when loading input, but not included in output.
    store = fields.Nested(PlainStoreSchema(), dump_only=True)  # Store details are included in output but not required for input.
    tags = fields.List(fields.Nested(PlainItemSchema(), dump_only = True))

# Schema for updating an item, where all fields are optional.
class ItemUpdateSchema(Schema):
    name = fields.Str()  # Optional field to update the item's name.
    price = fields.Float()  # Optional field to update the item's price.
    store_id = fields.Int()  # Optional field to update the store association.

    

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


# Extended Store schema that includes a list of items.
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)




class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only = True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)    


class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)    


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)