from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtGui import QPainter
from mortgage import PaymentRow


def create_payoff_chart(schedule: list[PaymentRow]) -> QChartView:
    series = QLineSeries()
    series.setName("Remaining Balance")

    for i, row in enumerate(schedule):
        series.append(i, row.balance)

    chart = QChart()
    chart.addSeries(series)
    chart.createDefaultAxes()
    chart.setTitle("Mortgage Payoff Over Time")

    view = QChartView(chart)
    view.setRenderHint(QPainter.Antialiasing)
    return view

