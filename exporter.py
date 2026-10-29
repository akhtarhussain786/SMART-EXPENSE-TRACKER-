"""
Exporter Module for Smart Expense Tracker.
Supports exporting transactions to CSV, JSON, and text audit formats.
"""

import csv
import json
from typing import List, Dict, Any
from database import Database

class DataExporter:
    def __init__(self, db: Database):
        self.db = db

    def export_to_csv(self, file_path: str, month_year: str = None) -> int:
        """Exports transactions to a formatted CSV file. Returns number of rows exported."""
        transactions = self.db.get_transactions(month_year=month_year)
        if not transactions:
            return 0

        fieldnames = ["ID", "Date", "Type", "Category", "Amount", "Description", "Payment Method", "Notes"]
        
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for tx in transactions:
                writer.writerow({
                    "ID": tx["id"],
                    "Date": tx["date"],
                    "Type": tx["type"].capitalize(),
                    "Category": tx["category_name"],
                    "Amount": f"{tx['amount']:.2f}",
                    "Description": tx["description"],
                    "Payment Method": tx["payment_method"],
                    "Notes": tx["notes"] or ""
                })
        return len(transactions)

    def export_to_json(self, file_path: str) -> int:
        """Exports all transactions, categories, and budgets to JSON backup."""
        all_tx = self.db.get_transactions()
        cats = self.db.get_categories()
        
        backup_data = {
            "metadata": {
                "version": "1.0",
                "app": "Smart Expense Tracker"
            },
            "categories": cats,
            "transactions": all_tx
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=4, ensure_ascii=False)

        return len(all_tx)

