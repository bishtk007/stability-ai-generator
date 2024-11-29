from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
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

def get_db():
    """Get database session"""
    if 'db' not in st.session_state:
        DATABASE_URL = os.getenv('DATABASE_URL')
        if not DATABASE_URL:
            st.error("Database URL not found in environment variables!")
            st.stop()
            
        try:
            # Create engine and session
            engine = create_engine(DATABASE_URL)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            
            # Create tables
            Base.metadata.create_all(engine)
            
            # Store session in streamlit state
            st.session_state.db = SessionLocal()
            
        except Exception as e:
            st.error(f"Failed to connect to database: {str(e)}")
            st.stop()
    
    return st.session_state.db

def init_db():
    """Initialize database"""
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        st.error("Database URL not found in environment variables!")
        st.stop()
        
    try:
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        return engine
    except Exception as e:
        st.error(f"Failed to initialize database: {str(e)}")
        st.stop()
