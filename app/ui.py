from datetime import date
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QGridLayout, QFileDialog,
    QMessageBox, QTableView, QTabWidget, QHBoxLayout
)

from mortgage import MortgageInputs, amortize
from amortization_model import AmortizationModel
from chart import create_payoff_chart
from persistence import export_amortization_csv


class MortgageCalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mortgage Payoff Calculator")
        self.resize(900, 600)
        self.current_schedule = None

        main_layout = QVBoxLayout(self)

        # ---------- INPUT FORM ----------
        form_layout = QGridLayout()

        self.balance_edit = QLineEdit("142044.18")
        self.rate_edit = QLineEdit("2.25")
        self.payment_edit = QLineEdit("2500.00")
        self.extra_edit = QLineEdit("300.00")

        form_layout.addWidget(QLabel("Current Balance ($)"), 0, 0)
        form_layout.addWidget(self.balance_edit, 0, 1)

        form_layout.addWidget(QLabel("Interest Rate (%)"), 1, 0)
        form_layout.addWidget(self.rate_edit, 1, 1)

        form_layout.addWidget(QLabel("Monthly Payment ($)"), 2, 0)
        form_layout.addWidget(self.payment_edit, 2, 1)

        form_layout.addWidget(QLabel("Extra Principal ($)"), 3, 0)
        form_layout.addWidget(self.extra_edit, 3, 1)

        main_layout.addLayout(form_layout)

        # ---------- BUTTON BAR ----------
        button_layout = QHBoxLayout()

        self.calculate_btn = QPushButton("Calculate")
        self.save_btn = QPushButton("Export CSV")
        self.load_btn = QPushButton("Load Scenario")

        self.calculate_btn.clicked.connect(self.calculate)
        self.save_btn.clicked.connect(self.export_csv)
        self.load_btn.clicked.connect(self.load)

        button_layout.addWidget(self.calculate_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.load_btn)

        main_layout.addLayout(button_layout)

        # ---------- RESULTS TABS ----------
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

    # ------------------------------------------------------------------
    # Core logic
    # ------------------------------------------------------------------

    def build_inputs(self) -> MortgageInputs:
        return MortgageInputs(
            balance=float(self.balance_edit.text()),
            annual_rate=float(self.rate_edit.text()) / 100.0,
            monthly_payment=float(self.payment_edit.text()),
            extra_principal=float(self.extra_edit.text()),
            next_payment_date=date.today(),
        )

    def calculate(self):
        try:
            inputs = self.build_inputs()
            schedule = amortize(inputs)
            self.current_schedule = schedule

            model = AmortizationModel(schedule)
            table = QTableView()
            table.setModel(model)
            table.resizeColumnsToContents()

            chart_view = create_payoff_chart(schedule)

            self.tabs.clear()
            self.tabs.addTab(table, "Amortization Table")
            self.tabs.addTab(chart_view, "Payoff Chart")

        except Exception as e:
            QMessageBox.critical(self, "Calculation Error", str(e))

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def export_csv(self):
        if not self.current_schedule:
            QMessageBox.warning(
                self,
                "Nothing to Export",
                "Please calculate the mortgage first."
            )
            return

        try:
            path, _ = QFileDialog.getSaveFileName(
                self,
                "Export Amortization Schedule",
                "",
                "CSV Files (*.csv)"
            )
            if not path:
                return

            export_amortization_csv(path, self.current_schedule)

        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))


    def load(self):
        try:
            path, _ = QFileDialog.getOpenFileName(
                self, "Load Scenario", "", "CSV Files (*.csv)"
            )
            if not path:
                return

            # Load the CSV and display it
            import csv
            from mortgage import PaymentRow
            from datetime import datetime
            
            schedule = []
            with open(path, mode="r") as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    schedule.append(PaymentRow(
                        date=datetime.fromisoformat(row[0]).date(),
                        principal=float(row[1]),
                        interest=float(row[2]),
                        balance=float(row[3])
                    ))
            
            self.current_schedule = schedule
            
            model = AmortizationModel(schedule)
            table = QTableView()
            table.setModel(model)
            table.resizeColumnsToContents()

            chart_view = create_payoff_chart(schedule)

            self.tabs.clear()
            self.tabs.addTab(table, "Amortization Table")
            self.tabs.addTab(chart_view, "Payoff Chart")

        except Exception as e:
            QMessageBox.critical(self, "Load Error", str(e))

