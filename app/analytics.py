import pandas as pd
import matplotlib.pyplot as plt
from .database import db
import io

class AnalyticsEngine:
    def __init__(self, db_manager):
        self.db = db_manager

    def get_transactions_df(self):
        """Fetches all transactions and returns a Pandas DataFrame."""
        try:
            data = self.db.fetch_all("SELECT * FROM transactions")
            if not data:
                # Return empty DataFrame with expected columns to avoid errors
                return pd.DataFrame(columns=['txn_id', 'customer_id', 'amount', 'txn_type', 'category', 'reason', 'payment_method', 'txn_date'])
            
            df = pd.DataFrame(data)
            # Ensure txn_date is datetime
            df['txn_date'] = pd.to_datetime(df['txn_date'])
            return df
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return pd.DataFrame()

    def get_customers_df(self):
        """Fetches all customers and returns a Pandas DataFrame."""
        try:
            data = self.db.fetch_all("SELECT * FROM customers")
            if not data:
                return pd.DataFrame(columns=['customer_id', 'name', 'gender', 'first_purchase_date'])
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error fetching customers: {e}")
            return pd.DataFrame()

    def get_kpis(self):
        """Calculates core Dashboard KPIs."""
        df = self.get_transactions_df()
        
        if df.empty:
            return {
                "total_income": 0.0,
                "total_expense": 0.0,
                "net_profit": 0.0,
                "top_payment_method": "N/A"
            }

        income = df[df['txn_type'] == 'Income']['amount'].sum()
        expense = df[df['txn_type'] == 'Expense']['amount'].sum()
        profit = income - expense
        
        # safely get top payment method
        if not df[df['txn_type'] == 'Income'].empty:
            top_method = df[df['txn_type'] == 'Income']['payment_method'].mode()
            top_method = top_method[0] if not top_method.empty else "N/A"
        else:
            top_method = "N/A"

        return {
            "total_income": income,
            "total_expense": expense,
            "net_profit": profit,
            "top_payment_method": top_method
        }

    def get_customer_kpis(self):
        """Calculates Customer-related KPIs."""
        txn_df = self.get_transactions_df()
        cust_df = self.get_customers_df()
        
        if txn_df.empty or cust_df.empty:
            return {
                "repeat_customer_rate": 0.0,
                "total_customers": len(cust_df)
            }

        # Identify repeat customers (count of distinct transactions > 1 per customer)
        # We look at income transactions only for customer behavior typically
        sales_data = txn_df[txn_df['txn_type'] == 'Income']
        
        if sales_data.empty:
             return {
                "repeat_customer_rate": 0.0,
                "total_customers": len(cust_df)
            }
            
        txn_counts = sales_data.groupby('customer_id').size()
        repeat_customers = txn_counts[txn_counts > 1].count()
        total_active_customers = len(txn_counts)
        
        rate = (repeat_customers / total_active_customers * 100) if total_active_customers > 0 else 0
        
        return {
            "repeat_customer_rate": round(rate, 2),
            "total_customers": len(cust_df)
        }

    def get_revenue_trend(self):
        """Returns data for Revenue Trend Chart."""
        df = self.get_transactions_df()
        if df.empty:
            return None, None

        # Filter Income only
        income_df = df[df['txn_type'] == 'Income'].copy()
        if income_df.empty:
            return None, None
            
        # Group by Date
        trend = income_df.groupby('txn_date')['amount'].sum().sort_index()
        return trend.index, trend.values

# Singleton for app
analytics = AnalyticsEngine(db)
