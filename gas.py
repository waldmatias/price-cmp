#!/usr/bin/env python
import sys

def calculate_gas_cost(km_to_travel):
    car_autonomy = 5 #l x km
    gas_cost = .5 # usd x l
    return (km_to_travel / car_autonomy) * gas_cost


if __name__ == '__main__':
    if sys.argv[1] and sys.argv[2]:
        km_to_travel = float(sys.argv[1])
        cost_usd = calculate_gas_cost(km_to_travel)
        exch = float(sys.argv[2])
        print(f'cost for {km_to_travel}km is {cost_usd} USD')
        print(f'{cost_usd * (exch*1000):,.2f} Bs.')
