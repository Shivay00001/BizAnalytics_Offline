from .database import db
from .analytics import analytics

class BackendService:
    IS_PRO_VERSION = True # Toggle this for Basic/Pro builds

    def __init__(self):
        self.db = db
        self.analytics = analytics

    def add_customer(self, name, gender, contact, first_purchase_date=None):
        """Adds a new customer."""
        query = """
            INSERT INTO customers (name, gender, contact, first_purchase_date)
            VALUES (?, ?, ?, ?)
        """
        # If no date provided, DB defaults to today, but we can also handle it here if needed.
        # Passing None lets DB handle the default.
        return self.db.execute_query(query, (name, gender, contact, first_purchase_date))

    def get_all_customers(self):
        """Returns list of all customers."""
        return self.db.fetch_all("SELECT * FROM customers ORDER BY name ASC")

    def add_transaction(self, customer_id, amount, txn_type, category, reason, payment_method, txn_date):
        """Adds a new transaction."""
        query = """
            INSERT INTO transactions (customer_id, amount, txn_type, category, reason, payment_method, txn_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return self.db.execute_query(query, (customer_id, amount, txn_type, category, reason, payment_method, txn_date))

    def get_dashboard_stats(self):
        """Aggregates all stats for the dashboard."""
        kpis = self.analytics.get_kpis()
        cust_kpis = self.analytics.get_customer_kpis()
        
        # Merge dicts
        return {**kpis, **cust_kpis}

    def get_revenue_trend_data(self):
        """Returns (dates, values) for the trend chart."""
        return self.analytics.get_revenue_trend()

    def get_recent_transactions(self, limit=10):
        """Get recent transactions for display."""
        query = """
            SELECT t.*, c.name as customer_name 
            FROM transactions t 
            LEFT JOIN customers c ON t.customer_id = c.customer_id 
            ORDER BY t.txn_date DESC, t.txn_id DESC 
            LIMIT ?
        """
        return self.db.fetch_all(query, (limit,))

service = BackendService()
