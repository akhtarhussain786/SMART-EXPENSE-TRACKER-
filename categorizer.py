"""
Smart Categorization Engine for Smart Expense Tracker.
Uses keyword rules, transaction historical patterns, and smart heuristics 
to automatically detect categories for descriptions.
"""

import re
from typing import Optional, Tuple
from database import Database

class SmartCategorizer:
    def __init__(self, db: Database):
        self.db = db

    def predict_category(self, description: str, trans_type: str = "expense") -> Tuple[Optional[str], float]:
        """
        Predicts category name and confidence score (0.0 to 1.0) given a description text.
        Returns: (predicted_category, confidence)
        """
        if not description or not description.strip():
            return None, 0.0

        clean_desc = description.strip().lower()

        # Step 1: Check Database Smart Rules
        rules = self.db.get_all_rules()
        for rule in rules:
            kw = rule['keyword'].lower()
            # Whole word or prominent substring match
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, clean_desc):
                return rule['category_name'], 0.95
            elif kw in clean_desc:
                return rule['category_name'], 0.85

        # Step 2: Check historical transaction habits of user (Learned pattern)
        historical_category = self._check_history(clean_desc)
        if historical_category:
            return historical_category, 0.80

        # Step 3: Heuristic Keyword Fallback
        if trans_type == "income":
            if any(w in clean_desc for w in ["salary", "stipend", "pay", "credit"]):
                return "Salary", 0.70
            return "Other Income", 0.50
        else:
            if any(w in clean_desc for w in ["tea", "coffee", "roll", "snack", "thali", "sweets"]):
                return "Food & Dining", 0.75
            if any(w in clean_desc for w in ["cab", "toll", "parking", "train", "ticket"]):
                return "Transportation", 0.75
            if any(w in clean_desc for w in ["recharge", "electricity", "gas", "dth"]):
                return "Utilities & Bills", 0.75
            if any(w in clean_desc for w in ["doctor", "pill", "tablet", "syrup", "medical"]):
                return "Health & Medical", 0.75

        # Default fallback
        fallback = "Miscellaneous Expense" if trans_type == "expense" else "Other Income"
        return fallback, 0.30

    def _check_history(self, clean_desc: str) -> Optional[str]:
        """Checks past transactions for exact or similar description to infer category."""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT c.name, COUNT(*) as freq
                    FROM transactions t
                    JOIN categories c ON t.category_id = c.id
                    WHERE LOWER(t.description) LIKE ?
                    GROUP BY c.name
                    ORDER BY freq DESC
                    LIMIT 1
                """, (f"%{clean_desc}%",))
                row = cursor.fetchone()
                if row:
                    return row[0]
        except Exception:
            pass
        return None

    def learn_rule(self, keyword: str, category_name: str) -> bool:
        """Stores a new rule learned from user confirmation."""
        return self.db.add_rule(keyword.strip(), category_name)

