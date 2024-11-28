import stripe
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import User, Payment

# Subscription Plans
PLANS = {
    'basic': {
        'name': 'Basic Plan',
        'price': 9.99,
        'images_per_month': 100,
        'stripe_price_id': 'price_basic_monthly',
        'features': [
            '100 images/month',
            '1024x1024 resolution',
            'Basic styles',
            'Standard generation speed'
        ]
    },
    'pro': {
        'name': 'Pro Plan',
        'price': 19.99,
        'images_per_month': 300,
        'stripe_price_id': 'price_pro_monthly',
        'features': [
            '300 images/month',
            'All resolutions up to 1536x1536',
            'All style presets',
            'Priority generation',
            'Save favorites'
        ]
    },
    'business': {
        'name': 'Business Plan',
        'price': 49.99,
        'images_per_month': 1000,
        'stripe_price_id': 'price_business_monthly',
        'features': [
            '1000 images/month',
            'All Pro features',
            'Bulk generation',
            'Commercial license',
            'Custom style presets',
            'Priority support'
        ]
    }
}

# Credit Packages
CREDIT_PACKAGES = {
    'small': {
        'name': '10 Credits',
        'credits': 10,
        'price': 2.99,
        'stripe_price_id': 'price_credits_10'
    },
    'medium': {
        'name': '50 Credits',
        'credits': 50,
        'price': 9.99,
        'stripe_price_id': 'price_credits_50'
    },
    'large': {
        'name': '100 Credits',
        'credits': 100,
        'price': 14.99,
        'stripe_price_id': 'price_credits_100'
    }
}

class SubscriptionManager:
    def __init__(self, stripe_secret_key: str):
        stripe.api_key = stripe_secret_key
        
    def create_checkout_session(self, plan_id: str, user_id: int):
        """Create a Stripe checkout session for subscription"""
        plan = PLANS.get(plan_id)
        if not plan:
            raise ValueError("Invalid plan ID")
            
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': plan['stripe_price_id'],
                'quantity': 1,
            }],
            mode='subscription',
            success_url='https://your-domain.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://your-domain.com/cancel',
            client_reference_id=str(user_id)
        )
        return session
        
    def create_credit_checkout(self, package_id: str, user_id: int):
        """Create a Stripe checkout session for credit purchase"""
        package = CREDIT_PACKAGES.get(package_id)
        if not package:
            raise ValueError("Invalid package ID")
            
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': package['stripe_price_id'],
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://your-domain.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://your-domain.com/cancel',
            client_reference_id=str(user_id)
        )
        return session

def update_user_subscription(db: Session, user_id: int, plan_id: str):
    """Update user's subscription status"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
        
    plan = PLANS.get(plan_id)
    if not plan:
        raise ValueError("Invalid plan")
        
    user.subscription_type = plan_id
    user.subscription_end = datetime.utcnow() + timedelta(days=30)
    user.credits_remaining = plan['images_per_month']
    
    payment = Payment(
        user_id=user_id,
        amount=plan['price'],
        payment_type='subscription',
        status='completed'
    )
    
    db.add(payment)
    db.commit()
    
def add_user_credits(db: Session, user_id: int, package_id: str):
    """Add credits to user's account"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
        
    package = CREDIT_PACKAGES.get(package_id)
    if not package:
        raise ValueError("Invalid package")
        
    user.credits_remaining += package['credits']
    
    payment = Payment(
        user_id=user_id,
        amount=package['price'],
        payment_type='credits',
        status='completed'
    )
    
    db.add(payment)
    db.commit()

def check_user_credits(db: Session, user_id: int) -> bool:
    """Check if user has credits available"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
        
    return user.credits_remaining > 0

def deduct_credit(db: Session, user_id: int):
    """Deduct one credit from user's account"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
        
    if user.credits_remaining <= 0:
        raise ValueError("No credits remaining")
        
    user.credits_remaining -= 1
    db.commit()
