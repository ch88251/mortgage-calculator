from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QGridLayout, QMessageBox
)
from datetime import date
from mortgage import MortgageInputs, calculate_payoff


class MortgageCalculatorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mortgage Payoff Calculator")

        layout = QGridLayout(self)

        # Inputs
        self.balance = QLineEdit("142044.18")
        self.rate = QLineEdit("2.25")
        self.payment = QLineEdit("2500.00")
        self.extra = QLineEdit("300.00")

        layout.addWidget(QLabel("Current Balance ($):"), 0, 0)
        layout.addWidget(self.balance, 0, 1)

        layout.addWidget(QLabel("Interest Rate (%):"), 1, 0)
        layout.addWidget(self.rate, 1, 1)

        layout.addWidget(QLabel("Monthly Payment ($):"), 2, 0)
        layout.addWidget(self.payment, 2, 1)

        layout.addWidget(QLabel("Extra Principal ($):"), 3, 0)
        layout.addWidget(self.extra, 3, 1)

        # Button
        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_btn, 4, 0, 1, 2)

        # Output
        self.result_label = QLabel("")
        layout.addWidget(self.result_label, 5, 0, 1, 2)

    def calculate(self):
        try:
            inputs = MortgageInputs(
                balance=float(self.balance.text()),
                annual_rate=float(self.rate.text()) / 100,
                monthly_payment=float(self.payment.text()),
                extra_principal=float(self.extra.text()),
                next_payment_date=date.today(),
            )

            result = calculate_payoff(inputs)

            self.result_label.setText(
                f"Payoff Date: {result.payoff_date.strftime('%B %Y')}\n"
                f"Payments Remaining: {result.months}\n"
                f"Total Interest: ${result.total_interest:,.2f}"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

