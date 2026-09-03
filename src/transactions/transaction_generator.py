import random
from datetime import datetime, timedelta


class TransactionGenerator:

    def __init__(self, seed=42):
        self.random = random.Random(seed)

    def generate_transactions(
        self,
        customer,
        financial_profile,
        start_date,
        months=1
    ):

        transactions = []

        start_date = datetime.strptime(start_date, "%Y-%m-%d")

        monthly_income = financial_profile["monthly_income"]
        expenses = financial_profile["monthly_expenses"]

        # ------------------------------------------------
        # 1. Salary transaction
        # ------------------------------------------------

        salary_day = self.random.randint(1, 5)

        salary_date = start_date + timedelta(days=salary_day - 1)

        transactions.append({
            "customer_id": customer["customer_id"],
            "timestamp": salary_date.strftime("%Y-%m-%d"),
            "transaction_type": "SALARY",
            "category": "INCOME",
            "credit_debit": "CREDIT",
            "amount": round(monthly_income, 2),
            "description": "Monthly salary"
        })

        # ------------------------------------------------
        # 2. Rent
        # ------------------------------------------------

        rent_day = self.random.randint(1, 7)

        rent_date = start_date + timedelta(days=rent_day - 1)

        transactions.append({
            "customer_id": customer["customer_id"],
            "timestamp": rent_date.strftime("%Y-%m-%d"),
            "transaction_type": "RENT",
            "category": "HOUSING",
            "credit_debit": "DEBIT",
            "amount": round(expenses["housing"], 2),
            "description": "Monthly rent"
        })

        # ------------------------------------------------
        # 3. Utilities
        # ------------------------------------------------

        utility_day = self.random.randint(5, 15)

        utility_date = start_date + timedelta(days=utility_day - 1)

        transactions.append({
            "customer_id": customer["customer_id"],
            "timestamp": utility_date.strftime("%Y-%m-%d"),
            "transaction_type": "UTILITIES",
            "category": "BILLS",
            "credit_debit": "DEBIT",
            "amount": round(expenses["utilities"], 2),
            "description": "Utility bill payment"
        })

        # ------------------------------------------------
        # 4. Food transactions
        # ------------------------------------------------

        food_total = expenses["food"]

        number_of_food_transactions = self.random.randint(8, 15)

        food_amounts = self._split_amount(
            food_total,
            number_of_food_transactions
        )

        for amount in food_amounts:

            day = self.random.randint(1, 28)

            transaction_date = start_date + timedelta(days=day - 1)

            transactions.append({
                "customer_id": customer["customer_id"],
                "timestamp": transaction_date.strftime("%Y-%m-%d"),
                "transaction_type": "GROCERIES",
                "category": "FOOD",
                "credit_debit": "DEBIT",
                "amount": round(amount, 2),
                "description": "Grocery purchase"
            })

        # ------------------------------------------------
        # 5. Transport transactions
        # ------------------------------------------------

        transport_total = expenses["transport"]

        number_of_transport_transactions = self.random.randint(8, 20)

        transport_amounts = self._split_amount(
            transport_total,
            number_of_transport_transactions
        )

        for amount in transport_amounts:

            day = self.random.randint(1, 28)

            transaction_date = start_date + timedelta(days=day - 1)

            transactions.append({
                "customer_id": customer["customer_id"],
                "timestamp": transaction_date.strftime("%Y-%m-%d"),
                "transaction_type": "TRANSPORT",
                "category": "TRANSPORT",
                "credit_debit": "DEBIT",
                "amount": round(amount, 2),
                "description": "Transport expense"
            })

        # ------------------------------------------------
        # 6. Debt / EMI
        # ------------------------------------------------

        if expenses["debt"] > 0:

            debt_day = self.random.randint(5, 20)

            debt_date = start_date + timedelta(days=debt_day - 1)

            transactions.append({
                "customer_id": customer["customer_id"],
                "timestamp": debt_date.strftime("%Y-%m-%d"),
                "transaction_type": "EMI",
                "category": "DEBT",
                "credit_debit": "DEBIT",
                "amount": round(expenses["debt"], 2),
                "description": "Loan EMI payment"
            })

        # ------------------------------------------------
        # 7. Discretionary spending
        # ------------------------------------------------

        discretionary_total = expenses["discretionary"]

        number_of_discretionary_transactions = self.random.randint(2, 6)

        discretionary_amounts = self._split_amount(
            discretionary_total,
            number_of_discretionary_transactions
        )

        for amount in discretionary_amounts:

            day = self.random.randint(1, 28)

            transaction_date = start_date + timedelta(days=day - 1)

            transactions.append({
                "customer_id": customer["customer_id"],
                "timestamp": transaction_date.strftime("%Y-%m-%d"),
                "transaction_type": "SHOPPING",
                "category": "DISCRETIONARY",
                "credit_debit": "DEBIT",
                "amount": round(amount, 2),
                "description": "Discretionary purchase"
            })

        # ------------------------------------------------
        # 8. Investment
        # ------------------------------------------------

        investment = financial_profile["monthly_investment"]

        if investment > 0:

            investment_day = self.random.randint(10, 25)

            investment_date = (
                start_date + timedelta(days=investment_day - 1)
            )

            transactions.append({
                "customer_id": customer["customer_id"],
                "timestamp": investment_date.strftime("%Y-%m-%d"),
                "transaction_type": "INVESTMENT",
                "category": "INVESTMENT",
                "credit_debit": "DEBIT",
                "amount": round(investment, 2),
                "description": "Monthly investment"
            })

        # ------------------------------------------------
        # Sort transactions by date
        # ------------------------------------------------

        transactions.sort(
            key=lambda x: x["timestamp"]
        )

        return transactions

    # ----------------------------------------------------
    # Helper function
    # ----------------------------------------------------

    def _split_amount(self, total_amount, number_of_transactions):

        weights = [
            self.random.uniform(0.5, 1.5)
            for _ in range(number_of_transactions)
        ]

        weight_sum = sum(weights)

        amounts = [
            total_amount * weight / weight_sum
            for weight in weights
        ]

        return amounts