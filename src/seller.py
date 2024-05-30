from product import Product


class Seller:
    def __init__(self, name, production_product, starting_budget, production_speed, demand_product, margin_function,
                 demand_function, bank, starting_demand: float = 10, consume_speed: float = 40) -> None:
        self.name = name
        self.product: Product = production_product
        self.budget = starting_budget
        self.production_speed = production_speed
        self.demand_product: Product = demand_product
        self.margin_function = margin_function
        self.demand_function = demand_function
        self.bank = bank
        self.consume_speed = consume_speed

    def produce(self): 
        self.product.amount += self.production_speed
    
    def consume_cumulated(self):
        self.demand_product.amount += self.consume_speed

    def production_product_adjust_price(self):
        self.product.set_margin_multiplier(self.margin_function(self.product.amount))

    def demand_product_adjust_price(self):
        self.demand_product.set_margin_multiplier(self.demand_function(self.demand_product.amount))

    # def try_to_buy(self, product_list):
    #     total_cost = 0
    #     for seller, product in product_list:
    #         if seller != self and product.amount > 0:
    #             quantity_to_buy = min(self.current_demand, product.amount)
    #             cost = quantity_to_buy * product.price
    #             if self.budget >= cost:
    #                 product.decrease_amount(quantity_to_buy)
    #                 self.budget -= cost
    #                 self.current_demand -= quantity_to_buy
    #                 self.bank.update_transactions(cost)
    #                 total_cost += cost
    #     return total_cost

    def try_to_buy(self, product_list):
        chosen_seller = None

        for seller, product in product_list:
            # print(f"My proposition: {self.demand_product.price}, their proposition: {product.price}")
            # print(f"{product.price} <= {self.demand_product.price}")
            if seller != self and product.name == self.demand_product.name and product.price <= self.demand_product.price:
                chosen_seller = seller

        if chosen_seller is None:
            return
        
        # print("seller chosen")

        for seller, product in product_list:
            if seller != self \
                and product.amount > 0 \
                and product.name == self.demand_product.name \
                and product.price <= self.demand_product.price \
                and product.price < chosen_seller.product.price:

                chosen_seller = seller

        self.bank.process_transaction(chosen_seller, self)

    def publish_offer(self):
        self.bank.publish_offer(self, self.product)
