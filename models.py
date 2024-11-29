from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    subscription_type = Column(String, default='free')  # 'free', 'basic', 'pro', 'business', 'pay_as_you_go'
    subscription_end = Column(DateTime, nullable=True)
    credits_remaining = Column(Integer, default=3)  # Start with 3 free credits
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    images = relationship("Image", back_populates="user")
    payments = relationship("Payment", back_populates="user")

class Image(Base):
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    prompt = Column(String)
    negative_prompt = Column(String, nullable=True)
    style = Column(String, nullable=True)
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

def init_db():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        # Fallback to SQLite for local development
        DATABASE_URL = 'sqlite:///ai_art_generator.db'
    
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    return engine
