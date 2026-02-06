# BizAnalytics Offline - Setup & Run Guide

## Prerequisites

1. Python 3.10+ installed.
2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the App

Run the following command in your terminal from the project root:

```bash
python main.py
```

## Features

- **Dashboard**: View key metrics (Income, Expense, Profit, Repeat Customers) and Revenue Trend.
- **Add Entry**: Log Income or Expenses. New customers are automatically created.
- **Customers**: View customer list.
- **Reports**: Export data to CSV or PDF (Pro feature).

## Pro Version

To simulate the "Basic" version (disable PDF export), edit `app/backend.py`:

```python
IS_PRO_VERSION = False
```

## Database

The app creates a local SQLite file `biz_analytics.db` in the run directory. To reset data, simply delete this file.
