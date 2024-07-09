from sqlalchemy import create_engine, Column, Integer, String, DateTime, DECIMAL, Text, ForeignKey, func , NVARCHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy.sql.schema import UniqueConstraint 
from datetime import datetime
from con import engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from datetime import date
from sqlalchemy.orm import declarative_base

Base = declarative_base()



class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    customer_number = Column(String(255), unique=True, index=True)  # Adjust the length as needed
    customer_name = Column(String)
    address = Column(String)
    category = Column(String)

    invoices = relationship('Invoice', back_populates='customer')  # One-to-many relationship with Invoice

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True)
    invoice_number = Column(String(255), unique=True, index=True)  # Adjust the length as needed
    date = Column(String)
    total = Column(String)
    image_link = Column(String)

    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', back_populates='invoices')

    items = relationship('Item', back_populates='invoice')  # One-to-many relationship with Item

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Float)
    quantity = Column(Float)

    invoice_id = Column(Integer, ForeignKey('invoices.id'))
    invoice = relationship('Invoice', back_populates='items')
    invoice = relationship("Invoice", back_populates="items")



class RequestLog(Base):
    __tablename__ = "request_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    method = Column(String)
    path = Column(String)
    status_code = Column(Integer)

# Create tables in database
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)