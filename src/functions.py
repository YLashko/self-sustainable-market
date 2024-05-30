from enum import Enum

class MarginFunctions(Enum):
    def mul_inverse(x_mul: float = 0.1, hor_shift: float = 0.5, ver_shift: float = 1) -> callable:
        return lambda x: max(1 / (x_mul * x + hor_shift) + ver_shift, 0)

class DemandFunctions(Enum):
    def sqrt_demand(sqrt_pow: float = 0.25, hor_shift: float = 0.25, ver_shift: float = 0.5) -> callable:
        return lambda x: max((x + hor_shift) ** sqrt_pow + ver_shift, 0) if x > 0 else 0

class CommissionFunctions(Enum):
    def exp_commission(exp_pow: float = 1.0005, x_mul: float = 0.02, max_commission: float = 0.5):
        return lambda x: min((x * x_mul) ** exp_pow - (x * x_mul), max_commission)

if __name__ == '__main__':
    a = MarginFunctions.mul_inverse(x_mul = 1) # sanity check
    print(a(3))
    b = DemandFunctions.sqrt_demand()
    print(b(2))
    c = CommissionFunctions.exp_commission()
    for i in range(0, 100, 1):
        print(b(i))
