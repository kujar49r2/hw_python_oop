import datetime as dt
from typing import Optional, Union

date_format = "%d.%m.%Y"


class Record:
    def __init__(
        self, amount: Union[int, float], comment: str, date: Optional[str] = None
    ) -> None:
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, date_format).date()
        else:
            self.date = dt.datetime.now().date()


class Calculator:
    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.records: list[Record] = []

    def add_record(self, record: Record):
        """Сохранять новую запись о расходах/приёме пищи"""
        self.records.append(record)

    def get_today_stats(self):
        """Считать, сколько денег/калорий потрачено/съедено сегодня"""
        return sum(
            record.amount for record in self.records if record.date == dt.date.today()
        )

    def get_rest(self) -> float:
        """Сколько осталось денег/калорий"""
        return self.limit - self.get_today_stats()

    def get_week_stats(self):
        """Считать, сколько денег/калорий потрачено за последние 7 дней"""
        today = dt.date.today()
        week_start = today - dt.timedelta(days=7)
        return sum(
            record.amount
            for record in self.records
            if week_start <= record.date <= today
        )


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        balance_of_cal = self.get_rest()
        if balance_of_cal > 0:
            return f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {balance_of_cal} кКал"
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):
    RUB_RATE = 1.00
    USD_RATE = 92.00
    EURO_RATE = 102.00

    def get_today_cash_remained(self, currency: str):
        """Определять, сколько ещё денег можно потратить сегодня в рублях,
        долларах или евро"""

        balance_in_rub = self.get_rest()

        balance_in_different_currencies: dict[str, tuple[float, str]] = {
            "rub": (balance_in_rub / self.RUB_RATE, "руб"),
            "usd": (balance_in_rub / self.USD_RATE, "USD"),
            "eur": (balance_in_rub / self.EURO_RATE, "Euro"),
        }
        if currency not in balance_in_different_currencies:
            return "<выбрана неверная валюта>"

        balance_in_selected_currency, currency_name = balance_in_different_currencies[
            currency
        ]

        if balance_in_rub > 0:
            return f"На сегодня осталось {round(balance_in_selected_currency, 2)} {currency_name}"
        elif balance_in_rub == 0:
            return "Денег нет, держись"
        else:
            return f"Денег нет, держись: твой долг - {round(abs(balance_in_selected_currency), 2)} {currency_name}"


if __name__ == "__main__":
    limit = 1000
    cash_calculator = CashCalculator(limit)
    calories_calculator = CaloriesCalculator(limit)

    # записи для денег
    r1 = Record(amount=300, comment="кофе")
    r2 = Record(amount=300, comment="Серёге за обед")
    r3 = Record(amount=1000, comment="Бар на день рождения", date="19.11.2023")

    # записи для калорий
    r4 = Record(amount=118, comment="Кусок тортика. И ещё один.")
    r5 = Record(amount=84, comment="Йогурт.")
    r6 = Record(amount=1140, comment="Баночка чипсов.", date="24.02.2019")

    cash_calculator.add_record(r1)
    cash_calculator.add_record(r2)
    cash_calculator.add_record(r3)

    calories_calculator.add_record(r4)
    calories_calculator.add_record(r5)
    calories_calculator.add_record(r6)

    print(cash_calculator.get_today_stats())
    print(calories_calculator.get_today_stats())

    # вывод результатов
    print(cash_calculator.get_today_cash_remained("rub"))
    # print(calories_calculator.get_calories_remained())
