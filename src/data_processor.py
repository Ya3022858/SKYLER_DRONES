import pandas as pd
import json

def clean_column_value(col_data):
    """
    Extracts meaningful value from Monday.com column structure.
    """
    if not col_data:
        return None
    
    text = col_data.get('text')
    
    # Try to parse numeric values if text looks like a number
    # Monday returns numbers as text usually
    if col_data.get('type') == 'numbers':
        if text:
            try:
                return float(text.replace(',', ''))
            except ValueError:
                return text
        return None
        
    return text

def normalize_dataframe(items, columns_map=None):
    """
    Converts list of items into a clean Pandas DataFrame.
    """
    if not items:
        return pd.DataFrame()

    processed_data = []
    
    for item in items:
        row = {'id': item['id'], 'name': item['name']}
        
        for col in item['column_values']:
            clean_val = clean_column_value(col)
            # Use title if map provided, else ID
            col_key = col['id']
            if columns_map and col_key in columns_map:
                col_key = columns_map[col_key]
                
            row[col_key] = clean_val
            
        processed_data.append(row)
        
    df = pd.DataFrame(processed_data)
    return df

class DataProcessor:
    def __init__(self, items, columns_map=None):
        self.raw_items = items
        self.df = normalize_dataframe(items, columns_map)

    def get_dataframe(self):
        return self.df

    def clean_data(self):
        # Remove duplicates
        if not self.df.empty:
            self.df.drop_duplicates(subset=['id'], inplace=True)
        return self.df
