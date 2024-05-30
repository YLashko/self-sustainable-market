from product import Product


class Seller:
    def __init__(self, name, production_product, starting_budget, production_speed, demand_product, margin_function,
                 demand_function, bank, starting_demand: float = 10) -> None:
        self.name = name
        self.product: Product = production_product
        self.budget = starting_budget
        self.production_speed = production_speed
        self.demand_product = demand_product
        self.margin_function = margin_function
        self.demand_function = demand_function
        self.current_demand = starting_demand
        self.bank = bank
        self.amount_cumulated = 0

    def produce(self):
        self.amount_cumulated += self.production_speed
        self.product.set_amount(self.amount_cumulated)

    def production_product_adjust_price(self):
        self.product.set_margin_multiplier(self.margin_function(self.amount_cumulated))

    def demand_product_adjust_price(self):
        self.demand_product.set_margin_multiplier(self.demand_function(self.current_demand))

    def try_to_buy(self, product_list):
        total_cost = 0
        for seller, product in product_list:
            if seller != self and product.amount > 0:
                quantity_to_buy = min(self.current_demand, product.amount)
                cost = quantity_to_buy * product.price
                if self.budget >= cost:
                    product.decrease_amount(quantity_to_buy)
                    self.budget -= cost
                    self.current_demand -= quantity_to_buy
                    self.bank.update_transactions(cost)
                    total_cost += cost
        return total_cost

    def publish_offer(self):
        self.bank.publish_offer(self, self.product)
