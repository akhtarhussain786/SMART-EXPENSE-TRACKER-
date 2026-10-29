"""
Financial Analytics and Smart Insights Engine for Smart Expense Tracker.
Computes financial summaries, category breakdowns, monthly trends, and rule-based AI advice.
"""

from typing import Dict, Any, List
from datetime import datetime
from database import Database

class AnalyticsEngine:
    def __init__(self, db: Database):
        self.db = db

    def get_monthly_summary(self, month_year: str) -> Dict[str, Any]:
        """
        Calculates income, expense, balance, savings rate for a given YYYY-MM.
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total Income
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE type = 'income' AND date LIKE ?
            """, (f"{month_year}%",))
            total_income = cursor.fetchone()[0]

            # Total Expense
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE type = 'expense' AND date LIKE ?
            """, (f"{month_year}%",))
            total_expense = cursor.fetchone()[0]

            # Transaction counts
            cursor.execute("""
                SELECT COUNT(*) FROM transactions WHERE date LIKE ?
            """, (f"{month_year}%",))
            tx_count = cursor.fetchone()[0]

        net_savings = total_income - total_expense
        savings_rate = (net_savings / total_income * 100.0) if total_income > 0 else 0.0

        return {
            "month_year": month_year,
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "net_savings": round(net_savings, 2),
            "savings_rate": round(savings_rate, 1),
            "transaction_count": tx_count
        }

    def get_category_breakdown(self, month_year: str, trans_type: str = "expense") -> List[Dict[str, Any]]:
        """
        Returns spending or earnings grouped by category with percentages.
        """
        summary = self.get_monthly_summary(month_year)
        total = summary['total_expense'] if trans_type == 'expense' else summary['total_income']

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.name as category, c.icon, c.color, 
                       SUM(t.amount) as amount, COUNT(t.id) as count
                FROM transactions t
                JOIN categories c ON t.category_id = c.id
                WHERE t.type = ? AND t.date LIKE ?
                GROUP BY c.id
                ORDER BY amount DESC
            """, (trans_type, f"{month_year}%"))

            rows = cursor.fetchall()
            results = []
            for row in rows:
                amt = row['amount']
                pct = (amt / total * 100.0) if total > 0 else 0.0
                results.append({
                    "category": row['category'],
                    "icon": row['icon'],
                    "color": row['color'],
                    "amount": round(amt, 2),
                    "percentage": round(pct, 1),
                    "count": row['count']
                })
            return results

    def get_payment_method_breakdown(self, month_year: str) -> List[Dict[str, Any]]:
        """Breakdown of expenses by payment method (UPI, Card, Cash, etc.)"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT payment_method, SUM(amount) as total, COUNT(*) as count
                FROM transactions
                WHERE type = 'expense' AND date LIKE ?
                GROUP BY payment_method
                ORDER BY total DESC
            """, (f"{month_year}%",))
            return [dict(row) for row in cursor.fetchall()]

    def generate_smart_insights(self, month_year: str) -> List[Dict[str, str]]:
        """
        Generates actionable, human-readable insights and advisory tips based on user data.
        """
        insights = []
        summary = self.get_monthly_summary(month_year)
        cat_breakdown = self.get_category_breakdown(month_year, "expense")
        budget_status = self.db.get_budget_status(month_year)

        # 1. Budget Alerts
        for b in budget_status:
            if b['budget_limit'] > 0:
                if b['status'] == 'Exceeded':
                    insights.append({
                        "level": "CRITICAL",
                        "title": f"Budget Exceeded in {b['category_name']}",
                        "message": f"You spent ₹{b['actual_spent']:.0f} exceeding your ₹{b['budget_limit']:.0f} budget by ₹{b['actual_spent'] - b['budget_limit']:.0f}."
                    })
                elif b['status'] == 'Warning':
                    insights.append({
                        "level": "WARNING",
                        "title": f"High Spending in {b['category_name']}",
                        "message": f"You have reached {b['percentage']:.0f}% of your allocated ₹{b['budget_limit']:.0f} budget."
                    })

        # 2. Savings Rate Feedback
        savings_rate = summary['savings_rate']
        if summary['total_income'] > 0:
            if savings_rate >= 20.0:
                insights.append({
                    "level": "SUCCESS",
                    "title": "Healthy Savings Rate",
                    "message": f"Awesome! You saved {savings_rate:.1f}% of your earnings this month, beating the standard 20% rule."
                })
            elif savings_rate > 0:
                insights.append({
                    "level": "INFO",
                    "title": "Modest Savings",
                    "message": f"You saved {savings_rate:.1f}% this month. Consider trimming non-essential lifestyle expenses to reach a 20% benchmark."
                })
            else:
                insights.append({
                    "level": "CRITICAL",
                    "title": "Deficit Spending Alert",
                    "message": f"Expenses exceeded income by ₹{abs(summary['net_savings']):.2f}. Review high-cost items immediately."
                })

        # 3. Top Spending Category Concentration
        if cat_breakdown:
            top_cat = cat_breakdown[0]
            if top_cat['percentage'] > 35.0:
                insights.append({
                    "level": "INFO",
                    "title": f"High Concentration in {top_cat['category']}",
                    "message": f"{top_cat['category']} accounts for {top_cat['percentage']:.1f}% (₹{top_cat['amount']:.0f}) of total expenses."
                })

        # 4. Daily Spend Metric
        try:
            today = datetime.now()
            # approximate days passed in month
            cur_month = today.strftime("%Y-%m")
            if cur_month == month_year:
                day_num = max(1, today.day)
            else:
                day_num = 30
            avg_daily = summary['total_expense'] / day_num
            insights.append({
                "level": "INFO",
                "title": "Average Daily Burn Rate",
                "message": f"Your average daily spending is approx ₹{avg_daily:.2f}/day across {day_num} days."
            })
        except Exception:
            pass

        return insights

