from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import User, Image, Payment
import pandas as pd
import plotly.express as px

class Analytics:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_stats(self, user_id: int) -> dict:
        """Get basic stats for a user"""
        user = self.db.query(User).filter(User.id == user_id).first()
        total_images = self.db.query(Image).filter(Image.user_id == user_id).count()
        total_spent = self.db.query(func.sum(Payment.amount)).filter(
            Payment.user_id == user_id,
            Payment.status == 'completed'
        ).scalar() or 0
        
        return {
            'subscription': user.subscription_type,
            'credits_remaining': user.credits_remaining,
            'total_images': total_images,
            'total_spent': total_spent
        }
    
    def get_daily_usage(self, user_id: int, days: int = 30) -> list:
        """Get daily image generation stats"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        daily_stats = self.db.query(
            func.date(Image.created_at).label('date'),
            func.count(Image.id).label('count')
        ).filter(
            Image.user_id == user_id,
            Image.created_at >= start_date
        ).group_by(
            func.date(Image.created_at)
        ).all()
        
        return daily_stats
    
    def get_style_distribution(self, user_id: int) -> dict:
        """Get distribution of styles used"""
        styles = self.db.query(
            Image.style,
            func.count(Image.id).label('count')
        ).filter(
            Image.user_id == user_id
        ).group_by(
            Image.style
        ).all()
        
        return {style: count for style, count in styles}
    
    def get_resolution_stats(self, user_id: int) -> dict:
        """Get statistics about image resolutions used"""
        resolutions = self.db.query(
            Image.width,
            Image.height,
            func.count(Image.id).label('count')
        ).filter(
            Image.user_id == user_id
        ).group_by(
            Image.width,
            Image.height
        ).all()
        
        return {f"{width}x{height}": count for width, height, count in resolutions}
    
    def get_payment_history(self, user_id: int) -> list:
        """Get user's payment history"""
        payments = self.db.query(Payment).filter(
            Payment.user_id == user_id
        ).order_by(
            Payment.created_at.desc()
        ).all()
        
        return payments
    
    def generate_usage_report(self, user_id: int) -> dict:
        """Generate a comprehensive usage report"""
        stats = self.get_user_stats(user_id)
        daily_usage = self.get_daily_usage(user_id)
        style_dist = self.get_style_distribution(user_id)
        resolution_stats = self.get_resolution_stats(user_id)
        
        # Create daily usage graph
        usage_df = pd.DataFrame(daily_usage)
        if not usage_df.empty:
            fig = px.line(
                usage_df,
                x='date',
                y='count',
                title='Daily Image Generation'
            )
            fig.update_layout(template='plotly_dark')
        else:
            fig = None
        
        return {
            'basic_stats': stats,
            'style_distribution': style_dist,
            'resolution_stats': resolution_stats,
            'usage_graph': fig
        }
    
    def track_image_generation(self, user_id: int, prompt: str, style: str,
                             width: int, height: int, image_url: str):
        """Track a new image generation"""
        new_image = Image(
            user_id=user_id,
            prompt=prompt,
            style=style,
            width=width,
            height=height,
            image_url=image_url,
            created_at=datetime.utcnow()
        )
        
        self.db.add(new_image)
        self.db.commit()
    
    def track_payment(self, user_id: int, amount: float, payment_type: str):
        """Track a new payment"""
        new_payment = Payment(
            user_id=user_id,
            amount=amount,
            payment_type=payment_type,
            status='completed',
            created_at=datetime.utcnow()
        )
        
        self.db.add(new_payment)
        self.db.commit()
