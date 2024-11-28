import streamlit as st
import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from models import User, init_db
import os

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def show_login_page():
    st.title("Login")
    
    # Initialize database
    engine = init_db()
    Session = sessionmaker(bind=engine)
    db = Session()
    
    # Custom CSS
    st.markdown("""
    <style>
    .auth-form {
        max-width: 400px;
        margin: auto;
        padding: 20px;
        background-color: #1E1E1E;
        border-radius: 10px;
        border: 1px solid #333;
    }
    .auth-header {
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=True):
        st.text_input("Email", key="login_email")
        st.text_input("Password", type="password", key="login_password")
        
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Login")
        with col2:
            if st.form_submit_button("Register"):
                st.session_state.show_register = True
                st.rerun()
    
    if submit:
        user = authenticate_user(db, st.session_state.login_email, st.session_state.login_password)
        if user:
            access_token = create_access_token({"sub": user.email})
            st.session_state.user = user
            st.session_state.token = access_token
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid email or password")

def show_register_page():
    st.title("Register")
    
    # Initialize database
    engine = init_db()
    Session = sessionmaker(bind=engine)
    db = Session()
    
    with st.form("register_form", clear_on_submit=True):
        st.text_input("Email", key="register_email")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Password", type="password", key="register_password")
        with col2:
            st.text_input("Confirm Password", type="password", key="confirm_password")
            
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Register")
        with col2:
            if st.form_submit_button("Back to Login"):
                st.session_state.show_register = False
                st.rerun()
    
    if submit:
        if st.session_state.register_password != st.session_state.confirm_password:
            st.error("Passwords do not match")
            return
            
        # Check if user exists
        existing_user = db.query(User).filter(User.email == st.session_state.register_email).first()
        if existing_user:
            st.error("Email already registered")
            return
            
        # Create new user
        hashed_password = get_password_hash(st.session_state.register_password)
        new_user = User(
            email=st.session_state.register_email,
            password=hashed_password,
            subscription_type="free",
            credits_remaining=3  # Free trial credits
        )
        
        db.add(new_user)
        db.commit()
        
        st.success("Registration successful! Please login.")
        st.session_state.show_register = False
        st.rerun()

def show_auth_page():
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False
        
    if st.session_state.show_register:
        show_register_page()
    else:
        show_login_page()

if __name__ == "__main__":
    show_auth_page()
