from dataclasses import dataclass
from datetime import date
from calendar import monthrange


def add_months(d: date, months: int) -> date:
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    last_day = monthrange(y, m)[1]
    return date(y, m, min(d.day, last_day))


@dataclass
class MortgageInputs:
    balance: float
    annual_rate: float
    monthly_payment: float
    extra_principal: float
    next_payment_date: date


@dataclass
class MortgageResult:
    payoff_date: date
    months: int
    total_interest: float


def calculate_payoff(inputs: MortgageInputs) -> MortgageResult:
    balance = inputs.balance
    monthly_rate = inputs.annual_rate / 12
    date_cursor = inputs.next_payment_date

    months = 0
    total_interest = 0.0

    while balance > 0:
        interest = balance * monthly_rate
        total_interest += interest

        principal = (inputs.monthly_payment + inputs.extra_principal) - interest
        if principal <= 0:
            raise ValueError("Payment does not cover interest.")

        principal = min(principal, balance)
        balance -= principal

        months += 1
        if balance <= 0:
            break

        date_cursor = add_months(date_cursor, 1)

    return MortgageResult(
        payoff_date=date_cursor,
        months=months,
        total_interest=round(total_interest, 2),
    )

