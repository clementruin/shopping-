import random

class Goods:
    def __init__(self, price, color):
        self.price = price
        self.price = color
        self.color = color
        self.size = size

class Carpet(Goods):
    pass

class Moket(Goods):
    def __init__(self, size, m2_price):
        self.size = size
        self.m2_price = m2_price

    @property
    def total_price(self):
        return size*m2_price


class Shop:
    def __init__(self, name, stock, cash):
        self.name = name
        self.stock = stock
        self.cash = cash
        self.gain = 0
        self.items_sold = 0

    def deliver(self, items_number):
        if self.stock - items_number < 0:
            print("Empty stocks, sorry")
        else:
            self.stock -= items_number
            self.items_sold += items_number

    def credit(self, amount):
        self.cash += amount
        self.gain += amount

    def state(self):
        print("{} :: {} items sold | gain : ${} | treasury : ${}".format(
            self.name, self.items_sold, self.gain, self.cash))


class Customer:
    def __init__(self, name, cash):
        self.name = name
        self.cash = cash
        self.expense = 0
        self.items = 0

    def debit(self, amount):
        if self.cash - amount < 0:
            print(self.name,": Not enough cash")
        else:
            self.cash -= amount
            self.expense += amount

    def state(self):
        print("{} :: {} items bought | expenses : ${} | money left : ${}".format(
            self.name, self.items, self.expense, self.cash))


class Transaction:
    def __init__(
            self,
            code,
            customer,
            shop,
            amount,
            items_number,
            hour,
            minute):
        self.customer = customer
        self.shop = shop
        self.amount = amount
        self.items_number = items_number
        self.hour = hour
        self.minute = minute
        self.id = code

    def do(self):
        self.shop.deliver(self.items_number)
        self.customer.debit(self.amount)
        self.shop.credit(self.amount)
        self.customer.items += self.items_number
        print(
            "{} : {} bought {} items in {} for ${}".format(
                self.id,
                self.customer.name,
                self.items_number,
                self.shop.name,
                self.amount))


customers = [
    Customer("Aly", 50),
    Customer("Bat", 500),
    Customer("Ced", 250),
    Customer("Deni", 350),
    Customer("Elo", 150),
    Customer("Fop", 50),
    Customer("Gil", 250),
    Customer("Haas", 75),
    Customer("Ive", 150),
    Customer("Jac", 100),
    Customer("Kyl", 100)
]


def main():
    shop1 = Shop("HappyTapis", 250, 245)
    shop2 = Shop("LuxusCarpet", 130, 900)
    event_p = 0.04
    opening = 8
    closure = 19

    for h in range(opening, closure):
        for m in range(61):
            if random.random() < event_p:
                customer = random.choice(customers)
                shop = random.choice([shop1, shop2])
                amount = random.randint(10, 40)
                items_number = random.randint(1, 3)
                time = random.uniform(8.00, 19.00)
                tr = Transaction(
                    "transaction_at_{}:{}".format(
                        h, m), customer, shop, amount, items_number, h, m)
                tr.do()

    print("\nSUMMARY\n")
    shop1.state()
    shop2.state()
    for c in customers:
        c.state()


main()
