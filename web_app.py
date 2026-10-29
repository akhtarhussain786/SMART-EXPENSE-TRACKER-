"""
FastAPI Web Application Backend for Smart Expense Tracker.
Exposes REST APIs for:
- Adding, viewing, and removing transactions (Expenses & Incomes)
- Real-time Smart Auto-Categorization
- Financial summaries and category breakdowns for interactive charts
- Budget tracking and threshold alerts
- Serving the modern responsive web frontend
"""

import os
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel, Field

from database import Database
from categorizer import SmartCategorizer
from analytics import AnalyticsEngine
from exporter import DataExporter

# Initialize Application & Engines
app = FastAPI(title="Smart Expense Tracker API", version="1.0.0")
db = Database()
categorizer = SmartCategorizer(db)
analytics = AnalyticsEngine(db)
exporter = DataExporter(db)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# --- Request / Response Models ---
class TransactionCreate(BaseModel):
    date: str = Field(..., example="2026-10-29")
    type: str = Field(..., example="expense")  # 'expense' or 'income'
    category: str = Field(..., example="Food & Dining")
    amount: float = Field(..., gt=0, example=450.0)
    description: str = Field(..., example="Zomato Dinner Biryani")
    payment_method: str = Field(default="UPI", example="UPI")
    notes: Optional[str] = Field(default="", example="")

class BudgetCreate(BaseModel):
    category: str
    month: str
    limit: float

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    """Serves the main responsive web dashboard HTML page."""
    html_path = os.path.join(TEMPLATES_DIR, "index.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="Frontend template index.html not found.")
    with open(html_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/summary")
async def get_summary(month: Optional[str] = None):
    """Returns monthly income, expense, net savings, and savings rate."""
    m = month or datetime.now().strftime("%Y-%m")
    summary = analytics.get_monthly_summary(m)
    return summary

@app.get("/api/categories")
async def get_categories(type: Optional[str] = None):
    """Returns list of categories (optionally filtered by type)."""
    return db.get_categories(cat_type=type)

@app.get("/api/transactions")
async def get_transactions(
    month: Optional[str] = None,
    type: Optional[str] = None,
    search: Optional[str] = None
):
    """Fetches transactions filtered by month, type, or search keyword."""
    m = month or datetime.now().strftime("%Y-%m")
    t = None if (not type or type == "All") else type
    s = search.strip() if search else None
    return db.get_transactions(month_year=m, trans_type=t, search_query=s)

@app.post("/api/transactions")
async def add_transaction(tx: TransactionCreate):
    """Adds a new expense or income transaction."""
    try:
        new_id = db.add_transaction(
            date=tx.date,
            trans_type=tx.type,
            category_name=tx.category,
            amount=tx.amount,
            description=tx.description,
            payment_method=tx.payment_method,
            notes=tx.notes or ""
        )
        return {"success": True, "id": new_id, "message": "Transaction added successfully"}
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})

@app.delete("/api/transactions/{tx_id}")
async def delete_transaction(tx_id: int):
    """Removes / deletes an expense transaction by ID."""
    success = db.delete_transaction(tx_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Transaction with ID {tx_id} not found.")
    return {"success": True, "id": tx_id, "message": "Transaction removed successfully"}

@app.get("/api/predict-category")
async def predict_category(desc: str = Query(...), type: str = Query("expense")):
    """Sub-millisecond heuristic auto-categorizer endpoint."""
    category, confidence = categorizer.predict_category(desc, type)
    return {"category": category, "confidence": round(confidence, 2)}

@app.get("/api/category-breakdown")
async def get_category_breakdown(month: Optional[str] = None):
    """Returns breakdown of spending grouped by category for donut chart."""
    m = month or datetime.now().strftime("%Y-%m")
    return analytics.get_category_breakdown(m, trans_type="expense")

@app.get("/api/budgets")
async def get_budgets(month: Optional[str] = None):
    """Returns monthly budget targets vs actual spent and status."""
    m = month or datetime.now().strftime("%Y-%m")
    return db.get_budget_status(m)

@app.post("/api/budgets")
async def set_budget(b: BudgetCreate):
    """Sets or updates monthly budget limit for a category."""
    ok = db.set_budget(b.category, b.month, b.limit)
    return {"success": ok}

@app.get("/api/insights")
async def get_insights(month: Optional[str] = None):
    """Returns smart AI financial insights and tips."""
    m = month or datetime.now().strftime("%Y-%m")
    return analytics.generate_smart_insights(m)


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 SMART EXPENSE TRACKER - WEB SERVER STARTED!")
    print("👉 Open your browser at: http://127.0.0.1:8000")
    print("="*60 + "\n")
    uvicorn.run("web_app:app", host="127.0.0.1", port=8000, reload=True)

