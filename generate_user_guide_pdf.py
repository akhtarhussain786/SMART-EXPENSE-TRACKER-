"""
User Guide & Deployment Manual PDF Generator for Smart Expense Tracker.
Generates an official, step-by-step visual installation and execution manual
so anyone can run the application on any other laptop or PC.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

# Palette
PRIMARY_COLOR = colors.HexColor("#1E3A8A")     # Deep Navy
SECONDARY_COLOR = colors.HexColor("#2563EB")   # Royal Blue
ACCENT_GREEN = colors.HexColor("#0D9488")      # Teal / Dark Emerald
SUCCESS_COLOR = colors.HexColor("#10B981")     # Emerald Green
WARNING_COLOR = colors.HexColor("#D97706")     # Amber
DARK_TEXT = colors.HexColor("#0F172A")         # Slate 900
BODY_TEXT = colors.HexColor("#334155")         # Slate 700
LIGHT_BG = colors.HexColor("#F8FAFC")          # Slate 50
BORDER_COLOR = colors.HexColor("#CBD5E1")      # Slate 300
HIGHLIGHT_BG = colors.HexColor("#F1F5F9")      # Slate 100

class ManualNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        page_num = self._pageNumber
        self.saveState()
        
        # Running Top Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(PRIMARY_COLOR)
        self.drawString(45, 808, "SMART EXPENSE TRACKER - DEPLOYMENT & USER EXECUTION MANUAL")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(550, 808, "STEP-BY-STEP SETUP GUIDE")
        
        self.setStrokeColor(SECONDARY_COLOR)
        self.setLineWidth(1)
        self.line(45, 800, 550, 800)

        # Running Bottom Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.8)
        self.line(45, 45, 550, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(45, 32, "Smart Expense Tracker | Cross-Platform Installation & Execution Manual")
        
        page_str = f"Page {page_num} of {total_pages}"
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(PRIMARY_COLOR)
        self.drawRightString(550, 32, page_str)
        self.restoreState()

def get_manual_styles():
    base = getSampleStyleSheet()
    styles = {
        "ManualTitle": ParagraphStyle(
            "ManualTitle",
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=PRIMARY_COLOR,
            spaceAfter=3
        ),
        "ManualSubtitle": ParagraphStyle(
            "ManualSubtitle",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=BODY_TEXT,
            spaceAfter=12
        ),
        "SectionHeading": ParagraphStyle(
            "SectionHeading",
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=PRIMARY_COLOR,
            spaceBefore=10,
            spaceAfter=5,
            keepWithNext=True
        ),
        "StepTitle": ParagraphStyle(
            "StepTitle",
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=14,
            textColor=SECONDARY_COLOR,
            spaceBefore=6,
            spaceAfter=3,
            keepWithNext=True
        ),
        "BodyText": ParagraphStyle(
            "BodyText",
            fontName="Helvetica",
            fontSize=8.8,
            leading=12.2,
            textColor=DARK_TEXT,
            spaceAfter=4
        ),
        "CodeCommand": ParagraphStyle(
            "CodeCommand",
            fontName="Courier-Bold",
            fontSize=8.5,
            leading=11.5,
            textColor=colors.HexColor("#0F172A")
        ),
        "TableHeader": ParagraphStyle(
            "TableHeader",
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            alignment=1,
            textColor=colors.white
        ),
        "TableCell": ParagraphStyle(
            "TableCell",
            fontName="Helvetica",
            fontSize=8,
            leading=10.5,
            textColor=DARK_TEXT
        ),
        "TableCellBold": ParagraphStyle(
            "TableCellBold",
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10.5,
            textColor=PRIMARY_COLOR
        ),
        "CalloutText": ParagraphStyle(
            "CalloutText",
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=DARK_TEXT
        )
    }
    return styles

def create_code_block(command_text, styles, width=505):
    p = Paragraph(f"<b>&gt; {command_text}</b>", styles["CodeCommand"])
    t = Table([[p]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#38BDF8")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#1E293B")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def create_alert_box(title, text, styles, alert_type="info", width=505):
    bg_color = "#EFF6FF"
    border_color = "#2563EB"
    if alert_type == "warning":
        bg_color = "#FEF3C7"
        border_color = "#D97706"
    elif alert_type == "success":
        bg_color = "#ECFDF5"
        border_color = "#059669"

    content = Paragraph(f"<b>{title}:</b> {text}", styles["CalloutText"])
    t = Table([[content]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(bg_color)),
        ('LINELEFT', (0,0), (0,-1), 3.5, colors.HexColor(border_color)),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def build_user_manual_pdf(output_filename: str = None) -> str:
    if not output_filename:
        docs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
        os.makedirs(docs_dir, exist_ok=True)
        output_filename = os.path.join(docs_dir, "Smart_Expense_Tracker_User_Manual.pdf")

    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=48,
        bottomMargin=48
    )

    styles = get_manual_styles()
    story = []

    # =========================================================================
    # PAGE 1: PREREQUISITES & STEP-BY-STEP SETUP
    # =========================================================================
    story.append(Paragraph("SMART EXPENSE TRACKER - USER MANUAL", styles["ManualTitle"]))
    story.append(Paragraph("Developed by <b>Disha Prajapati</b> | Complete Step-by-Step Guide to Deploy and Run on Any Laptop/PC", styles["ManualSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=8, spaceBefore=0))

    story.append(Paragraph("1. System Prerequisites", styles["SectionHeading"]))
    story.append(Paragraph(
        "Before running this project on a new laptop, ensure the following minimum software environment is installed:",
        styles["BodyText"]
    ))

    prereq_data = [
        [
            Paragraph("<b>Prerequisite Component</b>", styles["TableHeader"]),
            Paragraph("<b>Required Specification</b>", styles["TableHeader"]),
            Paragraph("<b>Download / Verification Note</b>", styles["TableHeader"])
        ],
        [
            Paragraph("<b>Python 3 Environment</b>", styles["TableCellBold"]),
            Paragraph("Python 3.9, 3.10, 3.11, or 3.12", styles["TableCell"]),
            Paragraph("Official installer from <font color='#2563EB'><u>python.org</u></font>", styles["TableCell"])
        ],
        [
            Paragraph("<b>Package Manager (pip)</b>", styles["TableCellBold"]),
            Paragraph("Pip 22.0 or higher", styles["TableCell"]),
            Paragraph("Bundled automatically with standard Python installer", styles["TableCell"])
        ],
        [
            Paragraph("<b>Operating System</b>", styles["TableCellBold"]),
            Paragraph("Windows 10/11, macOS, or Linux", styles["TableCell"]),
            Paragraph("Fully cross-platform (No OS-specific dependencies)", styles["TableCell"])
        ],
        [
            Paragraph("<b>Web Browser</b>", styles["TableCellBold"]),
            Paragraph("Chrome, Edge, Firefox, or Safari", styles["TableCell"]),
            Paragraph("Required to view the Web Application Dashboard", styles["TableCell"])
        ]
    ]
    prereq_table = Table(prereq_data, colWidths=[130, 160, 215])
    prereq_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, HIGHLIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(prereq_table)
    story.append(Spacer(1, 6))

    story.append(create_alert_box(
        "CRITICAL STEP DURING PYTHON INSTALLATION",
        "When installing Python on Windows, make sure to <b>CHECK</b> the box at the bottom that says: <i>'Add python.exe to PATH'</i>. If you skip this, terminal commands like 'python' or 'pip' will not be recognized.",
        styles,
        alert_type="warning"
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. Transferring and Extracting the Project", styles["SectionHeading"]))
    story.append(Paragraph(
        "<b>Step 1:</b> Copy the complete project folder (<code>SmartExpenseTracker</code>) to a Pen Drive, Google Drive, or transfer as a ZIP archive.<br/>"
        "<b>Step 2:</b> On the destination laptop, paste and extract the folder to any convenient location (e.g., <code>D:\\SmartExpenseTracker</code> or <code>C:\\Users\\YourName\\Desktop\\SmartExpenseTracker</code>).",
        styles["BodyText"]
    ))

    story.append(Paragraph("3. Installing Required Python Dependencies", styles["SectionHeading"]))
    story.append(Paragraph(
        "Open Command Prompt (cmd) or PowerShell, navigate to the project directory, and install required libraries:",
        styles["BodyText"]
    ))

    story.append(create_code_block("cd D:\\SmartExpenseTracker", styles))
    story.append(Spacer(1, 4))
    story.append(create_code_block("pip install -r requirements.txt", styles))
    story.append(Spacer(1, 6))

    story.append(create_alert_box(
        "What does requirements.txt install?",
        "It installs <b>FastAPI</b>, <b>Uvicorn</b> (for the web interface), <b>ReportLab</b> (for academic PDF generation), and <b>PyMuPDF</b>. Standard modules like <code>sqlite3</code> and <code>tkinter</code> are already built into Python.",
        styles,
        alert_type="info"
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: RUNNING WEB APP, DESKTOP APP & TESTING
    # =========================================================================
    story.append(Paragraph("4. How to Run the Web Application (Website Interface)", styles["SectionHeading"]))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_COLOR, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph(
        "The Web Application provides a modern browser-based interface where users can view charts, add transactions with live auto-categorization, and remove expenses with a single click.",
        styles["BodyText"]
    ))

    story.append(Paragraph("Method A: Quick One-Click Double-Click (Easiest for Non-Technical Users)", styles["StepTitle"]))
    story.append(Paragraph(
        "1. Open the project folder in Windows File Explorer.<br/>"
        "2. Double-click the file named <b><code>run_web.bat</code></b>.<br/>"
        "3. A black console window will open, and your web browser will automatically open to <b><code>http://127.0.0.1:8000</code></b>!",
        styles["BodyText"]
    ))

    story.append(Paragraph("Method B: Terminal / Command Prompt Command", styles["StepTitle"]))
    story.append(Paragraph("Run the Python runner script from terminal:", styles["BodyText"]))
    story.append(create_code_block("python run_web.py", styles))
    story.append(Spacer(1, 6))

    story.append(create_alert_box(
        "How to Add & Remove Expenses on the Web App",
        "• <b>To Add Expense:</b> Click <b>'+ Add Expense'</b> at the top. Type a description (e.g., 'Swiggy dinner', 'Uber cab', 'Electricity bill') — the system auto-detects the category! Enter amount and click <b>'Save'</b>.<br/>"
        "• <b>To Remove Expense:</b> In the transactions table, find the expense and click the <b>🗑️ (Trash Icon)</b>. Confirm the popup prompt, and the transaction is instantly deleted from SQLite database.",
        styles,
        alert_type="success"
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5. How to Run the Native Desktop Application (Tkinter GUI)", styles["SectionHeading"]))
    story.append(Paragraph(
        "If you want to use the native desktop standalone software with tabs, canvas vector graphics, and rule-training:",
        styles["BodyText"]
    ))
    story.append(create_code_block("python app.py", styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph("6. Initializing Realistic Demo Data (Optional for Evaluation/Viva)", styles["SectionHeading"]))
    story.append(Paragraph(
        "If you are demonstrating the project to an examiner, professor, or client and need realistic transactions, budgets, and charts pre-populated immediately, run:",
        styles["BodyText"]
    ))
    story.append(create_code_block("python sample_data.py", styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph("7. Generating the Official 7-Page Academic Synopsis PDF", styles["SectionHeading"]))
    story.append(Paragraph(
        "The project includes an automated ReportLab generator that produces a submission-ready 7-page academic synopsis PDF covering Introduction, Literature Review, Comparative Matrix, SDLC Model, Flowcharts, and Gantt Timeline:",
        styles["BodyText"]
    ))
    story.append(create_code_block("python generate_synopsis_pdf.py", styles))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The generated PDF is saved at: <code>docs/Smart_Expense_Tracker_Synopsis.pdf</code>.",
        styles["BodyText"]
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: TROUBLESHOOTING & COMMON FAQS
    # =========================================================================
    story.append(Paragraph("8. Troubleshooting & Frequently Asked Questions (FAQ)", styles["SectionHeading"]))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY_COLOR, spaceAfter=8, spaceBefore=2))

    story.append(Paragraph(
        "If you encounter any unexpected issues on a new laptop, refer to the diagnostic matrix below:",
        styles["BodyText"]
    ))

    faq_data = [
        [
            Paragraph("<b>Error / Symptom</b>", styles["TableHeader"]),
            Paragraph("<b>Root Cause</b>", styles["TableHeader"]),
            Paragraph("<b>Immediate Solution & Fix</b>", styles["TableHeader"])
        ],
        [
            Paragraph("<b>'python' is not recognized as an internal or external command</b>", styles["TableCellBold"]),
            Paragraph("Python was installed without checking 'Add to PATH'.", styles["TableCell"]),
            Paragraph("Re-run the Python installer, select <b>'Modify'</b>, and check <b>'Add Python to PATH'</b>. Alternatively, search 'Environment Variables' and add Python install path.", styles["TableCell"])
        ],
        [
            Paragraph("<b>ModuleNotFoundError: No module named 'fastapi' or 'reportlab'</b>", styles["TableCellBold"]),
            Paragraph("Dependencies have not yet been installed in current Python environment.", styles["TableCell"]),
            Paragraph("Run command: <code>pip install -r requirements.txt</code>. Ensure your computer is connected to the internet during install.", styles["TableCell"])
        ],
        [
            Paragraph("<b>Error: Port 8000 is already in use</b>", styles["TableCellBold"]),
            Paragraph("Another process (or previous instance of web_app) is running on port 8000.", styles["TableCell"]),
            Paragraph("Open <code>web_app.py</code> and change <code>port=8000</code> to <code>port=8080</code> or <code>port=5000</code>, then restart.", styles["TableCell"])
        ],
        [
            Paragraph("<b>Browser does not open automatically</b>", styles["TableCellBold"]),
            Paragraph("Default browser handler delayed or restricted by Windows security.", styles["TableCell"]),
            Paragraph("Manually open Google Chrome, Microsoft Edge, or Firefox, and type <b><code>http://127.0.0.1:8000</code></b> in the address bar.", styles["TableCell"])
        ],
        [
            Paragraph("<b>Where is transaction data stored?</b>", styles["TableCellBold"]),
            Paragraph("Local storage persistence.", styles["TableCell"]),
            Paragraph("All data is stored locally in <code>expense_tracker.db</code> (SQLite). If you move the folder, all data stays intact with 100% privacy.", styles["TableCell"])
        ]
    ]

    faq_table = Table(faq_data, colWidths=[140, 150, 215])
    faq_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, HIGHLIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(faq_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("9. Project Quick Reference Summary Sheet", styles["SectionHeading"]))
    
    summary_data = [
        [
            Paragraph("<b>Feature / Objective</b>", styles["TableHeader"]),
            Paragraph("<b>Terminal Command</b>", styles["TableHeader"]),
            Paragraph("<b>Expected Output</b>", styles["TableHeader"])
        ],
        [
            Paragraph("Launch Web Interface", styles["TableCellBold"]),
            Paragraph("<code>python run_web.py</code>", styles["TableCell"]),
            Paragraph("Opens web dashboard at http://127.0.0.1:8000", styles["TableCell"])
        ],
        [
            Paragraph("Launch Desktop GUI", styles["TableCellBold"]),
            Paragraph("<code>python app.py</code>", styles["TableCell"]),
            Paragraph("Opens native Tkinter desktop application window", styles["TableCell"])
        ],
        [
            Paragraph("Populate Demo Data", styles["TableCellBold"]),
            Paragraph("<code>python sample_data.py</code>", styles["TableCell"]),
            Paragraph("Seeds realistic transactions, budgets & categories", styles["TableCell"])
        ],
        [
            Paragraph("Generate Synopsis PDF", styles["TableCellBold"]),
            Paragraph("<code>python generate_synopsis_pdf.py</code>", styles["TableCell"]),
            Paragraph("Generates 7-Page Academic Synopsis PDF", styles["TableCell"])
        ]
    ]
    summary_table = Table(summary_data, colWidths=[140, 175, 190])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, HIGHLIGHT_BG]),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(summary_table)

    doc.build(story, canvasmaker=ManualNumberedCanvas)
    return output_filename

if __name__ == "__main__":
    generated_file = build_user_manual_pdf()
    print(f"[SUCCESS] User Manual PDF generated at: {generated_file}")

