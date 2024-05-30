from seller import Seller
from product import Product
from bank import Bank
from functions import MarginFunctions, DemandFunctions, CommissionFunctions

class Market:
    def __init__(self, sellers, bank):
        self.sellers = sellers
        self.bank = bank
        self.day = 0
        self.previous_total_transaction_saldo = 0
        self.previous_income = 0

    def simulate_day(self):
        self.day += 1
        total_income = 0

        # Step 1: Production phase
        for seller in self.sellers:
            seller.produce()
            seller.production_product_adjust_price()

        # Step 2: Publish offers
        self.bank.clear_products_list()
        for seller in self.sellers:
            seller.publish_offer()

        # Step 3: Buying phase
        for seller in self.sellers:
            income = seller.try_to_buy(self.bank.products_list)
            total_income += income

        # Step 4: Adjust inflation
        self.bank.adjust_commission()

        # Calculate differences and print results
        if self.day == 1:
            difference = 0
        else:
            difference = total_income - self.previous_income
        self.previous_income = total_income
        inflation = self.bank.get_commission()
        print(f"DAY {self.day} | Income: {total_income:.2f} | Difference: {difference:.2f} | Inflation: {inflation:.4f}")

    def run_simulation(self, days):
        for _ in range(days):
            self.simulate_day()

if __name__ == '__main__':
    bank = Bank(100000, CommissionFunctions.exp_commission())
    sellers = [
        Seller("Seller1", Product("Necessity", 10, False, 100), 500, 5, Product("Luxury", 50, True, 50), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank),
        Seller("Seller2", Product("Necessity", 7, False, 100), 100, 4, Product("Luxury", 55, True, 60), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank),
        Seller("Seller3", Product("Necessity", 3, True, 200), 1600, 4, Product("Luxury", 55, True, 60), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank),
        Seller("Seller4", Product("Necessity", 12, False, 1000), 10600, 4, Product("Luxury", 55, True, 60), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank),
        Seller("Seller5", Product("Necessity", 4, True, 500), 2600, 4, Product("Luxury", 55, True, 60), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank),
        Seller("Seller6", Product("Necessity", 12, False, 100), 2600, 4, Product("Luxury", 55, True, 60), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank),
        Seller("Seller7", Product("Necessity", 8, True, 300), 45600, 4, Product("Luxury", 55, True, 60), MarginFunctions.mul_inverse(), DemandFunctions.sqrt_demand(), bank)
    ]

    market = Market(sellers, bank)
    market.run_simulation(30)

