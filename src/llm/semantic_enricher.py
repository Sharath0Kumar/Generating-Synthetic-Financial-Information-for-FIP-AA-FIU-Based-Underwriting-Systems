import random


class SemanticEnricher:

    def __init__(self, seed=42):
        self.random = random.Random(seed)

        self.merchants = {
            "GROCERIES": [
                "Reliance Smart",
                "DMart",
                "More Supermarket",
                "Local Grocery Store",
                "Spencer's"
            ],

            "TRANSPORT": [
                "BMTC",
                "Namma Yatri",
                "Uber",
                "Ola",
                "Local Bus"
            ],

            "SHOPPING": [
                "Amazon",
                "Flipkart",
                "Myntra",
                "Local Retail Store",
                "Online Shopping"
            ],

            "RENT": [
                "House Rent",
                "Monthly Rent Payment"
            ],

            "UTILITIES": [
                "Electricity Board",
                "Water Utility",
                "Internet Provider",
                "Mobile Recharge"
            ],

            "EMI": [
                "Bank Loan EMI",
                "Personal Loan EMI",
                "Vehicle Loan EMI"
            ],

            "INVESTMENT": [
                "Mutual Fund",
                "SIP Investment",
                "Investment Account"
            ],

            "SALARY": [
                "Employer",
                "Company Payroll"
            ]
        }

    def enrich_transaction(self, transaction):

        transaction_type = transaction["transaction_type"]

        merchant_list = self.merchants.get(
            transaction_type,
            ["Unknown Merchant"]
        )

        merchant = self.random.choice(
            merchant_list
        )

        transaction["merchant"] = merchant

        transaction["narration"] = self._generate_narration(
            transaction_type,
            merchant
        )

        return transaction

    def _generate_narration(
        self,
        transaction_type,
        merchant
    ):

        narrations = {

            "GROCERIES":
                f"Purchase at {merchant}",

            "TRANSPORT":
                f"Transport payment - {merchant}",

            "SHOPPING":
                f"Purchase from {merchant}",

            "RENT":
                "Monthly house rent payment",

            "UTILITIES":
                f"Utility bill payment - {merchant}",

            "EMI":
                f"Monthly EMI payment - {merchant}",

            "INVESTMENT":
                f"Monthly investment - {merchant}",

            "SALARY":
                f"Salary credit - {merchant}"
        }

        return narrations.get(
            transaction_type,
            transaction_type
        )

    def enrich_transactions(
        self,
        transactions
    ):

        enriched_transactions = []

        for transaction in transactions:

            enriched_transaction = (
                self.enrich_transaction(
                    transaction.copy()
                )
            )

            enriched_transactions.append(
                enriched_transaction
            )

        return enriched_transactions