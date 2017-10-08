# Transaction

import sqlalchemy
import csv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)

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

new_transaction = TransactionTable(
    customer='Kyl',
    shop='HappyTapis',
    c_items=3,
    m_size=12,
    amount=60)
new_transaction2 = TransactionTable(
    customer='Ive',
    shop='HappyTapis',
    c_items=3,
    m_size=12,
    amount=60)

Session = sessionmaker(bind=engine)
session = Session()

session.add(new_transaction)
session.add(new_transaction2)
# session.commit()

for instance in session.query(TransactionTable).order_by(TransactionTable.id):
    print("\n", instance.shop)

outfile = open('mydump.csv', 'w')
outcsv = csv.writer(outfile)
records = session.query(TransactionTable).all()
[outcsv.writerow([getattr(curr, column.name)
                  for column in TransactionTable.__mapper__.columns]) for curr in records]
print(Base.metadata.tables.keys())
outfile.close()

session.commit()
