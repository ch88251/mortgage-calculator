import sys
from PySide6.QtWidgets import QApplication
from ui import MortgageCalculatorUI


def main():
    app = QApplication(sys.argv)
    window = MortgageCalculatorUI()
    window.resize(420, 250)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

