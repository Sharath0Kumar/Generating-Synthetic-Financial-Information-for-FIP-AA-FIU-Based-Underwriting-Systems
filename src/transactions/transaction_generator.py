import random
from datetime import datetime, timedelta

from src.temporal.hawkes_generator import HawkesGenerator


class TransactionGenerator:

    def __init__(
        self,
        seed=42,
        opening_balance=5000,
        use_hawkes=True
    ):
        self.random = random.Random(seed)
        self.opening_balance = opening_balance
        self.use_hawkes = use_hawkes

    def generate_transactions(
        self,
        customer,
        financial_profile,
        start_date,
        months=1
    ):
        all_transactions = []

        start_date = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        )

        monthly_income = financial_profile["monthly_income"]
        expenses = financial_profile["essential_expenses"]
        debt = financial_profile["debt_burden"]
        discretionary = financial_profile["discretionary_spending"]
        investment = financial_profile["investment"]

        # Generate transactions month by month
        for month_index in range(months):

            month_start = self._add_months(
                start_date,
                month_index
            )

            monthly_transactions = self._generate_month(
                customer=customer,
                monthly_income=monthly_income,
                expenses=expenses,
                debt=debt,
                discretionary=discretionary,
                investment=investment,
                month_start=month_start
            )

            all_transactions.extend(
                monthly_transactions
            )

        # Sort all transactions chronologically
        all_transactions.sort(
            key=lambda x: x["timestamp"]
        )

        # Calculate running balance
        self._add_running_balance(
            all_transactions
        )

        # ---------------------------------------------------------
        # ACCOUNT-LEVEL OPENING AND CLOSING BALANCE
        # ---------------------------------------------------------

        # Balance before the first transaction
        opening_balance = self.opening_balance

        # Balance after the final transaction
        if all_transactions:
            closing_balance = all_transactions[-1]["balance"]
        else:
            closing_balance = opening_balance

        return {
            "customer_id": customer["customer_id"],
            "opening_balance": round(
                opening_balance,
                2
            ),
            "transactions": all_transactions,
            "closing_balance": round(
                closing_balance,
                2
            )
        }

    # =========================================================
    # GENERATE ONE MONTH
    # =========================================================

    def _generate_month(
        self,
        customer,
        monthly_income,
        expenses,
        debt,
        discretionary,
        investment,
        month_start
    ):
        transactions = []

        # =====================================================
        # SALARY - REGULAR
        # =====================================================

        salary_day = self.random.randint(1, 5)

        salary_date = (
            month_start
            + timedelta(days=salary_day - 1)
            + timedelta(
                hours=self.random.randint(8, 11),
                minutes=self.random.randint(0, 59)
            )
        )

        transactions.append(
            self._create_transaction(
                customer=customer,
                transaction_date=salary_date,
                transaction_type="SALARY",
                category="INCOME",
                credit_debit="CREDIT",
                amount=monthly_income,
                description="Monthly salary"
            )
        )

        # =====================================================
        # RENT - RECURRING
        # =====================================================

        rent_day = self.random.randint(3, 7)

        rent_date = (
            month_start
            + timedelta(days=rent_day - 1)
            + timedelta(
                hours=self.random.randint(9, 20),
                minutes=self.random.randint(0, 59)
            )
        )

        transactions.append(
            self._create_transaction(
                customer=customer,
                transaction_date=rent_date,
                transaction_type="RENT",
                category="HOUSING",
                credit_debit="DEBIT",
                amount=expenses["housing"],
                description="Monthly rent"
            )
        )

        # =====================================================
        # UTILITIES - RECURRING
        # =====================================================

        utility_day = self.random.randint(7, 15)

        utility_date = (
            month_start
            + timedelta(days=utility_day - 1)
            + timedelta(
                hours=self.random.randint(9, 20),
                minutes=self.random.randint(0, 59)
            )
        )

        transactions.append(
            self._create_transaction(
                customer=customer,
                transaction_date=utility_date,
                transaction_type="UTILITIES",
                category="BILLS",
                credit_debit="DEBIT",
                amount=expenses["utilities"],
                description="Utility bill payment"
            )
        )

        # =====================================================
        # EMI - RECURRING
        # =====================================================

        if debt > 0:

            emi_day = self.random.randint(10, 20)

            emi_date = (
                month_start
                + timedelta(days=emi_day - 1)
                + timedelta(
                    hours=self.random.randint(9, 20),
                    minutes=self.random.randint(0, 59)
                )
            )

            transactions.append(
                self._create_transaction(
                    customer=customer,
                    transaction_date=emi_date,
                    transaction_type="EMI",
                    category="DEBT",
                    credit_debit="DEBIT",
                    amount=debt,
                    description="Loan EMI payment"
                )
            )

        # =====================================================
        # INVESTMENT - RECURRING
        # =====================================================

        if investment > 0:

            investment_day = self.random.randint(5, 15)

            investment_date = (
                month_start
                + timedelta(days=investment_day - 1)
                + timedelta(
                    hours=self.random.randint(9, 20),
                    minutes=self.random.randint(0, 59)
                )
            )

            transactions.append(
                self._create_transaction(
                    customer=customer,
                    transaction_date=investment_date,
                    transaction_type="INVESTMENT",
                    category="INVESTMENT",
                    credit_debit="DEBIT",
                    amount=investment,
                    description="Monthly investment"
                )
            )

        # =====================================================
        # VARIABLE EXPENSES
        # HAWKES CONTROLS THEIR TIMING
        # =====================================================

        variable_transactions = []

        # -----------------------------------------------------
        # GROCERIES
        # -----------------------------------------------------

        food_count = self.random.randint(8, 15)

        food_amounts = self._split_amount(
            expenses["food"],
            food_count
        )

        for amount in food_amounts:

            variable_transactions.append(
                self._create_template(
                    transaction_type="GROCERIES",
                    category="FOOD",
                    credit_debit="DEBIT",
                    amount=amount,
                    description="Grocery purchase"
                )
            )

        # -----------------------------------------------------
        # TRANSPORT
        # -----------------------------------------------------

        transport_count = self.random.randint(8, 20)

        transport_amounts = self._split_amount(
            expenses["transport"],
            transport_count
        )

        for amount in transport_amounts:

            variable_transactions.append(
                self._create_template(
                    transaction_type="TRANSPORT",
                    category="TRANSPORT",
                    credit_debit="DEBIT",
                    amount=amount,
                    description="Transport expense"
                )
            )

        # -----------------------------------------------------
        # SHOPPING / DISCRETIONARY
        # -----------------------------------------------------

        shopping_count = self.random.randint(2, 6)

        shopping_amounts = self._split_amount(
            discretionary,
            shopping_count
        )

        for amount in shopping_amounts:

            variable_transactions.append(
                self._create_template(
                    transaction_type="SHOPPING",
                    category="DISCRETIONARY",
                    credit_debit="DEBIT",
                    amount=amount,
                    description="Discretionary purchase"
                )
            )

        # Shuffle variable transactions
        self.random.shuffle(
            variable_transactions
        )

        # Generate Hawkes timestamps
        timestamps = self._generate_hawkes_timestamps(
            month_start=month_start,
            number_of_transactions=len(
                variable_transactions
            )
        )

        # Assign timestamps to variable transactions
        for template, timestamp in zip(
            variable_transactions,
            timestamps
        ):

            transactions.append(
                self._create_transaction(
                    customer=customer,
                    transaction_date=timestamp,
                    transaction_type=template[
                        "transaction_type"
                    ],
                    category=template[
                        "category"
                    ],
                    credit_debit=template[
                        "credit_debit"
                    ],
                    amount=template[
                        "amount"
                    ],
                    description=template[
                        "description"
                    ]
                )
            )

        return transactions

    # =========================================================
    # TRANSACTION TEMPLATE
    # =========================================================

    def _create_template(
        self,
        transaction_type,
        category,
        credit_debit,
        amount,
        description
    ):
        return {
            "transaction_type": transaction_type,
            "category": category,
            "credit_debit": credit_debit,
            "amount": amount,
            "description": description
        }

    # =========================================================
    # HAWKES TIMESTAMPS
    # =========================================================

    def _generate_hawkes_timestamps(
        self,
        month_start,
        number_of_transactions
    ):
        if number_of_transactions == 0:
            return []

        if self.use_hawkes:

            hawkes = HawkesGenerator(
                baseline_rate=0.5,
                alpha=0.8,
                beta=1.5,
                seed=self.random.randint(
                    1,
                    1000000
                )
            )

            events = hawkes.generate_events(
                duration_days=30,
                max_events=100
            )

            # If Hawkes generates fewer events,
            # generate additional random timestamps.
            if len(events) < number_of_transactions:

                extra_events = (
                    self._generate_random_event_times(
                        number_of_transactions
                        - len(events)
                    )
                )

                events.extend(
                    extra_events
                )

        else:

            events = (
                self._generate_random_event_times(
                    number_of_transactions
                )
            )

        events = events[
            :number_of_transactions
        ]

        timestamps = []

        for event_time in events:

            timestamp = (
                month_start
                + timedelta(days=event_time)
            )

            timestamps.append(
                timestamp
            )

        timestamps.sort()

        return timestamps

    # =========================================================
    # RANDOM EVENT TIMES
    # =========================================================

    def _generate_random_event_times(
        self,
        count
    ):
        return [
            self.random.uniform(
                0,
                29
            )
            for _ in range(count)
        ]

    # =========================================================
    # CREATE TRANSACTION
    # =========================================================

    def _create_transaction(
        self,
        customer,
        transaction_date,
        transaction_type,
        category,
        credit_debit,
        amount,
        description
    ):
        return {
            "customer_id": customer[
                "customer_id"
            ],
            "timestamp": transaction_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "transaction_type": transaction_type,
            "category": category,
            "credit_debit": credit_debit,
            "amount": round(
                amount,
                2
            ),
            "description": description
        }

    # =========================================================
    # SPLIT TOTAL AMOUNT
    # =========================================================

    def _split_amount(
        self,
        total_amount,
        number_of_transactions
    ):
        weights = [
            self.random.uniform(
                0.5,
                1.5
            )
            for _ in range(
                number_of_transactions
            )
        ]

        weight_sum = sum(
            weights
        )

        amounts = [
            total_amount
            * weight
            / weight_sum
            for weight in weights
        ]

        return amounts

    # =========================================================
    # RUNNING BALANCE
    # =========================================================

    def _add_running_balance(
        self,
        transactions
    ):
        balance = self.opening_balance

        for transaction in transactions:

            if (
                transaction["credit_debit"]
                == "CREDIT"
            ):
                balance += transaction[
                    "amount"
                ]

            else:
                balance -= transaction[
                    "amount"
                ]

            transaction["balance"] = round(
                balance,
                2
            )

    # =========================================================
    # BALANCE VALIDATION
    # =========================================================

    def validate_balance(
        self,
        account_data
    ):
        opening_balance = (
            account_data[
                "opening_balance"
            ]
        )

        transactions = (
            account_data[
                "transactions"
            ]
        )

        closing_balance = (
            account_data[
                "closing_balance"
            ]
        )

        total_credits = sum(
            transaction["amount"]
            for transaction in transactions
            if transaction[
                "credit_debit"
            ] == "CREDIT"
        )

        total_debits = sum(
            transaction["amount"]
            for transaction in transactions
            if transaction[
                "credit_debit"
            ] == "DEBIT"
        )

        calculated_closing_balance = (
            opening_balance
            + total_credits
            - total_debits
        )

        calculated_closing_balance = round(
            calculated_closing_balance,
            2
        )

        return (
            calculated_closing_balance
            == closing_balance
        )

    # =========================================================
    # ADD MONTHS
    # =========================================================

    def _add_months(
        self,
        date,
        months
    ):
        month = (
            date.month
            - 1
            + months
        )

        year = (
            date.year
            + month // 12
        )

        month = (
            month % 12
            + 1
        )

        return date.replace(
            year=year,
            month=month
        )