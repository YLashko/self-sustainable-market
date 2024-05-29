class Product:
    def __init__(self, name, production_cost, is_luxury, starting_amount) -> None:
        self.name = name
        self.production_cost = production_cost
        self.is_luxury = is_luxury
        self.amount = starting_amount

    def set_margin_multiplier(self, margin_multiplier):
        self.price = self.production_cost * margin_multiplier

    def get_sell_margin(self, sell_price):
        return sell_price - self.production_cost
    
    def set_amount(self, amount):
        self.amount = amount
