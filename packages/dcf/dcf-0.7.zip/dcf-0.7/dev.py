from tabulate import tabulate
from dcf import CashRateCurve, RateCashFlowList, get_basis_point_value


curve = CashRateCurve([1, 2], [0.1, 0.2], forward_tenor=3/12)
shift = CashRateCurve([0], [0.01], forward_tenor=3/12)
shifted = curve + shift
print(tabulate(shifted.table, headers='firstrow'))


cf = RateCashFlowList([1], [100], origin=0, forward_curve=curve)
print(tabulate(cf.table, headers='firstrow'))
print(get_basis_point_value(cf, curve, 0.0, curve))
