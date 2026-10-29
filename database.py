"""
Database Management Module for Smart Expense Tracker
Handles SQLite connection, schema creation, data seeding, and CRUD operations.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expense_tracker.db")

DEFAULT_CATEGORIES = [
    # Expenses
    ("Food & Dining", "expense", "🍔", "#F59E0B"),
    ("Groceries", "expense", "🛒", "#10B981"),
    ("Transportation", "expense", "🚗", "#3B82F6"),
    ("Utilities & Bills", "expense", "💡", "#8B5CF6"),
    ("Housing & Rent", "expense", "🏠", "#EC4899"),
    ("Entertainment", "expense", "🎬", "#F43F5E"),
    ("Health & Medical", "expense", "💊", "#14B8A6"),
    ("Shopping & Lifestyle", "expense", "🛍️", "#6366F1"),
    ("Education & Courses", "expense", "📚", "#06B6D4"),
    ("Miscellaneous Expense", "expense", "📦", "#6B7280"),
    # Income
    ("Salary", "income", "💼", "#10B981"),
    ("Freelance & Business", "income", "💻", "#059669"),
    ("Investments & Dividends", "income", "📈", "#34D399"),
    ("Gifts & Allowance", "income", "🎁", "#6EE7B7"),
    ("Other Income", "income", "💰", "#A7F3D0")
]

DEFAULT_SMART_RULES = [
    ("swiggy", "Food & Dining"),
    ("zomato", "Food & Dining"),
    ("mcdonalds", "Food & Dining"),
    ("starbucks", "Food & Dining"),
    ("restaurant", "Food & Dining"),
    ("cafe", "Food & Dining"),
    ("burger", "Food & Dining"),
    ("pizza", "Food & Dining"),
    ("lunch", "Food & Dining"),
    ("dinner", "Food & Dining"),
    ("supermarket", "Groceries"),
    ("blinkit", "Groceries"),
    ("zepto", "Groceries"),
    ("instamart", "Groceries"),
    ("bigbasket", "Groceries"),
    ("vegetables", "Groceries"),
    ("milk", "Groceries"),
    ("ration", "Groceries"),
    ("uber", "Transportation"),
    ("ola", "Transportation"),
    ("metro", "Transportation"),
    ("bus", "Transportation"),
    ("train", "Transportation"),
    ("petrol", "Transportation"),
    ("diesel", "Transportation"),
    ("fuel", "Transportation"),
    ("auto", "Transportation"),
    ("rapido", "Transportation"),
    ("flight", "Transportation"),
    ("netflix", "Entertainment"),
    ("prime", "Entertainment"),
    ("spotify", "Entertainment"),
    ("hotstar", "Entertainment"),
    ("movie", "Entertainment"),
    ("cinema", "Entertainment"),
    ("game", "Entertainment"),
    ("steam", "Entertainment"),
    ("electricity", "Utilities & Bills"),
    ("water bill", "Utilities & Bills"),
    ("wifi", "Utilities & Bills"),
    ("broadband", "Utilities & Bills"),
    ("mobile recharge", "Utilities & Bills"),
    ("gas cylinder", "Utilities & Bills"),
    ("rent", "Housing & Rent"),
    ("flat rent", "Housing & Rent"),
    ("hostel", "Housing & Rent"),
    ("maintenance", "Housing & Rent"),
    ("pharmacy", "Health & Medical"),
    ("doctor", "Health & Medical"),
    ("medicine", "Health & Medical"),
    ("hospital", "Health & Medical"),
    ("clinic", "Health & Medical"),
    ("amazon", "Shopping & Lifestyle"),
    ("flipkart", "Shopping & Lifestyle"),
    ("myntra", "Shopping & Lifestyle"),
    ("clothes", "Shopping & Lifestyle"),
    ("shoes", "Shopping & Lifestyle"),
    ("zara", "Shopping & Lifestyle"),
    ("udemy", "Education & Courses"),
    ("coursera", "Education & Courses"),
    ("book", "Education & Courses"),
    ("tuition", "Education & Courses"),
    ("salary", "Salary"),
    ("paycheck", "Salary"),
    ("freelance", "Freelance & Business"),
    ("upwork", "Freelance & Business"),
    ("fiverr", "Freelance & Business"),
    ("client", "Freelance & Business"),
    ("dividend", "Investments & Dividends"),
    ("stocks", "Investments & Dividends"),
    ("mutual fund", "Investments & Dividends")
]


class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Creates tables and populates default categories and smart rules if empty."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Categories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('expense', 'income')),
                    icon TEXT DEFAULT '💳',
                    color TEXT DEFAULT '#3B82F6'
                )
            """)

            # Transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('expense', 'income')),
                    category_id INTEGER NOT NULL,
                    amount REAL NOT NULL CHECK(amount > 0),
                    description TEXT NOT NULL,
                    payment_method TEXT DEFAULT 'UPI',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
                )
            """)

            # Budgets table (Category-level monthly limits)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER NOT NULL,
                    month_year TEXT NOT NULL,  -- Format: 'YYYY-MM'
                    amount_limit REAL NOT NULL CHECK(amount_limit >= 0),
                    UNIQUE(category_id, month_year),
                    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
                )
            """)

            # Smart rules table for auto-categorization
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS smart_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT UNIQUE NOT NULL,
                    category_name TEXT NOT NULL
                )
            """)

            conn.commit()

        # Seed categories if empty
        self._seed_default_categories()
        self._seed_default_rules()

    def _seed_default_categories(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM categories")
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.executemany(
                    "INSERT OR IGNORE INTO categories (name, type, icon, color) VALUES (?, ?, ?, ?)",
                    DEFAULT_CATEGORIES
                )
                conn.commit()

    def _seed_default_rules(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM smart_rules")
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.executemany(
                    "INSERT OR IGNORE INTO smart_rules (keyword, category_name) VALUES (?, ?)",
                    DEFAULT_SMART_RULES
                )
                conn.commit()

    # --- Category Operations ---
    def get_categories(self, cat_type: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if cat_type:
                cursor.execute("SELECT * FROM categories WHERE type = ? ORDER BY name ASC", (cat_type,))
            else:
                cursor.execute("SELECT * FROM categories ORDER BY type DESC, name ASC")
            return [dict(row) for row in cursor.fetchall()]

    def get_category_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categories WHERE name = ?", (name,))
            row = cursor.fetchone()
            return dict(row) if row else None

    # --- Transaction Operations ---
    def add_transaction(self, date: str, trans_type: str, category_name: str, 
                        amount: float, description: str, payment_method: str = "UPI", 
                        notes: str = "") -> int:
        cat = self.get_category_by_name(category_name)
        if not cat:
            # Create category on the fly if needed
            with self.get_connection() as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO categories (name, type) VALUES (?, ?)", (category_name, trans_type))
                conn.commit()
                cat_id = cur.lastrowid
        else:
            cat_id = cat['id']

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (date, type, category_id, amount, description, payment_method, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (date, trans_type, cat_id, float(amount), description.strip(), payment_method, notes.strip()))
            conn.commit()
            return cursor.lastrowid

    def get_transactions(self, month_year: Optional[str] = None, 
                         trans_type: Optional[str] = None,
                         category_id: Optional[int] = None,
                         search_query: Optional[str] = None) -> List[Dict[str, Any]]:
        query = """
            SELECT t.id, t.date, t.type, t.amount, t.description, t.payment_method, t.notes,
                   c.name as category_name, c.icon as category_icon, c.color as category_color, c.id as category_id
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE 1=1
        """
        params = []
        if month_year:
            query += " AND t.date LIKE ?"
            params.append(f"{month_year}%")
        if trans_type:
            query += " AND t.type = ?"
            params.append(trans_type)
        if category_id:
            query += " AND t.category_id = ?"
            params.append(category_id)
        if search_query:
            query += " AND (t.description LIKE ? OR t.notes LIKE ? OR c.name LIKE ?)"
            wildcard = f"%{search_query}%"
            params.extend([wildcard, wildcard, wildcard])

        query += " ORDER BY t.date DESC, t.id DESC"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def delete_transaction(self, tx_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
            conn.commit()
            return cursor.rowcount > 0

    def update_transaction(self, tx_id: int, date: str, trans_type: str, category_name: str,
                           amount: float, description: str, payment_method: str, notes: str) -> bool:
        cat = self.get_category_by_name(category_name)
        if not cat:
            return False
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE transactions
                SET date = ?, type = ?, category_id = ?, amount = ?, description = ?, payment_method = ?, notes = ?
                WHERE id = ?
            """, (date, trans_type, cat['id'], float(amount), description, payment_method, notes, tx_id))
            conn.commit()
            return cursor.rowcount > 0

    # --- Budget Operations ---
    def set_budget(self, category_name: str, month_year: str, amount_limit: float) -> bool:
        cat = self.get_category_by_name(category_name)
        if not cat:
            return False
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO budgets (category_id, month_year, amount_limit)
                VALUES (?, ?, ?)
                ON CONFLICT(category_id, month_year) 
                DO UPDATE SET amount_limit = excluded.amount_limit
            """, (cat['id'], month_year, float(amount_limit)))
            conn.commit()
            return True

    def get_budget_status(self, month_year: str) -> List[Dict[str, Any]]:
        """
        Calculates budget limit, actual spend, remaining, and percentage used for each category in a month.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    c.id as category_id,
                    c.name as category_name,
                    c.icon as category_icon,
                    c.color as category_color,
                    COALESCE(b.amount_limit, 0) as budget_limit,
                    COALESCE(SUM(t.amount), 0) as actual_spent
                FROM categories c
                LEFT JOIN budgets b ON c.id = b.category_id AND b.month_year = ?
                LEFT JOIN transactions t ON c.id = t.category_id AND t.date LIKE ? AND t.type = 'expense'
                WHERE c.type = 'expense'
                GROUP BY c.id
                ORDER BY budget_limit DESC, actual_spent DESC
            """, (month_year, f"{month_year}%"))
            
            results = []
            for row in cursor.fetchall():
                r = dict(row)
                limit = r['budget_limit']
                spent = r['actual_spent']
                remaining = max(0.0, limit - spent) if limit > 0 else 0.0
                pct = (spent / limit * 100.0) if limit > 0 else 0.0
                status = "Normal"
                if limit > 0:
                    if spent > limit:
                        status = "Exceeded"
                    elif pct >= 80:
                        status = "Warning"
                results.append({
                    **r,
                    "remaining": remaining,
                    "percentage": round(pct, 1),
                    "status": status
                })
            return results

    # --- Smart Rules ---
    def get_all_rules(self) -> List[Dict[str, str]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT keyword, category_name FROM smart_rules ORDER BY keyword ASC")
            return [dict(row) for row in cursor.fetchall()]

    def add_rule(self, keyword: str, category_name: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT OR REPLACE INTO smart_rules (keyword, category_name) VALUES (?, ?)",
                               (keyword.lower().strip(), category_name))
                conn.commit()
                return True
            except Exception:
                return False

