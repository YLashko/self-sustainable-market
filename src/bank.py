class Bank:
    def __init__(self, starting_budget, commission_function) -> None:
        self.budget = starting_budget
        self.total_transaction_saldo = 0
        self.commission_function = commission_function
        self.products_list = []
        self.commission = 0

    def adjust_commission(self):
        self.commission = self.commission_function(self.total_transaction_saldo)

    def publish_offer(self, seller, product):
        self.products_list.append((seller, product))

    def clear_products_list(self):
        self.products_list.clear()

    def update_transactions(self, transaction_amount):
        self.total_transaction_saldo += transaction_amount
        self.adjust_commission()

    def get_commission(self):
        return self.commission
