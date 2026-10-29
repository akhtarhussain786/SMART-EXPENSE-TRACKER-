# 💰 Smart Expense Tracker (Python Desktop Application)

An intelligent, privacy-first personal financial management application built in Python. Features real-time heuristic auto-categorization, proactive budget threshold alerts, vector visual charts, and automated academic synopsis PDF generation.

---

## 🚀 Key Features

1. **Smart Auto-Categorization (Rule & History AI)**:
   - Automatically detects categories as you type descriptions (e.g., typing *"Uber"* auto-selects **Transportation**, *"Zomato"* selects **Food & Dining**, *"BESCOM"* selects **Utilities**).
   - Allows users to train custom keyword rules directly from the GUI.

2. **Interactive Financial Dashboard**:
   - Live KPI cards: **Net Balance / Savings**, **Monthly Income**, **Monthly Expense**, and **Savings Rate %**.
   - Custom vector Donut Spending Chart rendered dynamically on Canvas.
   - Real-time budget warning banners.

3. **Budget Planner & Overrun Protection**:
   - Set monthly budgets per expense category.
   - Dynamic color-coded progress bars:
     - 🟢 **Normal**: < 80% of budget spent
     - 🟡 **Warning**: 80% - 100% of budget spent
     - 🔴 **Critical**: > 100% (Budget Exceeded)

4. **Actionable Financial Insights**:
   - Automated rule-based advice regarding savings rate benchmarks, highest spending category concentrations, and daily burn rates.

5. **Multi-Format Export & Academic Synopsis PDF Generator**:
   - Export filtered transactions to standard **CSV** spreadsheets.
   - Full database backup to **JSON**.
   - One-click generation of the official **7-page College Project Synopsis PDF**.

---

## 📁 Project Architecture

```
d:\dishaProjects\SmartExpenseTracker\
├── app.py                      # Main Tkinter Desktop Application (Modern UI)
├── database.py                 # SQLite database schema, connections, and CRUD
├── categorizer.py              # Heuristic & history-based auto-categorizer engine
├── analytics.py                # Financial aggregation & automated advice engine
├── exporter.py                 # CSV & JSON data export routines
├── sample_data.py              # Realistic demo dataset generator
├── generate_synopsis_pdf.py    # ReportLab script producing the 7-page academic synopsis PDF
├── requirements.txt            # Python package dependencies
├── README.md                   # Project documentation
└── docs/
    └── Smart_Expense_Tracker_Synopsis.pdf  # Generated 7-page Academic Synopsis
```

---

## 🌐 Web Application Interface (NEW!)

A responsive, modern web dashboard built with **FastAPI** and **Tailwind CSS + Chart.js**.

### To Run the Web Application:
```bash
python run_web.py
```
*Or simply double-click `run_web.bat` in Windows Explorer.*

This will automatically open your default browser at `http://127.0.0.1:8000`:
- **Add Expense & Income:** Modal form with live auto-detection as you type description (e.g. typing *Zomato*, *Uber*, *Blinkit*).
- **Remove / Delete Expense:** Single-click 🗑️ trash icon to instantly remove any expense with real-time UI updates.
- **Search & Filter:** Live search bar and type filters (Expenses only / Income only).
- **Interactive Visuals:** Dynamic category donut chart with tooltips and responsive budget progress bars with threshold alerts.

---

## 🖥️ Desktop Application (Tkinter)

To run the native desktop version:
```bash
python app.py
```

### 1. Prerequisites
- Python 3.9 or higher (tested on Python 3.11).
- Standard Tkinter support (included with standard Python for Windows/macOS).

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Seed Realistic Demo Data (Optional)
```bash
python sample_data.py
```

### 4. Launch the Desktop Application
```bash
python app.py
```

---

## 📄 Generating the 6 to 7 Page Project Synopsis PDF

You can generate the official academic project synopsis in two ways:

### Option A: From Command Line
```bash
python generate_synopsis_pdf.py
```
*The PDF will be generated and saved at `docs/Smart_Expense_Tracker_Synopsis.pdf`.*

### Option B: From the Application UI
1. Launch `python app.py`
2. Navigate to the **"📂 Reports & Synopsis"** tab.
3. Click on **"⚡ Generate 6-7 Page Synopsis PDF"**.
4. The system generates the PDF and asks if you would like to open it immediately.

---

## 📋 Synopsis Sections Covered (7 Pages Academic Structure)

| Page # | Section Title | Contents |
|---|---|---|
| **Page 1** | **Academic Title & Cover Sheet** | Project Title, Student Details, Guide Details, University/Department Info, Academic Session |
| **Page 2** | **1. Introduction & Problem Formulation** | Project Background, Problem Statement, Primary/Secondary Objectives, Scope & Boundaries |
| **Page 3** | **2. Literature Review & Gap Analysis** | Existing Systems (Excel vs Commercial Cloud Apps), Novelty, Detailed Comparison Matrix Table |
| **Page 4** | **3. Tools & Technology Stack** | Python 3.11, Tkinter/TTK, SQLite3, ReportLab, Model-View-Controller (MVC) Architecture |
| **Page 5** | **4. Preliminary Investigation & SDLC** | Feasibility Analysis (Technical, Economic, Operational), Agile-Waterfall Hybrid SDLC Model |
| **Page 6** | **5. System Workflow & Project Timeline** | 5-Step System Workflow, Work Breakdown Structure, 16-Week Gantt Chart Schedule Table |
| **Page 7** | **6. System Requirements, Testing & Conclusion** | Hardware/Software Specs, Database Schema, Testing Plan (Unit/Boundary), Future Scope & Signatures |

