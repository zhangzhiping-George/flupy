#from collections import namedtuple
#from abc import ABC, abstractmethod
import inspect

def large_order_promo(order):       
    products = {item.product for item in order.cart}
    if len(products) > 10:
        return order.total() * .07
    return 0

def fidelity_promo(order):
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

def bulkitem_promo(order):
    discount = 0
    for item in order.cart:
        if item.quantity > 10:
            discount += item.total() * .1
    return discount 



