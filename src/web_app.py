import streamlit as st
import pandas as pd
import os
import sys

# Add project root to path so 'src' module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from src.monday_api import MondayClient
from src.data_processor import DataProcessor
from src.analyzer import Analyzer

# Page Config
st.set_page_config(page_title="AI BI Agent", layout="wide")

# Load Environment Variables
load_dotenv()

@st.cache_resource
def get_monday_data():
    """
    Fetches data from Monday.com and returns processed DataFrames.
    Cached to prevent re-fetching on every interaction.
    """
    api_key = os.getenv("MONDAY_API_KEY")
    wo_board_id = os.getenv("WORK_ORDERS_BOARD_ID")
    deals_board_id = os.getenv("DEALS_BOARD_ID")

    if not api_key:
        return None, None, "Missing API Key"

    client = MondayClient()
    
    deals_df = pd.DataFrame()
    wo_df = pd.DataFrame()
    error = None

    try:
        if deals_board_id:
            deals_items = client.get_board_items(int(deals_board_id))
            deals_cols = client.get_board_columns(int(deals_board_id))
            deals_processor = DataProcessor(deals_items, deals_cols)
            deals_df = deals_processor.clean_data()
            
        if wo_board_id:
            wo_items = client.get_board_items(int(wo_board_id))
            wo_cols = client.get_board_columns(int(wo_board_id))
            wo_processor = DataProcessor(wo_items, wo_cols)
            wo_df = wo_processor.clean_data()
            
    except Exception as e:
        error = str(e)
        
    return deals_df, wo_df, error

# --- UI ---

st.title("🤖 AI Business Intelligence Agent")

with st.sidebar:
    st.header("Status")
    if st.button("Refresh Data"):
        st.cache_resource.clear()
        st.rerun()
        
    st.markdown("---")
    st.markdown("**Connected Boards**:")
    st.markdown(f"- Deals Board ID: `{os.getenv('DEALS_BOARD_ID')}`")
    st.markdown(f"- Work Orders Board ID: `{os.getenv('WORK_ORDERS_BOARD_ID')}`")

# Fetch Data
deals_df, wo_df, error = get_monday_data()

if error:
    st.error(f"Error fetching data: {error}")
    st.stop()
    
if deals_df.empty and wo_df.empty:
    st.warning("No data found. Please check your Board IDs.")
    st.stop()

# Initialize Analyzer
analyzer = Analyzer(deals_df, wo_df)

# Create Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💬 Ask AI", "💾 Raw Data"])

with tab1:
    st.subheader("Pipeline Snapshot")
    
    # Metrics Logic (Quick extraction for UI)
    total_pipeline_val = 0
    avg_deal_size = 0
    total_deals = len(deals_df) if not deals_df.empty else 0
    
    # Try using Analyzer helper or reuse logic (replicating briefly for UI specific display)
    value_col = analyzer._find_column_by_similarity(deals_df, ['deal value', 'amount', 'price', 'revenue', 'value'])
    if value_col and not deals_df.empty:
         numeric_values = pd.to_numeric(deals_df[value_col], errors='coerce').fillna(0)
         total_pipeline_val = numeric_values.sum()
         avg_deal_size = numeric_values.mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Deals", total_deals)
    col2.metric("Pipeline Value", f"${total_pipeline_val:,.0f}")
    col3.metric("Avg Deal Size", f"${avg_deal_size:,.0f}")
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("#### Deal Stages")
        stage_col = analyzer._find_column_by_similarity(deals_df, ['stage', 'status', 'phase'])
        if stage_col and not deals_df.empty:
            stage_counts = deals_df[stage_col].value_counts()
            st.bar_chart(stage_counts)
        else:
            st.info("No Stage column found.")

    with col_chart2:
        st.markdown("#### Work Order Status")
        wo_status_col = analyzer._find_column_by_similarity(wo_df, ['status', 'state'])
        if wo_status_col and not wo_df.empty:
            status_counts = wo_df[wo_status_col].value_counts()
            st.bar_chart(status_counts)
        else:
            st.info("No Status column found.")

with tab2:
    st.subheader("Ask the Agent")
    
    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about pipeline health, operations, or request an update..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = ""
            user_input = prompt.lower()
            
            # Simple routing logic (same as CLI)
            if 'update' in user_input or 'summary' in user_input:
                response = analyzer.generate_leadership_update()
            elif 'pipeline' in user_input or 'sales' in user_input or 'deal' in user_input:
                response = analyzer.get_pipeline_benth()
            elif 'operation' in user_input or 'work' in user_input or 'status' in user_input:
                response = analyzer.get_operational_status()
            else:
                 response = "I'm not sure how to answer that. Try asking about 'pipeline', 'sales', 'operations', or 'update'."
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with tab3:
    st.subheader("Raw Data Inspector")
    st.write("Deals Data")
    st.dataframe(deals_df)
    
    st.write("Work Orders Data")
    st.dataframe(wo_df)
