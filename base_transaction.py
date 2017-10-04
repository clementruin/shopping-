# Transaction 

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()

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


<<<<<<< HEAD
#new_transaction = TransactionTable(customer='Kyl', shop='HappyTapis', c_items=3, m_size=12, amount=60)
>>>>>>> 662481e64503b31b58edc8cda309d1adf38fbeef

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

session.add(new_request)
<<<<<<< HEAD
#session.commit()

#for instance in session.query(Request).order_by(Request.id):
#	print("\n", instance.id, instance.title, instance.description)
=======
#session.add_all([Request(title=title, description=description)])
#session.commit()

>>>>>>> 662481e64503b31b58edc8cda309d1adf38fbeef



