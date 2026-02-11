import os
import sys
import pandas as pd
from dotenv import load_dotenv
from src.monday_api import MondayClient
from src.data_processor import DataProcessor
from src.analyzer import Analyzer

# Load environment variables
load_dotenv()

def main():
    print("Initializing AI Business Intelligence Agent...")
    
    # 1. Check Configuration
    api_key = os.getenv("MONDAY_API_KEY")
    wo_board_id = os.getenv("WORK_ORDERS_BOARD_ID")
    deals_board_id = os.getenv("DEALS_BOARD_ID")
    
    if not api_key:
        print("Error: MONDAY_API_KEY not found in .env file.")
        print("Please configure your .env file.")
        return

    client = MondayClient()
    
    # 2. Fetch Data (with error handling)
    print("Fetching data from Monday.com...")
    
    deals_df = pd.DataFrame()
    wo_df = pd.DataFrame()
    
    try:
        if deals_board_id:
            print(f"  - Fetching Deals (Board ID: {deals_board_id})...")
            deals_items = client.get_board_items(int(deals_board_id))
            deals_cols = client.get_board_columns(int(deals_board_id))
            deals_processor = DataProcessor(deals_items, deals_cols)
            deals_df = deals_processor.clean_data()
            print(f"    Loaded {len(deals_df)} deals.")
        else:
            print("  - Warning: DEALS_BOARD_ID not set.")

        if wo_board_id:
            print(f"  - Fetching Work Orders (Board ID: {wo_board_id})...")
            wo_items = client.get_board_items(int(wo_board_id))
            wo_cols = client.get_board_columns(int(wo_board_id))
            wo_processor = DataProcessor(wo_items, wo_cols)
            wo_df = wo_processor.clean_data()
            print(f"    Loaded {len(wo_df)} work orders.")
        else:
            print("  - Warning: WORK_ORDERS_BOARD_ID not set.")
            
    except Exception as e:
        print(f"\nCRITICAL ERROR fetching data: {e}")
        return

    # 3. Initialize Analyzer
    analyzer = Analyzer(deals_df, wo_df)
    
    print("\n" + "="*50)
    print(" AGENT READY ")
    print("="*50)
    print("You can ask questions like:")
    print(" - 'How is the pipeline looking?'")
    print(" - 'Show me operational status'")
    print(" - 'Give me a leadership update'")
    print(" - 'exit' to quit")
    print("-" * 50)

    # 4. Main Interaction Loop
    while True:
        try:
            user_input = input("\nQuery > ").strip().lower()
            
            if user_input in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
                
            if not user_input:
                continue
                
            # Simple keyword matching for routing queries
            if 'update' in user_input or 'summary' in user_input or 'report' in user_input:
                print("\nGenerating Leadership Update...\n")
                print(analyzer.generate_leadership_update())
                
            elif 'pipeline' in user_input or 'sales' in user_input or 'deal' in user_input:
                print("\nAnalyzing Pipeline...\n")
                print(analyzer.get_pipeline_benth())
                
            elif 'operation' in user_input or 'work' in user_input or 'order' in user_input or 'status' in user_input:
                print("\nAnalyzing Operations...\n")
                print(analyzer.get_operational_status())
                
            else:
                print("I'm not sure how to answer that yet. Try asking about 'pipeline', 'operations', or 'update'.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred during analysis: {e}")

if __name__ == "__main__":
    main()
