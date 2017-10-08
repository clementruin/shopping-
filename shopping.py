import random
import sqlalchemy
import csv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Goods:
    def __init__(self, price, color):
        self.price = price
        self.color = color
        self.size = size


class Carpet(Goods):
    def __init__(self, price, color):
        self.price = price
        self.color = color
    pass


class Moket(Goods):
    def __init__(self, size):
        self.size = size
        self.m2_price = 2

    @property
    def total_price(self):
        return self.size * self.m2_price


class Shop:
    def __init__(self, name, c_stock, m_stock, cash):
        self.name = name
        self.c_stock = c_stock
        self.m_stock = m_stock
        self.cash = cash
        self.gain = 0
        self.c_items_sold = 0
        self.m_size_sold = 0

    def deliver(self, c_items_number, m_size):
        if self.c_stock - c_items_number < 0:
            print("Empty carpet stocks, sorry")
        elif self.m_stock - m_size < 0:  # elif ??
            print("Empty moket stocks, sorry")
        else:
            self.c_stock -= c_items_number
            self.m_stock -= m_size
            self.c_items_sold += c_items_number
            self.m_size_sold += m_size

    def credit(self, amount):
        self.cash += amount
        self.gain += amount

    def state(self):
        print(
            "{} :: {} carpet sold | {} square meter moket sold | gain : ${} | treasury : ${}".format(
                self.name,
                self.c_items_sold,
                self.m_size_sold,
                self.gain,
                self.cash))


class Customer:
    def __init__(self, name, cash):
        self.name = name
        self.cash = cash
        self.expense = 0
        self.c_items = 0
        self.m_size = 0

    def is_solvent(self, amount):
        return self.cash >= amount

    def debit(self, amount):
        if self.cash - amount < 0:
            print(self.name, ": Not enough cash")
        else:
            self.cash -= amount
            self.expense += amount

    def state(self):
        print(
            "{} :: {} carpet bought | {} square meter moket bought | expenses : ${} | money left : ${}".format(
                self.name,
                self.c_items,
                self.m_size,
                self.expense,
                self.cash))


class Transaction:
    def __init__(
            self,
            code,
            customer,
            shop,
            m_size,
            c_items_number,
            hour,
            minute,
            carpet,
            moket):
        self.amount = c_items_number * carpet.price + m_size * moket.m2_price
        self.customer = customer
        self.shop = shop
        self.c_items_number = c_items_number
        self.m_size = m_size
        self.hour = hour
        self.minute = minute
        self.id = code

    def do(self):
        if self.customer.is_solvent(self.amount):
            self.shop.deliver(self.c_items_number, self.m_size)
            self.customer.debit(self.amount)
            self.shop.credit(self.amount)
            self.customer.c_items += self.c_items_number
            self.customer.m_size += self.m_size
            new_transaction = TransactionTable(
                customer=self.customer.name,
                shop=self.shop.name,
                c_items=self.c_items_number,
                m_size=self.m_size,
                amount=self.amount)
            session.add(new_transaction)
            print(
                "{} : {} bought {} carpet(s) and {} m2 moket in {} for ${}".format(
                    self.id,
                    self.customer.name,
                    self.c_items_number,
                    self.m_size,
                    self.shop.name,
                    self.amount))


class TransactionTable(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    customer = Column(String)
    shop = Column(String)
    c_items = Column(Integer)
    m_size = Column(Integer)
    amount = Column(Integer)

    def __repr__(self):
        return "<TransactionTable(customer='%s', shop='%s', c_items='%s', m_size='%s', amount='%s')>" % (
            self.customer, self.shop, self.c_items, self.m_size, self.amount)


Base.metadata.create_all(engine)

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
    shop1 = Shop("HappyTapis", 250, 240, 245)
    shop2 = Shop("LuxusCarpet", 130, 420, 900)
    carpet = Carpet(12, 'blue')
    event_p = 0.04
    opening = 8
    closure = 19

    for h in range(opening, closure):
        for m in range(61):
            if random.random() < event_p:
                customer = random.choice(customers)
                shop = random.choice([shop1, shop2])
                m_size = random.randint(10, 40)
                moket = Moket(m_size)
                c_items_number = random.randint(1, 3)
                time = random.uniform(8.00, 19.00)
                tr = Transaction(
                    "transaction_at_{}:{}".format(
                        h,
                        m),
                    customer,
                    shop,
                    m_size,
                    c_items_number,
                    h,
                    m,
                    carpet,
                    moket)
                tr.do()

    print("\nSUMMARY\n")
    shop1.state()
    shop2.state()
    for c in customers:
        c.state()

    print(session.query(TransactionTable).count())
    records = session.query(TransactionTable).all()
    session.commit()
    outfile = open('static/mydump.csv', 'w')
    outcsv = csv.writer(outfile)
    outcsv.writerow(['id', 'customer', 'shop',
                     'carpets_nb', 'moket_size', 'amount'])
    [outcsv.writerow([getattr(curr, column.name)
                      for column in TransactionTable.__mapper__.columns]) for curr in records]
    outfile.close()


main()
