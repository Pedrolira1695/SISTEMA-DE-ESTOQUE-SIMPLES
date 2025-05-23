class InventoryItem:
    def __init__(self, item_id, name, quantity):
        self.id = item_id
        self.name = name
        self.quantity = quantity

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity
        }
