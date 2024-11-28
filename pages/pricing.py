import streamlit as st
from subscription import PLANS, CREDIT_PACKAGES, SubscriptionManager
import os

def show_pricing_page():
    st.title("Choose Your Plan")
    
    # Custom CSS for pricing cards
    st.markdown("""
    <style>
    .pricing-card {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        border: 1px solid #333;
    }
    .pricing-card:hover {
        border-color: #00BFFF;
    }
    .price {
        font-size: 24px;
        color: #00BFFF;
        margin: 10px 0;
    }
    .feature-list {
        margin: 15px 0;
    }
    .feature-item {
        margin: 5px 0;
        color: #CCC;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Subscription Plans
    st.header("Monthly Subscriptions")
    cols = st.columns(3)
    
    for idx, (plan_id, plan) in enumerate(PLANS.items()):
        with cols[idx]:
            st.markdown(f"""
            <div class="pricing-card">
                <h3>{plan['name']}</h3>
                <div class="price">${plan['price']}/month</div>
                <div class="feature-list">
                    {''.join(f'<div class="feature-item">✓ {feature}</div>' for feature in plan['features'])}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Subscribe to {plan['name']}", key=f"sub_{plan_id}"):
                if 'user' not in st.session_state:
                    st.warning("Please log in first")
                    st.session_state.redirect_to_login = True
                else:
                    try:
                        manager = SubscriptionManager(os.getenv('STRIPE_SECRET_KEY'))
                        session = manager.create_checkout_session(plan_id, st.session_state.user.id)
                        st.markdown(f'<meta http-equiv="refresh" content="0;url={session.url}">', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error creating checkout session: {str(e)}")
    
    # Credit Packages
    st.header("Pay As You Go Credits")
    credit_cols = st.columns(3)
    
    for idx, (package_id, package) in enumerate(CREDIT_PACKAGES.items()):
        with credit_cols[idx]:
            st.markdown(f"""
            <div class="pricing-card">
                <h3>{package['name']}</h3>
                <div class="price">${package['price']}</div>
                <div class="feature-list">
                    <div class="feature-item">✓ {package['credits']} image credits</div>
                    <div class="feature-item">✓ Never expires</div>
                    <div class="feature-item">✓ All styles included</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Buy {package['name']}", key=f"credit_{package_id}"):
                if 'user' not in st.session_state:
                    st.warning("Please log in first")
                    st.session_state.redirect_to_login = True
                else:
                    try:
                        manager = SubscriptionManager(os.getenv('STRIPE_SECRET_KEY'))
                        session = manager.create_credit_checkout(package_id, st.session_state.user.id)
                        st.markdown(f'<meta http-equiv="refresh" content="0;url={session.url}">', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error creating checkout session: {str(e)}")

    # FAQ Section
    st.header("Frequently Asked Questions")
    with st.expander("What's included in each plan?"):
        st.write("""
        Each plan includes:
        - High-quality AI image generation
        - Multiple style options
        - Download in various formats
        - Basic support
        
        Higher tier plans include additional features like higher resolution, priority generation, and commercial licensing.
        """)
        
    with st.expander("How do credits work?"):
        st.write("""
        - Each credit generates one image
        - Credits never expire
        - Can be used with any style or resolution
        - Purchase more credits anytime
        """)
        
    with st.expander("Can I upgrade or downgrade my plan?"):
        st.write("""
        Yes! You can change your plan at any time:
        - Upgrades are effective immediately
        - Downgrades take effect at the end of your billing cycle
        - Unused credits roll over
        """)

if __name__ == "__main__":
    show_pricing_page()
