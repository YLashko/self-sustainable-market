from seller import Seller
from product import Product
from bank import Bank
from functions import MarginFunctions, DemandFunctions, CommissionFunctions

class Market:
    def __init__(self, sellers, bank):
        self.sellers: list[Seller] = sellers
        self.bank: Bank = bank
        self.day = 0
        self.previous_total_transaction_saldo = 0
        self.previous_income = 0
        self.avg_product_price = 100

    def simulate_day(self, day_count):
        self.day += 1

        # Step 1: Production phase
        for seller in self.sellers:
            seller.produce()
            seller.consume_cumulated()
            seller.production_product_adjust_price()
            seller.demand_product_adjust_price()

        # Step 2: Publish offers
        self.bank.clear_products_list()
        for seller in self.sellers:
            seller.publish_offer()

        # Step 3: Buying phase
        for seller in self.sellers:
            seller.try_to_buy(self.bank.products_list)

        total_saldo = self.bank.total_transaction_saldo

        # Step 4: Adjust inflation
        self.bank.adjust_commission()
        self.bank.reset_transactions_saldo()

        # Step 5: Bank possible grant
        if day_count % 10 == 0:
            min_budget_seller = self.sellers[0]
            for idx, seller in enumerate(self.sellers):
                if seller.budget < min_budget_seller.budget:
                    min_budget_seller = seller
            self.bank.give_grant(min_budget_seller, 0.2)

        # Calculate differences and print results
        # TODO: rewrite this mess
        if self.day == 1:
            difference = 0
        else:
            difference = total_saldo - self.previous_income
        self.previous_income = total_saldo
        inflation = self.bank.get_commission()
        budget = self.bank.budget
        prev_avg_product_price = self.avg_product_price
        self.avg_product_price = sum([seller.product.price for seller in self.sellers]) / len(self.sellers)
        inflation = self.avg_product_price / prev_avg_product_price

        print(f"DAY {self.day} | Transaction saldo: {total_saldo:.2f}\t | Difference: {difference:.2f}\t | Comission: {inflation:.4f}\t | Budget: {budget:.4f}\t | Inflation: {(inflation - 1) * 100:.2f}%")
        # print("".join([str(seller.budget) + "\t" for seller in self.sellers]))

    def run_simulation(self, days):
        for day in range(days):
            self.simulate_day(day)

if __name__ == '__main__':
    bank = Bank(10000, CommissionFunctions.exp_commission())
    sellers = [
        Seller("Seller1", Product("Necessity", 10, False, 10), 5000, 5, Product("Luxury", 50, True, 0), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank, 10, 15),
        Seller("Seller2", Product("Necessity", 7, False, 7), 1000, 4, Product("Luxury", 55, True, 0), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank, 10, 15),
        Seller("Seller3", Product("Luxury", 50, True, 5), 1600, 4, Product("Necessity", 13, False, 0), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank),
        Seller("Seller4", Product("Necessity", 12, False, 5), 2000, 4, Product("Luxury", 55, True, 0), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank, 10, 15),
        Seller("Seller5", Product("Luxury", 50, True, 6), 2600, 4, Product("Necessity", 10, False, 0), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank),
        Seller("Seller6", Product("Necessity", 12, False, 2), 1600, 4, Product("Luxury", 55, True, 0), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank, 10, 15),
        Seller("Seller7", Product("Luxury", 46, True, 5), 2600, 4, Product("Necessity", 9, False, 0), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank)
    ]

    market = Market(sellers, bank)
    market.run_simulation(500)

