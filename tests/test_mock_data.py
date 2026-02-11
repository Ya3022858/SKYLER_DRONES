import pandas as pd
from src.analyzer import Analyzer

def test_analyzer():
    print("Testing Analyzer with Mock Data...")
    
    # Mock Deals Data
    deals_data = {
        'id': [1, 2, 3, 4],
        'Name': ['Deal A', 'Deal B', 'Deal C', 'Deal D'],
        'Stage': ['Lead', 'Negotiation', 'Closed Won', 'Qualified'],
        'Value': [1000, 5000, 10000, 2500]
    }
    deals_df = pd.DataFrame(deals_data)
    
    # Mock Work Orders Data
    wo_data = {
        'id': [101, 102, 103],
        'Name': ['Order X', 'Order Y', 'Order Z'],
        'Status': ['In Progress', 'Done', 'Stuck'],
        'Priority': ['High', 'Medium', 'Low']
    }
    wo_df = pd.DataFrame(wo_data)
    
    analyzer = Analyzer(deals_df, wo_df)
    
    print("\n--- Pipeline Health ---")
    print(analyzer.get_pipeline_benth())
    
    print("\n--- Operational Status ---")
    print(analyzer.get_operational_status())
    
    print("\n--- Leadership Update ---")
    print(analyzer.generate_leadership_update())
    
if __name__ == "__main__":
    test_analyzer()
