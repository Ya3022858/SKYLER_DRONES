import pandas as pd

class Analyzer:
    def __init__(self, deals_df=None, work_orders_df=None):
        self.deals_df = deals_df
        self.work_orders_df = work_orders_df

    def _find_column_by_similarity(self, df, keywords):
        """
        Helper to find a column name that matches a list of keywords.
        """
        if df is None or df.empty:
            return None
            
        columns = df.columns.str.lower()
        for col in df.columns:
            col_lower = col.lower()
            for keyword in keywords:
                if keyword in col_lower:
                    return col
        return None

    def get_pipeline_benth(self):
        """
        Analyzes the health of the sales pipeline.
        """
        if self.deals_df is None or self.deals_df.empty:
            return "No deals data available."

        # Attempt to find relevant columns
        value_col = self._find_column_by_similarity(self.deals_df, ['deal value', 'amount', 'price', 'revenue', 'value'])
        stage_col = self._find_column_by_similarity(self.deals_df, ['stage', 'status', 'phase'])
        
        insights = []
        
        total_deals = len(self.deals_df)
        insights.append(f"Total Deals in Pipeline: {total_deals}")
        
        if value_col:
            # Clean non-numeric values just in case
            numeric_values = pd.to_numeric(self.deals_df[value_col], errors='coerce').fillna(0)
            total_value = numeric_values.sum()
            avg_value = numeric_values.mean()
            insights.append(f"Total Pipeline Value: ${total_value:,.2f}")
            insights.append(f"Average Deal Size: ${avg_value:,.2f}")
        
        if stage_col:
            stage_counts = self.deals_df[stage_col].value_counts()
            insights.append("\nDeal Distribution by Stage:")
            for stage, count in stage_counts.items():
                insights.append(f"  - {stage}: {count}")
                
        return "\n".join(insights)

    def get_operational_status(self):
        """
        Analyzes work orders / operational status.
        """
        if self.work_orders_df is None or self.work_orders_df.empty:
            return "No work orders data available."
            
        status_col = self._find_column_by_similarity(self.work_orders_df, ['status', 'state', 'progress'])
        priority_col = self._find_column_by_similarity(self.work_orders_df, ['priority', 'urgency'])
        
        insights = []
        insights.append(f"Total Work Orders: {len(self.work_orders_df)}")
        
        if status_col:
            status_counts = self.work_orders_df[status_col].value_counts()
            insights.append("\nWork Order Status:")
            for status, count in status_counts.items():
                insights.append(f"  - {status}: {count}")
                
        if priority_col:
             priority_counts = self.work_orders_df[priority_col].value_counts()
             insights.append("\nBreakdown by Priority:")
             for prio, count in priority_counts.items():
                 insights.append(f"  - {prio}: {count}")
                 
        return "\n".join(insights)

    def generate_leadership_update(self):
        """
        Generates a high-level executive summary.
        """
        summary = ["*** EXECUTIVE LEADERSHIP UPDATE ***\n"]
        
        # Sales Highlights
        summary.append("SALES & PIPELINE")
        summary.append(self.get_pipeline_benth())
        summary.append("\n" + "-"*30 + "\n")
        
        # Operations Highlights
        summary.append("OPERATIONS & EXECUTION")
        summary.append(self.get_operational_status())
        
        return "\n".join(summary)
