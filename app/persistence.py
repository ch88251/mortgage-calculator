import csv
from mortgage import PaymentRow


def export_amortization_csv(path: str, rows: list[PaymentRow]):
    """
    Export full amortization schedule to CSV.
    """
    with open(path, mode="w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Date",
            "Principal Paid",
            "Interest Paid",
            "Remaining Balance"
        ])

        for row in rows:
            writer.writerow([
                row.date.isoformat(),
                f"{row.principal:.2f}",
                f"{row.interest:.2f}",
                f"{row.balance:.2f}",
            ])

