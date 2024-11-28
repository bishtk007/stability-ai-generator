from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    subscription_type = Column(String)  # 'basic', 'pro', 'business', 'pay_as_you_go'
    subscription_end = Column(DateTime)
    credits_remaining = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    images = relationship("Image", back_populates="user")
    payments = relationship("Payment", back_populates="user")

class Image(Base):
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    prompt = Column(String)
    negative_prompt = Column(String)
    style = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="images")

class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    payment_type = Column(String)  # 'subscription' or 'credits'
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="payments")

# Create database and tables
def init_db():
    engine = create_engine('sqlite:///ai_art_generator.db')
    Base.metadata.create_all(engine)
    return engine