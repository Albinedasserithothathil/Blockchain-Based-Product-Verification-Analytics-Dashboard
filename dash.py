import streamlit as st
import pandas as pd
import plotly.express as px
import hashlib
from datetime import datetime
from web3 import Web3
import json
from dotenv import load_dotenv
import os

# ------------------ Configuration ------------------
load_dotenv()  # Load environment variables

# Blockchain Configuration
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")  # Your deployed contract address
PROVIDER_URL = os.getenv("POLYGON_RPC")          # Polygon/Mumbai RPC URL
CONTRACT_ABI = json.loads(os.getenv("CONTRACT_ABI"))  # Your contract ABI

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

# ------------------ Custom CSS ------------------
st.markdown("""
<style>
    .header {
        background-color: #3D9970;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .header h1 { color: white; }
    .metric-card {
        border-left: 4px solid #3D9970;
        padding-left: 1rem;
    }
    .verification-success {
        border: 1px solid #3D9970;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .verification-fail {
        border: 1px solid #DC3545;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .blockchain-badge {
        background-color: #6f42c1;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        display: inline-block;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ Helper Functions ------------------
def generate_hash(row):
    """Generate SHA-256 hash of product data"""
    hash_input = (
        str(row['Product Name']) +
        str(row['Category']) +
        str(row['Quantity']) +
        str(row['MRP']) +
        str(row['Manufacturer']) +
        str(row['Manufacturer Address']) +
        str(row['Organic Certifications']) +
        str(row['Batch Number']) +
        str(row['Manufacture Date']) +
        str(row['Expiry Date']) +
        str(row['Arrival Date at Retailer']) +
        str(row['Retailer Name']) +
        str(row['Retailer Address'])
    )
    return hashlib.sha256(hash_input.encode()).hexdigest()

def verify_on_blockchain(batch_number, product_hash):
    """Verify product on blockchain"""
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    try:
        result = contract.functions.verifyProduct(batch_number, product_hash).call()
        return result
    except Exception as e:
        st.error(f"Blockchain verification error: {str(e)}")
        return False

# ------------------ Data Loading ------------------
@st.cache_data
def load_data():
    df = pd.read_excel('organic_india_complete_catalog.xlsx')
    
    # Data processing
    df['Manufacture Date'] = pd.to_datetime(df['Manufacture Date'], errors='coerce')
    df['Expiry Date'] = pd.to_datetime(df['Expiry Date'], errors='coerce')
    df['Arrival Date at Retailer'] = pd.to_datetime(df['Arrival Date at Retailer'], errors='coerce')
    
    # Generate hashes for all products
    df['Calculated Hash'] = df.apply(generate_hash, axis=1)
    
    # Stock status
    df['Numeric Quantity'] = pd.to_numeric(df['Quantity'].astype(str).str.extract(r'(\\d+)')[0], errors='coerce').fillna(0)
    df['Stock Status'] = df['Numeric Quantity'].apply(
        lambda qty: "Out of Stock" if qty <= 0 else "Low Stock" if qty <= 10 else "In Stock"
    )
    
    return df

df = load_data()

# ------------------ Dashboard UI ------------------
st.markdown('<div class="header"><h1>Organic India Product Dashboard <span class="blockchain-badge">Blockchain Verified</span></h1></div>', unsafe_allow_html=True)

# ------------------ Sidebar ------------------
with st.sidebar:
    st.title("Filters")
    search_term = st.text_input("Search by product name")
    
    st.subheader("Blockchain Verification")
    batch_number = st.text_input("Enter Batch Number")
    verify_btn = st.button("Verify on Blockchain")
    
    # Standard filters
    category = st.selectbox("Filter by Category", ["All"] + sorted(df['Category'].dropna().unique()))
    retailer = st.selectbox("Filter by Retailer", ["All"] + sorted(df['Retailer Name'].dropna().unique()))
    stock_status = st.radio("Filter by Stock Status", ["All", "In Stock", "Low Stock", "Out of Stock"])

# ------------------ Apply Filters ------------------
filtered_df = df.copy()
if search_term:
    filtered_df = filtered_df[filtered_df['Product Name'].str.contains(search_term, case=False, na=False)]
if category != "All":
    filtered_df = filtered_df[filtered_df['Category'] == category]
if retailer != "All":
    filtered_df = filtered_df[filtered_df['Retailer Name'] == retailer]
if stock_status != "All":
    filtered_df = filtered_df[filtered_df['Stock Status'] == stock_status]

# ------------------ Blockchain Verification ------------------
if verify_btn and batch_number:
    product = df[df['Batch Number'] == batch_number]
    
    if not product.empty:
        row = product.iloc[0]
        actual_hash = generate_hash(row)
        
        # Verify on blockchain
        blockchain_status = verify_on_blockchain(batch_number, actual_hash)
        
        # Display results
        status_class = "verification-success" if blockchain_status else "verification-fail"
        result_title = "✓ Blockchain Verification Successful!" if blockchain_status else "✗ Verification Failed"
        
        st.markdown(f"""
        <div class="{status_class}">
            <h3>{result_title}</h3>
            <p><strong>Product Name:</strong> {row['Product Name']}</p>
            <p><strong>Batch Number:</strong> {row['Batch Number']}</p>
            <p><strong>Manufacturer:</strong> {row['Manufacturer']}</p>
            <p><strong>Manufacture Date:</strong> {row['Manufacture Date'].strftime('%Y-%m-%d')}</p>
            <p><strong>Expiry Date:</strong> {row['Expiry Date'].strftime('%Y-%m-%d')}</p>
            <hr>
            <p><strong>Blockchain Address:</strong> {CONTRACT_ADDRESS}</p>
            <p><strong>Product Hash:</strong> {actual_hash}</p>
            <p><strong>Network:</strong> Polygon Mainnet</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Batch ID not found in database.")

# ------------------ Dashboard Metrics ------------------
st.header("Inventory Summary")
cols = st.columns(4)
with cols[0]:
    st.metric("Total Products", df["Product Name"].nunique())
with cols[1]:
    st.metric("Categories", df["Category"].nunique())
with cols[2]:
    st.metric("Retailers", df["Retailer Name"].nunique())
with cols[3]:
    st.metric("Blockchain Verified", len(df), help="Products registered on blockchain")

# ------------------ Visualizations ------------------
st.header("Product Analytics")
tab1, tab2, tab3 = st.tabs(["Category Distribution", "Stock Status", "Price Analysis"])

with tab1:
    fig = px.pie(filtered_df, names='Category', title='Products by Category')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = px.bar(
        filtered_df.groupby(['Retailer Name', 'Stock Status']).size().reset_index(name='Count'),
        x='Retailer Name',
        y='Count',
        color='Stock Status',
        title='Inventory Status by Retailer'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    fig = px.box(filtered_df, x='Category', y='MRP', title='Price Distribution by Category')
    st.plotly_chart(fig, use_container_width=True)

# ------------------ Product Data ------------------
st.header("Product Details")
st.dataframe(
    filtered_df[[
        'Product Name', 'Category', 'Batch Number', 'Quantity', 
        'MRP', 'Retailer Name', 'Stock Status'
    ]],
    use_container_width=True,
    hide_index=True
)