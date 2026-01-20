from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex
from mortgage import PaymentRow


class AmortizationModel(QAbstractTableModel):
    HEADERS = ["Date", "Principal", "Interest", "Remaining Balance"]

    def __init__(self, rows: list[PaymentRow]):
        super().__init__()
        self.rows = rows

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.rows)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.HEADERS)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        row = self.rows[index.row()]
        col = index.column()

        match col:
            case 0:
                return row.date.strftime("%Y-%m")
            case 1:
                return f"${row.principal:,.2f}"
            case 2:
                return f"${row.interest:,.2f}"
            case 3:
                return f"${row.balance:,.2f}"

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.HEADERS[section]
        return None

