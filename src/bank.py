class Bank:
    def __init__(self, starting_budget, comission_function) -> None:
        self.budget = starting_budget
        self.total_transaction_saldo = 0
        self.comission_function = comission_function
        self.products_list = []
        self.comission = 0
    
    def adjust_comission(self):
        self.comission = self.comission_function(self.total_transaction_saldo)
    
    def publish_offer(self, seller, product):
        ...

