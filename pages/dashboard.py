import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import User, Image, Payment, init_db
from subscription import PLANS

def show_dashboard():
    if 'user' not in st.session_state:
        st.warning("Please login to view your dashboard")
        st.session_state.redirect_to_login = True
        return
        
    # Initialize database
    engine = init_db()
    Session = sessionmaker(bind=engine)
    db = Session()
    
    user = db.query(User).filter(User.id == st.session_state.user.id).first()
    
    st.title("Account Dashboard")
    
    # Custom CSS
    st.markdown("""
    <style>
    .stat-card {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        border: 1px solid #333;
    }
    .stat-value {
        font-size: 24px;
        color: #00BFFF;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # User Info and Stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <h3>Subscription</h3>
            <div class="stat-value">{}</div>
            <div>Valid until: {}</div>
        </div>
        """.format(
            user.subscription_type.title(),
            user.subscription_end.strftime("%Y-%m-%d") if user.subscription_end else "N/A"
        ), unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="stat-card">
            <h3>Credits Remaining</h3>
            <div class="stat-value">{}</div>
            <div>Images available</div>
        </div>
        """.format(user.credits_remaining), unsafe_allow_html=True)
        
    with col3:
        total_images = db.query(Image).filter(Image.user_id == user.id).count()
        st.markdown("""
        <div class="stat-card">
            <h3>Total Images</h3>
            <div class="stat-value">{}</div>
            <div>Generated so far</div>
        </div>
        """.format(total_images), unsafe_allow_html=True)
    
    # Usage Analytics
    st.header("Usage Analytics")
    
    # Get last 30 days of image generation
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    daily_images = db.query(
        func.date(Image.created_at).label('date'),
        func.count(Image.id).label('count')
    ).filter(
        Image.user_id == user.id,
        Image.created_at >= thirty_days_ago
    ).group_by(
        func.date(Image.created_at)
    ).all()
    
    # Create usage graph
    fig = go.Figure()
    dates = [d.date for d in daily_images]
    counts = [d.count for d in daily_images]
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=counts,
        mode='lines+markers',
        name='Images Generated',
        line=dict(color='#00BFFF')
    ))
    
    fig.update_layout(
        title='Daily Image Generation',
        xaxis_title='Date',
        yaxis_title='Images Generated',
        template='plotly_dark',
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent Images
    st.header("Recent Images")
    recent_images = db.query(Image).filter(
        Image.user_id == user.id
    ).order_by(
        Image.created_at.desc()
    ).limit(10).all()
    
    if recent_images:
        image_cols = st.columns(5)
        for idx, image in enumerate(recent_images):
            with image_cols[idx % 5]:
                st.image(image.image_url, caption=f"Created: {image.created_at.strftime('%Y-%m-%d')}")
    else:
        st.info("No images generated yet")
    
    # Billing History
    st.header("Billing History")
    payments = db.query(Payment).filter(
        Payment.user_id == user.id
    ).order_by(
        Payment.created_at.desc()
    ).limit(5).all()
    
    if payments:
        for payment in payments:
            st.markdown(f"""
            <div class="stat-card">
                <h4>${payment.amount:.2f} - {payment.payment_type.title()}</h4>
                <div>Date: {payment.created_at.strftime('%Y-%m-%d %H:%M')}</div>
                <div>Status: {payment.status.title()}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No billing history yet")

if __name__ == "__main__":
    show_dashboard()
