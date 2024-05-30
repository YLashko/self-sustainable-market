class Bank:
    def __init__(self, starting_budget, commission_function) -> None:
        self.budget = starting_budget
        self.total_transaction_saldo = 0
        self.commission_function = commission_function
        self.products_list = []
        self.commission = 0

    def adjust_commission(self):
        self.commission = self.commission_function(self.total_transaction_saldo)

    def reset_transactions_saldo(self):
        self.total_transaction_saldo = 0

    def publish_offer(self, seller, product):
        self.products_list.append((seller, product))

    def clear_products_list(self):
        self.products_list.clear()
    
    def give_grant(self, seller, portion):
        seller.budget += self.budget * portion
        self.budget -= self.budget * portion
    
    def process_transaction(self, seller, buyer):
        chosen_product = seller.product

        buy_price = min(chosen_product.price * chosen_product.amount * (1 + self.commission),
                        self.budget / (1 + self.commission))
        
        buy_amount = buy_price / chosen_product.price / (1 + self.commission)

        if buy_price > buyer.budget:
            return

        chosen_product.amount -= buy_amount
        buyer.demand_product.amount -= buy_amount
        seller.budget += buy_price / (1 + self.commission)
        buyer.budget -= buy_price / (1 + self.commission)
        self.budget += buy_price * self.commission

        self.update_transactions_saldo(buy_price)

    def update_transactions_saldo(self, transaction_amount):
        self.total_transaction_saldo += transaction_amount

    def get_commission(self):
        return self.commission
