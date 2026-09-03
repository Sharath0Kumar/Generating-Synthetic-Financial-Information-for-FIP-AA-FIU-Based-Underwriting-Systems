import json
import random
from pathlib import Path


class FinancialProfileGenerator:

    def __init__(self, parameter_path, seed=42):
        self.parameter_path = Path(parameter_path)

        with open(self.parameter_path, "r", encoding="utf-8") as file:
            self.parameters = json.load(file)

        self.random = random.Random(seed)

    def generate_profile(self, customer):

        archetype_id = customer["archetype_id"]

        if archetype_id not in self.parameters:
            raise ValueError(
                f"No financial parameters found for '{archetype_id}'."
            )

        archetype_parameters = self.parameters[archetype_id]

        # Generate individual monthly income
        income_range = archetype_parameters["income"]

        monthly_income = self.random.randint(
            income_range["min"],
            income_range["max"]
        )

        # Get expense ratios
        ratios = archetype_parameters["expense_ratios"]

        housing = monthly_income * ratios["housing"]
        food = monthly_income * ratios["food"]
        utilities = monthly_income * ratios["utilities"]
        transport = monthly_income * ratios["transport"]
        debt = monthly_income * ratios["debt"]
        discretionary = monthly_income * ratios["discretionary"]
        investment = monthly_income * ratios["investment"]

        total_expenses = (
            housing
            + food
            + utilities
            + transport
            + debt
            + discretionary
        )

        savings = monthly_income - total_expenses - investment

        financial_profile = {
            "customer_id": customer["customer_id"],
            "archetype_id": archetype_id,
            "monthly_income": round(monthly_income, 2),

            "monthly_expenses": {
                "housing": round(housing, 2),
                "food": round(food, 2),
                "utilities": round(utilities, 2),
                "transport": round(transport, 2),
                "debt": round(debt, 2),
                "discretionary": round(discretionary, 2)
            },

            "monthly_investment": round(investment, 2),
            "estimated_monthly_savings": round(savings, 2)
        }

        return financial_profile