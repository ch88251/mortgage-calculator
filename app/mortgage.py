from dataclasses import dataclass
from datetime import date
from calendar import monthrange


def add_months(d: date, months: int) -> date:
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    last_day = monthrange(y, m)[1]
    return date(y, m, min(d.day, last_day))


@dataclass
class PaymentRow:
    date: date
    balance: float
    principal: float
    interest: float


@dataclass
class MortgageInputs:
    balance: float
    annual_rate: float
    monthly_payment: float
    extra_principal: float
    next_payment_date: date


def amortize(inputs: MortgageInputs) -> list[PaymentRow]:
    balance = inputs.balance
    monthly_rate = inputs.annual_rate / 12
    cursor = inputs.next_payment_date

    schedule: list[PaymentRow] = []

    while balance > 0:
        interest = balance * monthly_rate
        principal = (inputs.monthly_payment + inputs.extra_principal) - interest

        if principal <= 0:
            raise ValueError("Payment does not cover interest.")

        principal = min(principal, balance)
        balance -= principal

        schedule.append(
            PaymentRow(
                date=cursor,
                balance=round(balance, 2),
                principal=round(principal, 2),
                interest=round(interest, 2),
            )
        )

        if balance <= 0:
            break

        cursor = add_months(cursor, 1)

    return schedule

