import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date()
            if not date
            else dt.datetime.strptime(date, '%d.%m.%Y').date()
        )
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # [Pylint: W0621(redefined-outer-name), Calculator.get_today_stats]
        # Redefining name 'Record' from outer scope (line 4)
        # [Pylint: C0103(invalid-name), Calculator.get_today_stats]
        # Variable name "Record" doesn't conform to '(([a-z][a-z0-9_]{2,30})|(_[a-z0-9_]*))$' pattern
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (today - record.date).days < 7 and (
                    today - record.date
            ).days >= 0:
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        # [Pylint: R1705(no-else-return), CaloriesCalculator.get_calories_remained] Unnecessary "else" after "return"
        if x > 0:
            return (
                f'Сегодня можно съесть что-нибудь'
                f' ещё, но с общей калорийностью не более {x} кКал'
            )
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # [Pylint: C0103(invalid-name), CashCalculator.get_today_cash_remained]
    # Argument name "EURO_RATE" doesn't conform to '(([a-z][a-z0-9_]{2,45})|(_[a-z0-9_]*))$' pattern
    # [Pylint: C0103(invalid-name), CashCalculator.get_today_cash_remained]
    # Argument name "USD_RATE" doesn't conform to '(([a-z][a-z0-9_]{2,45})|(_[a-z0-9_]*))$' pattern
    # [Pylint: R1710(inconsistent-return-statements), CashCalculator.get_today_cash_remained]
    # Either all return statements in a function should return an expression, or none of them should.
    def get_today_cash_remained(
            self, currency, USD_RATE=USD_RATE, EURO_RATE=EURO_RATE,
    ):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # [Pylint: W0104(pointless-statement), CashCalculator.get_today_cash_remained]
            # Statement seems to have no effect
            cash_remained == 1.00
            currency_type = 'руб'
        # [Pylint: R1705(no-else-return), CashCalculator.get_today_cash_remained] Unnecessary "elif" after "return"
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' ' твой долг - {0:.2f} {1}'.format(
                -cash_remained, currency_type,
            )

    def get_week_stats(self):
        # [Pylint: W0235(useless-super-delegation), CashCalculator.get_week_stats]
        # Useless super delegation in method 'get_week_stats'
        super().get_week_stats()
