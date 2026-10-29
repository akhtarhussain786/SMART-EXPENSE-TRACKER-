"""
Sample Data Generator for Smart Expense Tracker.
Fills the SQLite database with realistic demo transactions and budgets
for instant demonstration and testing.
"""

from datetime import datetime, timedelta
import random
from database import Database

def seed_sample_data(db: Database):
    # Current month
    now = datetime.now()
    cur_month = now.strftime("%Y-%m")
    
    # Check if data already exists
    existing = db.get_transactions()
    if len(existing) > 5:
        print("[INFO] Sample data already present. Skipping.")
        return

    print("[INFO] Seeding realistic sample transactions and budgets...")

    # Set Monthly Budgets for Current Month
    budgets = [
        ("Food & Dining", 12000),
        ("Groceries", 8000),
        ("Transportation", 5000),
        ("Utilities & Bills", 4500),
        ("Entertainment", 3500),
        ("Shopping & Lifestyle", 7000),
        ("Health & Medical", 3000)
    ]
    for cat, limit in budgets:
        db.set_budget(cat, cur_month, limit)

    # Incomes
    db.add_transaction(f"{cur_month}-01", "income", "Salary", 75000.0, "Monthly Corporate Salary", "Bank Transfer", "Direct Deposit")
    db.add_transaction(f"{cur_month}-05", "income", "Freelance & Business", 15000.0, "Web Development Client Payment", "UPI", "Milestone 2 payment")
    db.add_transaction(f"{cur_month}-12", "income", "Investments & Dividends", 2400.0, "Quarterly Stock Dividend", "Bank Transfer", "TCS Dividend")

    # Expenses (Realistic items)
    sample_expenses = [
        # Date, Category, Amount, Description, Method
        (1, "Housing & Rent", 18000.0, "Flat Monthly Rent", "Net Banking"),
        (2, "Utilities & Bills", 1850.0, "Electricity Bill - BESCOM", "UPI"),
        (3, "Groceries", 2450.0, "Blinkit grocery order - oil, flour, milk", "UPI"),
        (4, "Transportation", 450.0, "Uber cab ride to office", "UPI"),
        (6, "Food & Dining", 680.0, "Zomato dinner biryani order", "UPI"),
        (7, "Entertainment", 799.0, "Netflix 4K Monthly Subscription", "Credit Card"),
        (8, "Transportation", 2100.0, "Petrol refill at Indian Oil pump", "Credit Card"),
        (10, "Shopping & Lifestyle", 3499.0, "Amazon purchase - Ergonomic Keyboard", "Credit Card"),
        (12, "Food & Dining", 1450.0, "Dinner with colleagues at Barbeque Nation", "UPI"),
        (14, "Health & Medical", 620.0, "Apollo Pharmacy - Vitamins & First Aid", "UPI"),
        (16, "Utilities & Bills", 999.0, "Airtel Xstream Fiber broadband bill", "UPI"),
        (18, "Groceries", 3100.0, "Supermarket weekly fruits & staples", "Debit Card"),
        (20, "Food & Dining", 520.0, "McDonalds burger combo lunch", "UPI"),
        (22, "Transportation", 380.0, "Ola auto ride city center", "UPI"),
        (24, "Shopping & Lifestyle", 2200.0, "Myntra casual shirts shopping", "Credit Card"),
        (26, "Education & Courses", 499.0, "Udemy Python Full Stack Course", "Debit Card"),
        (27, "Food & Dining", 890.0, "Cafe Coffee Day snacks with friends", "UPI"),
        (28, "Entertainment", 950.0, "PVR Cinemas movie tickets (2 seats)", "UPI")
    ]

    for day, cat, amt, desc, method in sample_expenses:
        # Clamp day to current month length
        day_str = f"{day:02d}"
        date_str = f"{cur_month}-{day_str}"
        db.add_transaction(date_str, "expense", cat, amt, desc, method, "Sample data record")

    print("[SUCCESS] Sample data initialized successfully.")

if __name__ == "__main__":
    db = Database()
    seed_sample_data(db)

