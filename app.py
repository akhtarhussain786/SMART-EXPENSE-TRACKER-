"""
Smart Expense Tracker - Desktop Application
Built with Python Tkinter / ttk.
Features:
- Live Interactive Dashboard with custom Canvas Pie & Bar Visualizations
- Smart Auto-Categorization while typing
- Transactions Management with Search & Filters
- Budget Planner with Color-Coded Progress Bars & Threshold Alerts
- Smart Financial Insights & Rule Training
- CSV / JSON Exporters and PDF Synopsis Launcher
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import math

from database import Database
from categorizer import SmartCategorizer
from analytics import AnalyticsEngine
from exporter import DataExporter

class SmartExpenseTrackerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Smart Expense Tracker - Developed by Disha Prajapati")
        self.root.geometry("1150x740")
        self.root.minsize(1000, 650)

        # Initialize core components
        self.db = Database()
        self.categorizer = SmartCategorizer(self.db)
        self.analytics = AnalyticsEngine(self.db)
        self.exporter = DataExporter(self.db)

        # Current working month (YYYY-MM)
        self.current_month_var = tk.StringVar(value=datetime.now().strftime("%Y-%m"))

        # Setup modern styling
        self._setup_styles()

        # Build UI layout
        self._build_top_navbar()
        self._build_notebook_tabs()

        # Refresh all views with initial data
        self.refresh_all_views()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Palette
        self.BG_MAIN = "#F8FAFC"
        self.COLOR_PRIMARY = "#1E3A8A"     # Deep Navy
        self.COLOR_SECONDARY = "#3B82F6"   # Electric Blue
        self.COLOR_SUCCESS = "#10B981"     # Emerald Green
        self.COLOR_DANGER = "#EF4444"      # Crimson Red
        self.COLOR_WARNING = "#F59E0B"     # Amber
        self.COLOR_CARD_BG = "#FFFFFF"

        self.root.configure(bg=self.BG_MAIN)

        self.style.configure(".", background=self.BG_MAIN, font=("Segoe UI", 10))
        self.style.configure("TNotebook", background=self.BG_MAIN, borderwidth=0)
        self.style.configure("TNotebook.Tab", padding=[18, 9], font=("Segoe UI", 10, "bold"), background="#E2E8F0")
        self.style.map("TNotebook.Tab",
            background=[("selected", self.COLOR_PRIMARY)],
            foreground=[("selected", "#FFFFFF")]
        )

        self.style.configure("Card.TFrame", background=self.COLOR_CARD_BG, relief="ridge", borderwidth=1)
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background=self.COLOR_PRIMARY, foreground="#FFFFFF")
        self.style.map("Primary.TButton", background=[("active", "#1E40AF")])

        self.style.configure("Success.TButton", font=("Segoe UI", 10, "bold"), background=self.COLOR_SUCCESS, foreground="#FFFFFF")
        self.style.map("Success.TButton", background=[("active", "#059669")])

        self.style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), background=self.COLOR_DANGER, foreground="#FFFFFF")
        self.style.map("Danger.TButton", background=[("active", "#DC2626")])

        # Treeview styling
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#E2E8F0", foreground="#1E293B")
        self.style.configure("Treeview", rowheight=28, font=("Segoe UI", 10), background="#FFFFFF")
        self.style.map("Treeview", background=[("selected", "#DBEAFE")], foreground=[("selected", "#1E3A8A")])

    def _build_top_navbar(self):
        nav_frame = tk.Frame(self.root, bg=self.COLOR_PRIMARY, height=65)
        nav_frame.pack(side="top", fill="x")

        # App Brand Title
        title_box = tk.Frame(nav_frame, bg=self.COLOR_PRIMARY)
        title_box.pack(side="left", padx=20, pady=12)

        lbl_app = tk.Label(title_box, text="💰 SMART EXPENSE TRACKER", font=("Segoe UI", 16, "bold"), bg=self.COLOR_PRIMARY, fg="#FFFFFF")
        lbl_app.pack(side="left")

        lbl_sub = tk.Label(title_box, text=" | Developed by Disha Prajapati", font=("Segoe UI", 10, "bold"), bg=self.COLOR_PRIMARY, fg="#A7F3D0")
        lbl_sub.pack(side="left", padx=10)

        # Right Month Selector & Quick Actions
        actions_box = tk.Frame(nav_frame, bg=self.COLOR_PRIMARY)
        actions_box.pack(side="right", padx=20, pady=12)

        tk.Label(actions_box, text="Active Month:", font=("Segoe UI", 10, "bold"), bg=self.COLOR_PRIMARY, fg="#FFFFFF").pack(side="left", padx=5)
        self.month_entry = ttk.Entry(actions_box, textvariable=self.current_month_var, width=9, justify="center")
        self.month_entry.pack(side="left", padx=5)

        btn_go = ttk.Button(actions_box, text="Update", command=self.refresh_all_views, width=8)
        btn_go.pack(side="left", padx=5)

        btn_new_tx = tk.Button(actions_box, text="+ Add Transaction", font=("Segoe UI", 10, "bold"),
                               bg=self.COLOR_SUCCESS, fg="#FFFFFF", relief="flat", padx=12, pady=4,
                               cursor="hand2", command=self.open_add_transaction_dialog)
        btn_new_tx.pack(side="left", padx=12)

    def _build_notebook_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # Tab Frames
        self.tab_dashboard = ttk.Frame(self.notebook)
        self.tab_transactions = ttk.Frame(self.notebook)
        self.tab_budgets = ttk.Frame(self.notebook)
        self.tab_insights = ttk.Frame(self.notebook)
        self.tab_exports = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_dashboard, text="  📊 Dashboard  ")
        self.notebook.add(self.tab_transactions, text="  📝 Transactions  ")
        self.notebook.add(self.tab_budgets, text="  🎯 Budgets & Goals  ")
        self.notebook.add(self.tab_insights, text="  💡 Smart Insights  ")
        self.notebook.add(self.tab_exports, text="  📂 Reports & Synopsis  ")

        self._build_dashboard_tab()
        self._build_transactions_tab()
        self._build_budgets_tab()
        self._build_insights_tab()
        self._build_exports_tab()

    # =========================================================================
    # TAB 1: DASHBOARD
    # =========================================================================
    def _build_dashboard_tab(self):
        main_frame = tk.Frame(self.tab_dashboard, bg=self.BG_MAIN)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Top 4 Metric Cards
        cards_frame = tk.Frame(main_frame, bg=self.BG_MAIN)
        cards_frame.pack(fill="x", pady=5)
        for i in range(4):
            cards_frame.columnconfigure(i, weight=1)

        self.card_balance = self._create_metric_card(cards_frame, 0, "Net Balance / Savings", "₹0.00", "#10B981")
        self.card_income = self._create_metric_card(cards_frame, 1, "Total Monthly Income", "₹0.00", "#3B82F6")
        self.card_expense = self._create_metric_card(cards_frame, 2, "Total Monthly Expense", "₹0.00", "#EF4444")
        self.card_savings_rate = self._create_metric_card(cards_frame, 3, "Savings Rate", "0%", "#8B5CF6")

        # Split Section: Left = Visual Spending Chart, Right = Recent Transactions List
        content_split = tk.Frame(main_frame, bg=self.BG_MAIN)
        content_split.pack(fill="both", expand=True, pady=10)
        content_split.columnconfigure(0, weight=5)
        content_split.columnconfigure(1, weight=5)
        content_split.rowconfigure(0, weight=1)

        # Left Card: Category Breakdown Chart
        left_card = tk.Frame(content_split, bg="#FFFFFF", relief="ridge", borderwidth=1)
        left_card.grid(row=0, column=0, sticky="nsew", padx=5)

        tk.Label(left_card, text="Spending Breakdown by Category", font=("Segoe UI", 12, "bold"), bg="#FFFFFF", fg="#1E293B").pack(anchor="w", padx=15, pady=(12, 5))
        self.chart_canvas = tk.Canvas(left_card, bg="#FFFFFF", highlightthickness=0, height=260)
        self.chart_canvas.pack(fill="both", expand=True, padx=15, pady=5)

        # Right Card: Recent Transactions & Alerts
        right_card = tk.Frame(content_split, bg="#FFFFFF", relief="ridge", borderwidth=1)
        right_card.grid(row=0, column=1, sticky="nsew", padx=5)

        tk.Label(right_card, text="Recent Transactions", font=("Segoe UI", 12, "bold"), bg="#FFFFFF", fg="#1E293B").pack(anchor="w", padx=15, pady=(12, 5))

        # Mini table for recent records
        cols = ("date", "category", "desc", "amount")
        self.recent_tree = ttk.Treeview(right_card, columns=cols, show="headings", height=8)
        self.recent_tree.heading("date", text="Date")
        self.recent_tree.heading("category", text="Category")
        self.recent_tree.heading("desc", text="Description")
        self.recent_tree.heading("amount", text="Amount")

        self.recent_tree.column("date", width=85, anchor="center")
        self.recent_tree.column("category", width=120, anchor="w")
        self.recent_tree.column("desc", width=160, anchor="w")
        self.recent_tree.column("amount", width=95, anchor="e")
        self.recent_tree.pack(fill="both", expand=True, padx=15, pady=5)

        # Alert Bar
        self.alert_banner = tk.Label(right_card, text="Status: All budgets within safe range.", font=("Segoe UI", 9, "bold"), bg="#ECFDF5", fg="#065F46", pady=6)
        self.alert_banner.pack(fill="x", padx=15, pady=(0, 10))

    def _create_metric_card(self, parent, col, title, value, color_accent):
        card = tk.Frame(parent, bg="#FFFFFF", relief="ridge", borderwidth=1, padx=15, pady=12)
        card.grid(row=0, column=col, sticky="nsew", padx=5)

        # Color strip on top
        strip = tk.Frame(card, bg=color_accent, height=4)
        strip.pack(fill="x", pady=(0, 8))

        lbl_title = tk.Label(card, text=title.upper(), font=("Segoe UI", 8, "bold"), bg="#FFFFFF", fg="#64748B")
        lbl_title.pack(anchor="w")

        lbl_val = tk.Label(card, text=value, font=("Segoe UI", 17, "bold"), bg="#FFFFFF", fg="#0F172A")
        lbl_val.pack(anchor="w", pady=(4, 0))

        return {"title": lbl_title, "val": lbl_val}

    def _render_canvas_chart(self, category_data):
        """Draws a clean modern Donut / Bar chart on Canvas without third-party dependencies."""
        self.chart_canvas.delete("all")
        w = self.chart_canvas.winfo_width() or 450
        h = self.chart_canvas.winfo_height() or 260

        if not category_data:
            self.chart_canvas.create_text(w/2, h/2, text="No expense records for selected month.", font=("Segoe UI", 11), fill="#94A3B8")
            return

        # Draw Bar chart on the left, legend on the right
        chart_w = min(220, w * 0.45)
        cx, cy = chart_w / 2 + 20, h / 2
        radius = min(cx - 25, cy - 20, 80)

        # Draw Pie slices
        start_angle = 0
        palette = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#14B8A6", "#6366F1", "#06B6D4", "#6B7280"]

        for idx, item in enumerate(category_data[:8]):
            color = palette[idx % len(palette)]
            pct = item['percentage']
            extent = (pct / 100.0) * 360.0
            if extent > 0:
                self.chart_canvas.create_arc(
                    cx - radius, cy - radius, cx + radius, cy + radius,
                    start=start_angle, extent=extent, fill=color, outline="#FFFFFF", width=2
                )
                start_angle += extent

        # Center donut hole
        hole_radius = radius * 0.55
        self.chart_canvas.create_oval(
            cx - hole_radius, cy - hole_radius, cx + hole_radius, cy + hole_radius,
            fill="#FFFFFF", outline="#FFFFFF"
        )
        self.chart_canvas.create_text(cx, cy, text="EXPENSES", font=("Segoe UI", 8, "bold"), fill="#64748B")

        # Draw Legend List on Right
        legend_x = cx + radius + 30
        legend_y = 25
        for idx, item in enumerate(category_data[:7]):
            color = palette[idx % len(palette)]
            self.chart_canvas.create_rectangle(legend_x, legend_y, legend_x + 12, legend_y + 12, fill=color, outline="")
            text_desc = f"{item['category']}: ₹{item['amount']:.0f} ({item['percentage']}%)"
            self.chart_canvas.create_text(legend_x + 20, legend_y + 6, text=text_desc, anchor="w", font=("Segoe UI", 9), fill="#334155")
            legend_y += 26

    # =========================================================================
    # TAB 2: TRANSACTIONS
    # =========================================================================
    def _build_transactions_tab(self):
        container = tk.Frame(self.tab_transactions, bg=self.BG_MAIN)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Filters toolbar
        filter_bar = tk.Frame(container, bg="#FFFFFF", relief="ridge", borderwidth=1, padx=12, pady=10)
        filter_bar.pack(fill="x", pady=(0, 10))

        tk.Label(filter_bar, text="Search:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").pack(side="left", padx=4)
        self.search_var = tk.StringVar()
        entry_search = ttk.Entry(filter_bar, textvariable=self.search_var, width=18)
        entry_search.pack(side="left", padx=4)
        entry_search.bind("<KeyRelease>", lambda e: self.load_transactions_data())

        tk.Label(filter_bar, text="Type:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").pack(side="left", padx=(10, 4))
        self.filter_type_var = tk.StringVar(value="All")
        combo_type = ttk.Combobox(filter_bar, textvariable=self.filter_type_var, values=["All", "expense", "income"], state="readonly", width=9)
        combo_type.pack(side="left", padx=4)
        combo_type.bind("<<ComboboxSelected>>", lambda e: self.load_transactions_data())

        btn_filter_reset = ttk.Button(filter_bar, text="Reset Filters", command=self._reset_filters)
        btn_filter_reset.pack(side="left", padx=10)

        # Right Action Buttons
        btn_delete = tk.Button(filter_bar, text="Delete Selected", font=("Segoe UI", 9, "bold"),
                               bg=self.COLOR_DANGER, fg="#FFFFFF", relief="flat", padx=10, pady=3,
                               command=self._delete_selected_transaction)
        btn_delete.pack(side="right", padx=5)

        btn_add = tk.Button(filter_bar, text="+ Add Transaction", font=("Segoe UI", 9, "bold"),
                            bg=self.COLOR_SUCCESS, fg="#FFFFFF", relief="flat", padx=10, pady=3,
                            command=self.open_add_transaction_dialog)
        btn_add.pack(side="right", padx=5)

        # Main Transactions Treeview Table
        table_card = tk.Frame(container, bg="#FFFFFF", relief="ridge", borderwidth=1)
        table_card.pack(fill="both", expand=True)

        columns = ("id", "date", "type", "category", "desc", "amount", "method", "notes")
        self.tx_tree = ttk.Treeview(table_card, columns=columns, show="headings", selectmode="browse")

        self.tx_tree.heading("id", text="ID")
        self.tx_tree.heading("date", text="Date")
        self.tx_tree.heading("type", text="Type")
        self.tx_tree.heading("category", text="Category")
        self.tx_tree.heading("desc", text="Description")
        self.tx_tree.heading("amount", text="Amount (₹)")
        self.tx_tree.heading("method", text="Payment Method")
        self.tx_tree.heading("notes", text="Notes")

        self.tx_tree.column("id", width=45, anchor="center")
        self.tx_tree.column("date", width=95, anchor="center")
        self.tx_tree.column("type", width=80, anchor="center")
        self.tx_tree.column("category", width=140, anchor="w")
        self.tx_tree.column("desc", width=260, anchor="w")
        self.tx_tree.column("amount", width=110, anchor="e")
        self.tx_tree.column("method", width=120, anchor="center")
        self.tx_tree.column("notes", width=180, anchor="w")

        # Scrollbar
        scroll_y = ttk.Scrollbar(table_card, orient="vertical", command=self.tx_tree.yview)
        self.tx_tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.tx_tree.pack(side="left", fill="both", expand=True)

    def _reset_filters(self):
        self.search_var.set("")
        self.filter_type_var.set("All")
        self.load_transactions_data()

    def _delete_selected_transaction(self):
        selected = self.tx_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a transaction to delete.")
            return

        item = self.tx_tree.item(selected[0])
        tx_id = item['values'][0]
        desc = item['values'][4]
        amt = item['values'][5]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete transaction #{tx_id} ({desc} - ₹{amt})?"):
            self.db.delete_transaction(tx_id)
            messagebox.showinfo("Deleted", "Transaction deleted successfully.")
            self.refresh_all_views()

    # =========================================================================
    # TAB 3: BUDGETS & GOALS
    # =========================================================================
    def _build_budgets_tab(self):
        container = tk.Frame(self.tab_budgets, bg=self.BG_MAIN)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Header with form to set budget
        form_card = tk.Frame(container, bg="#FFFFFF", relief="ridge", borderwidth=1, padx=15, pady=12)
        form_card.pack(fill="x", pady=(0, 10))

        tk.Label(form_card, text="Set Monthly Budget Limit", font=("Segoe UI", 11, "bold"), bg="#FFFFFF", fg=self.COLOR_PRIMARY).pack(anchor="w", pady=(0, 8))

        row_box = tk.Frame(form_card, bg="#FFFFFF")
        row_box.pack(fill="x")

        tk.Label(row_box, text="Category:", bg="#FFFFFF", font=("Segoe UI", 9, "bold")).pack(side="left", padx=5)
        self.budget_cat_combo = ttk.Combobox(row_box, state="readonly", width=22)
        self.budget_cat_combo.pack(side="left", padx=5)

        tk.Label(row_box, text="Limit (₹):", bg="#FFFFFF", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(15, 5))
        self.budget_limit_entry = ttk.Entry(row_box, width=12)
        self.budget_limit_entry.pack(side="left", padx=5)

        btn_save_budget = ttk.Button(row_box, text="Save Budget", command=self._save_budget_limit)
        btn_save_budget.pack(side="left", padx=15)

        # Budget Progress Bars Display Area (Scrollable Canvas)
        self.budget_list_canvas = tk.Canvas(container, bg=self.BG_MAIN, highlightthickness=0)
        self.budget_scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.budget_list_canvas.yview)
        self.budget_scroll_frame = tk.Frame(self.budget_list_canvas, bg=self.BG_MAIN)

        self.budget_scroll_frame.bind(
            "<Configure>",
            lambda e: self.budget_list_canvas.configure(scrollregion=self.budget_list_canvas.bbox("all"))
        )
        self.budget_list_canvas.create_window((0, 0), window=self.budget_scroll_frame, anchor="nw")
        self.budget_list_canvas.configure(yscrollcommand=self.budget_scrollbar.set)

        self.budget_scrollbar.pack(side="right", fill="y")
        self.budget_list_canvas.pack(side="left", fill="both", expand=True)

    def _save_budget_limit(self):
        cat = self.budget_cat_combo.get().strip()
        limit_str = self.budget_limit_entry.get().strip()
        month = self.current_month_var.get().strip()

        if not cat or not limit_str:
            messagebox.showerror("Error", "Please select category and enter amount limit.")
            return

        try:
            limit = float(limit_str)
            if limit < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Limit must be a valid positive number.")
            return

        self.db.set_budget(cat, month, limit)
        messagebox.showinfo("Success", f"Budget limit of ₹{limit:.2f} set for {cat} ({month}).")
        self.budget_limit_entry.delete(0, tk.END)
        self.refresh_all_views()

    def _render_budget_bars(self):
        # Clear existing
        for child in self.budget_scroll_frame.winfo_children():
            child.destroy()

        month = self.current_month_var.get().strip()
        budgets = self.db.get_budget_status(month)

        # Update categories combo in budget tab
        cat_names = [b['category_name'] for b in budgets]
        self.budget_cat_combo['values'] = cat_names
        if cat_names and not self.budget_cat_combo.get():
            self.budget_cat_combo.current(0)

        for b in budgets:
            card = tk.Frame(self.budget_scroll_frame, bg="#FFFFFF", relief="ridge", borderwidth=1, padx=15, pady=10)
            card.pack(fill="x", pady=5, padx=2)

            # Row 1: Name and amount info
            r1 = tk.Frame(card, bg="#FFFFFF")
            r1.pack(fill="x")

            lbl_name = tk.Label(r1, text=f"{b['category_icon']}  {b['category_name']}", font=("Segoe UI", 10, "bold"), bg="#FFFFFF", fg="#1E293B")
            lbl_name.pack(side="left")

            limit = b['budget_limit']
            spent = b['actual_spent']
            pct = b['percentage']

            status_text = f"Spent: ₹{spent:.0f} / ₹{limit:.0f} ({pct}%)" if limit > 0 else f"Spent: ₹{spent:.0f} (No Limit Set)"
            lbl_stat = tk.Label(r1, text=status_text, font=("Segoe UI", 9), bg="#FFFFFF", fg="#475569")
            lbl_stat.pack(side="right")

            # Progress bar simulation via Canvas
            p_canvas = tk.Canvas(card, height=14, bg="#E2E8F0", highlightthickness=0)
            p_canvas.pack(fill="x", pady=(6, 2))

            if limit > 0:
                fill_color = self.COLOR_SUCCESS
                if b['status'] == 'Exceeded':
                    fill_color = self.COLOR_DANGER
                elif b['status'] == 'Warning':
                    fill_color = self.COLOR_WARNING

                pct_clamped = min(100.0, pct)
                # Will draw dynamically upon canvas configure
                def draw_bar(c=p_canvas, p=pct_clamped, col=fill_color):
                    c_w = c.winfo_width()
                    if c_w > 0:
                        fill_w = (p / 100.0) * c_w
                        c.create_rectangle(0, 0, fill_w, 14, fill=col, outline="")

                p_canvas.bind("<Configure>", lambda e, c=p_canvas, p=pct_clamped, col=fill_color: draw_bar(c, p, col))

    # =========================================================================
    # TAB 4: SMART INSIGHTS & RULES
    # =========================================================================
    def _build_insights_tab(self):
        container = tk.Frame(self.tab_insights, bg=self.BG_MAIN)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Column: Generated AI Insights
        left_box = tk.Frame(container, bg="#FFFFFF", relief="ridge", borderwidth=1, padx=15, pady=12)
        left_box.pack(side="left", fill="both", expand=True, padx=(0, 5))

        tk.Label(left_box, text="Smart Financial Advice & Alerts", font=("Segoe UI", 12, "bold"), bg="#FFFFFF", fg=self.COLOR_PRIMARY).pack(anchor="w", pady=(0, 10))

        self.insights_listbox = tk.Frame(left_box, bg="#FFFFFF")
        self.insights_listbox.pack(fill="both", expand=True)

        # Right Column: Train Auto-Categorization Rule
        right_box = tk.Frame(container, bg="#FFFFFF", relief="ridge", borderwidth=1, padx=15, pady=12, width=380)
        right_box.pack(side="right", fill="y", padx=(5, 0))
        right_box.pack_propagate(False)

        tk.Label(right_box, text="Train Smart Categorizer", font=("Segoe UI", 12, "bold"), bg="#FFFFFF", fg=self.COLOR_PRIMARY).pack(anchor="w", pady=(0, 6))
        tk.Label(right_box, text="Teach the system new keywords or merchant names so it automatically selects categories for you.",
                 font=("Segoe UI", 8), bg="#FFFFFF", fg="#64748B", wraplength=340, justify="left").pack(anchor="w", pady=(0, 12))

        tk.Label(right_box, text="Keyword / Merchant Name:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").pack(anchor="w")
        self.rule_kw_entry = ttk.Entry(right_box, width=32)
        self.rule_kw_entry.pack(fill="x", pady=(2, 10))

        tk.Label(right_box, text="Map to Category:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").pack(anchor="w")
        self.rule_cat_combo = ttk.Combobox(right_box, state="readonly")
        self.rule_cat_combo.pack(fill="x", pady=(2, 15))

        btn_train = tk.Button(right_box, text="Add Smart Rule", font=("Segoe UI", 9, "bold"),
                              bg=self.COLOR_PRIMARY, fg="#FFFFFF", relief="flat", pady=6,
                              command=self._save_custom_rule)
        btn_train.pack(fill="x")

        # Rules list
        tk.Label(right_box, text="Active Smart Keywords:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").pack(anchor="w", pady=(18, 4))
        self.rules_display = tk.Listbox(right_box, height=12, font=("Segoe UI", 9), relief="solid", borderwidth=1)
        self.rules_display.pack(fill="both", expand=True)

    def _save_custom_rule(self):
        kw = self.rule_kw_entry.get().strip()
        cat = self.rule_cat_combo.get().strip()
        if not kw or not cat:
            messagebox.showerror("Error", "Please provide both keyword and target category.")
            return

        self.categorizer.learn_rule(kw, cat)
        messagebox.showinfo("Trained", f"Smart Rule saved! '{kw}' will now automatically map to '{cat}'.")
        self.rule_kw_entry.delete(0, tk.END)
        self._load_insights_and_rules()

    def _load_insights_and_rules(self):
        # Clear previous insights
        for child in self.insights_listbox.winfo_children():
            child.destroy()

        month = self.current_month_var.get().strip()
        insights = self.analytics.generate_smart_insights(month)

        if not insights:
            tk.Label(self.insights_listbox, text="No active warnings or alerts. Finances look steady!", font=("Segoe UI", 10), bg="#FFFFFF", fg="#64748B").pack(pady=20)
        else:
            for item in insights:
                bg_col = "#EFF6FF"
                border_col = self.COLOR_SECONDARY
                if item['level'] == "CRITICAL":
                    bg_col = "#FEF2F2"
                    border_col = self.COLOR_DANGER
                elif item['level'] == "WARNING":
                    bg_col = "#FFFBEB"
                    border_col = self.COLOR_WARNING
                elif item['level'] == "SUCCESS":
                    bg_col = "#ECFDF5"
                    border_col = self.COLOR_SUCCESS

                card = tk.Frame(self.insights_listbox, bg=bg_col, relief="solid", borderwidth=1, padx=12, pady=10)
                card.pack(fill="x", pady=5)

                lbl_t = tk.Label(card, text=item['title'], font=("Segoe UI", 10, "bold"), bg=bg_col, fg="#0F172A")
                lbl_t.pack(anchor="w")

                lbl_m = tk.Label(card, text=item['message'], font=("Segoe UI", 9), bg=bg_col, fg="#334155", wraplength=480, justify="left")
                lbl_m.pack(anchor="w", pady=(3, 0))

        # Populate combo categories
        all_cats = self.db.get_categories()
        cat_names = [c['name'] for c in all_cats]
        self.rule_cat_combo['values'] = cat_names
        if cat_names and not self.rule_cat_combo.get():
            self.rule_cat_combo.current(0)

        # Populate active rules
        self.rules_display.delete(0, tk.END)
        rules = self.db.get_all_rules()
        for r in rules:
            self.rules_display.insert(tk.END, f"  {r['keyword']}  ➔  {r['category_name']}")

    # =========================================================================
    # TAB 5: EXPORTS & SYNOPSIS
    # =========================================================================
    def _build_exports_tab(self):
        container = tk.Frame(self.tab_exports, bg=self.BG_MAIN)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Two main cards: Exporters and Academic Synopsis Generator
        cards_grid = tk.Frame(container, bg=self.BG_MAIN)
        cards_grid.pack(fill="both", expand=True)
        cards_grid.columnconfigure(0, weight=1)
        cards_grid.columnconfigure(1, weight=1)

        # Card 1: Data Export
        export_card = tk.Frame(cards_grid, bg="#FFFFFF", relief="ridge", borderwidth=1, padx=20, pady=20)
        export_card.grid(row=0, column=0, sticky="nsew", padx=10)

        tk.Label(export_card, text="📊 Data Export & Backup", font=("Segoe UI", 13, "bold"), bg="#FFFFFF", fg=self.COLOR_PRIMARY).pack(anchor="w", pady=(0, 10))
        tk.Label(export_card, text="Export your financial records into spreadsheets or JSON backup files for external record keeping.",
                 font=("Segoe UI", 9), bg="#FFFFFF", fg="#64748B", wraplength=400, justify="left").pack(anchor="w", pady=(0, 20))

        btn_csv = tk.Button(export_card, text="Export Monthly Transactions to CSV", font=("Segoe UI", 10, "bold"),
                            bg=self.COLOR_SECONDARY, fg="#FFFFFF", relief="flat", padx=15, pady=8,
                            command=self._export_csv_action)
        btn_csv.pack(fill="x", pady=6)

        btn_json = tk.Button(export_card, text="Export Full Database Backup (JSON)", font=("Segoe UI", 10, "bold"),
                             bg="#475569", fg="#FFFFFF", relief="flat", padx=15, pady=8,
                             command=self._export_json_action)
        btn_json.pack(fill="x", pady=6)

        # Card 2: Academic Synopsis Generator (PDF)
        pdf_card = tk.Frame(cards_grid, bg="#FFFFFF", relief="ridge", borderwidth=1, padx=20, pady=20)
        pdf_card.grid(row=0, column=1, sticky="nsew", padx=10)

        tk.Label(pdf_card, text="📄 Academic Project Synopsis (6-7 Pages)", font=("Segoe UI", 13, "bold"), bg="#FFFFFF", fg=self.COLOR_PRIMARY).pack(anchor="w", pady=(0, 10))
        tk.Label(pdf_card, text="Generates a comprehensive 6-7 page academic project proposal / synopsis in PDF format, complete with Title Sheet, Introduction, Tools & Tech, Gap Analysis, SDLC Model, Flowcharts, Hardware/Software specs, and Gantt Timeline.",
                 font=("Segoe UI", 9), bg="#FFFFFF", fg="#64748B", wraplength=400, justify="left").pack(anchor="w", pady=(0, 20))

        btn_pdf = tk.Button(pdf_card, text="⚡ Generate 6-7 Page Synopsis PDF", font=("Segoe UI", 10, "bold"),
                            bg=self.COLOR_SUCCESS, fg="#FFFFFF", relief="flat", padx=15, pady=10,
                            command=self._generate_synopsis_action)
        btn_pdf.pack(fill="x", pady=6)

        self.synopsis_status_lbl = tk.Label(pdf_card, text="Ready to generate PDF.", font=("Segoe UI", 9, "italic"), bg="#FFFFFF", fg="#64748B")
        self.synopsis_status_lbl.pack(anchor="w", pady=(15, 0))

    def _export_csv_action(self):
        month = self.current_month_var.get().strip()
        fpath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], initialfile=f"Expense_Report_{month}.csv")
        if fpath:
            count = self.exporter.export_to_csv(fpath, month_year=month)
            messagebox.showinfo("Export Successful", f"Successfully exported {count} transactions to:\n{fpath}")

    def _export_json_action(self):
        fpath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")], initialfile="ExpenseTracker_Backup.json")
        if fpath:
            count = self.exporter.export_to_json(fpath)
            messagebox.showinfo("Backup Successful", f"Successfully exported {count} transactions to:\n{fpath}")

    def _generate_synopsis_action(self):
        try:
            self.synopsis_status_lbl.config(text="Generating Synopsis PDF...", fg=self.COLOR_SECONDARY)
            self.root.update_idletasks()
            
            # Import generator module
            import generate_synopsis_pdf
            pdf_path = generate_synopsis_pdf.build_synopsis_pdf()
            
            self.synopsis_status_lbl.config(text=f"PDF Generated successfully:\n{pdf_path}", fg=self.COLOR_SUCCESS)
            if messagebox.askyesno("PDF Created", f"Synopsis PDF generated successfully!\n\nFile saved at:\n{pdf_path}\n\nWould you like to open it now?"):
                os.startfile(pdf_path)
        except Exception as e:
            self.synopsis_status_lbl.config(text=f"Error: {str(e)}", fg=self.COLOR_DANGER)
            messagebox.showerror("PDF Generation Error", f"Failed to generate synopsis PDF:\n{str(e)}")

    # =========================================================================
    # MODAL DIALOG: ADD TRANSACTION
    # =========================================================================
    def open_add_transaction_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Add New Transaction")
        dlg.geometry("480x560")
        dlg.resizable(False, False)
        dlg.transient(self.root)
        dlg.grab_set()

        dlg.configure(bg="#FFFFFF")

        tk.Label(dlg, text="Record New Transaction", font=("Segoe UI", 13, "bold"), bg="#FFFFFF", fg=self.COLOR_PRIMARY).pack(pady=(15, 10))

        form_frame = tk.Frame(dlg, bg="#FFFFFF", padx=25)
        form_frame.pack(fill="both", expand=True)

        # 1. Type
        tk.Label(form_frame, text="Type:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").grid(row=0, column=0, sticky="w", pady=4)
        type_var = tk.StringVar(value="expense")
        type_box = tk.Frame(form_frame, bg="#FFFFFF")
        type_box.grid(row=0, column=1, sticky="w", pady=4)
        rb_exp = ttk.Radiobutton(type_box, text="Expense", value="expense", variable=type_var)
        rb_inc = ttk.Radiobutton(type_box, text="Income", value="income", variable=type_var)
        rb_exp.pack(side="left", padx=(0, 10))
        rb_inc.pack(side="left")

        # 2. Date
        tk.Label(form_frame, text="Date (YYYY-MM-DD):", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").grid(row=1, column=0, sticky="w", pady=4)
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        entry_date = ttk.Entry(form_frame, textvariable=date_var, width=25)
        entry_date.grid(row=1, column=1, sticky="w", pady=4)

        # 3. Description (With Auto-Categorize hook)
        tk.Label(form_frame, text="Description:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").grid(row=2, column=0, sticky="w", pady=4)
        desc_var = tk.StringVar()
        entry_desc = ttk.Entry(form_frame, textvariable=desc_var, width=25)
        entry_desc.grid(row=2, column=1, sticky="w", pady=4)

        # 4. Category
        tk.Label(form_frame, text="Category:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").grid(row=3, column=0, sticky="w", pady=4)
        cat_combo = ttk.Combobox(form_frame, state="readonly", width=23)
        cat_combo.grid(row=3, column=1, sticky="w", pady=4)

        def populate_categories():
            cats = self.db.get_categories(cat_type=type_var.get())
            cat_combo['values'] = [c['name'] for c in cats]
            if cats:
                cat_combo.current(0)

        populate_categories()
        type_var.trace_add("write", lambda *args: populate_categories())

        # Smart hint label
        lbl_hint = tk.Label(form_frame, text="💡 Tip: Type 'Zomato', 'Uber', 'Electricity', etc.", font=("Segoe UI", 8, "italic"), bg="#FFFFFF", fg="#64748B")
        lbl_hint.grid(row=4, column=1, sticky="w", pady=(0, 4))

        # Auto-detect callback on typing
        def on_desc_change(*args):
            text = desc_var.get()
            if len(text) >= 3:
                predicted, conf = self.categorizer.predict_category(text, type_var.get())
                if predicted and predicted in cat_combo['values']:
                    cat_combo.set(predicted)
                    lbl_hint.config(text=f"✨ Auto-detected: {predicted} ({int(conf*100)}%)", fg=self.COLOR_SUCCESS)
                else:
                    lbl_hint.config(text="💡 Tip: Type 'Zomato', 'Uber', 'Electricity', etc.", fg="#64748B")

        desc_var.trace_add("write", on_desc_change)

        # 5. Amount
        tk.Label(form_frame, text="Amount (₹):", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").grid(row=5, column=0, sticky="w", pady=4)
        amt_var = tk.StringVar()
        entry_amt = ttk.Entry(form_frame, textvariable=amt_var, width=25)
        entry_amt.grid(row=5, column=1, sticky="w", pady=4)

        # 6. Payment Method
        tk.Label(form_frame, text="Payment Method:", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").grid(row=6, column=0, sticky="w", pady=4)
        method_combo = ttk.Combobox(form_frame, values=["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"], state="readonly", width=23)
        method_combo.grid(row=6, column=1, sticky="w", pady=4)
        method_combo.set("UPI")

        # 7. Notes
        tk.Label(form_frame, text="Notes (Optional):", font=("Segoe UI", 9, "bold"), bg="#FFFFFF").grid(row=7, column=0, sticky="nw", pady=4)
        entry_notes = ttk.Entry(form_frame, width=25)
        entry_notes.grid(row=7, column=1, sticky="w", pady=4)

        # Action Buttons
        btn_box = tk.Frame(dlg, bg="#FFFFFF", pady=15)
        btn_box.pack(fill="x")

        def submit_transaction():
            t_date = date_var.get().strip()
            t_type = type_var.get()
            t_desc = desc_var.get().strip()
            t_cat = cat_combo.get().strip()
            t_amt_str = amt_var.get().strip()
            t_method = method_combo.get().strip()
            t_notes = entry_notes.get().strip()

            if not t_date or not t_desc or not t_cat or not t_amt_str:
                messagebox.showerror("Error", "Please fill in all required fields (Date, Description, Category, Amount).")
                return

            try:
                t_amt = float(t_amt_str)
                if t_amt <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Amount must be a valid positive number.")
                return

            self.db.add_transaction(t_date, t_type, t_cat, t_amt, t_desc, t_method, t_notes)
            messagebox.showinfo("Saved", "Transaction added successfully!")
            dlg.destroy()
            self.refresh_all_views()

        btn_save = tk.Button(btn_box, text="Save Transaction", font=("Segoe UI", 10, "bold"),
                             bg=self.COLOR_SUCCESS, fg="#FFFFFF", relief="flat", padx=20, pady=6,
                             command=submit_transaction)
        btn_save.pack(side="right", padx=25)

        btn_cancel = ttk.Button(btn_box, text="Cancel", command=dlg.destroy)
        btn_cancel.pack(side="right", padx=5)

    # =========================================================================
    # DATA REFRESH LOGIC
    # =========================================================================
    def refresh_all_views(self):
        month = self.current_month_var.get().strip()

        # 1. Update Metrics Cards
        summary = self.analytics.get_monthly_summary(month)
        self.card_balance['val'].config(text=f"₹{summary['net_savings']:,.2f}")
        self.card_income['val'].config(text=f"₹{summary['total_income']:,.2f}")
        self.card_expense['val'].config(text=f"₹{summary['total_expense']:,.2f}")
        self.card_savings_rate['val'].config(text=f"{summary['savings_rate']}%")

        # 2. Update Canvas Chart
        cat_data = self.analytics.get_category_breakdown(month, trans_type="expense")
        self._render_canvas_chart(cat_data)

        # 3. Update Recent Transactions
        for row in self.recent_tree.get_children():
            self.recent_tree.delete(row)
        recent_txs = self.db.get_transactions(month_year=month)[:6]
        for tx in recent_txs:
            prefix = "+" if tx['type'] == 'income' else "-"
            amt_display = f"{prefix}₹{tx['amount']:,.2f}"
            self.recent_tree.insert("", "end", values=(tx['date'], tx['category_name'], tx['description'], amt_display))

        # Check Alerts for banner
        budgets = self.db.get_budget_status(month)
        exceeded = [b for b in budgets if b['status'] == 'Exceeded']
        warning = [b for b in budgets if b['status'] == 'Warning']
        if exceeded:
            self.alert_banner.config(text=f"⚠️ Critical: Budget exceeded in {exceeded[0]['category_name']}!", bg="#FEE2E2", fg="#991B1B")
        elif warning:
            self.alert_banner.config(text=f"⚡ Warning: Approaching limit in {warning[0]['category_name']}.", bg="#FEF3C7", fg="#92400E")
        else:
            self.alert_banner.config(text="✅ All category expenses are within budget limits.", bg="#ECFDF5", fg="#065F46")

        # 4. Load Tab Data
        self.load_transactions_data()
        self._render_budget_bars()
        self._load_insights_and_rules()

    def load_transactions_data(self):
        for row in self.tx_tree.get_children():
            self.tx_tree.delete(row)

        month = self.current_month_var.get().strip()
        t_type = self.filter_type_var.get()
        filter_type = None if t_type == "All" else t_type
        search_q = self.search_var.get().strip() or None

        records = self.db.get_transactions(month_year=month, trans_type=filter_type, search_query=search_q)
        for r in records:
            prefix = "+" if r['type'] == 'income' else "-"
            amt_str = f"{prefix}₹{r['amount']:,.2f}"
            self.tx_tree.insert("", "end", values=(
                r['id'], r['date'], r['type'].capitalize(), r['category_name'],
                r['description'], amt_str, r['payment_method'], r['notes']
            ))


def main():
    root = tk.Tk()
    app = SmartExpenseTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

