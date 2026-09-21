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

        # -------------------------------------------------
        # 1. Generate annual income
        # -------------------------------------------------

        income_range = archetype_parameters["income"]["annual"]

        annual_income = self.random.randint(
            income_range["min"],
            income_range["max"]
        )

        # -------------------------------------------------
        # 2. Convert annual income to monthly income
        # -------------------------------------------------

        monthly_income = annual_income / 12

        # -------------------------------------------------
        # 3. Generate variable expense ratios
        # -------------------------------------------------

        ratios = archetype_parameters["expense_ratios"]

        housing_ratio = self.random.uniform(
            ratios["housing"]["min"],
            ratios["housing"]["max"]
        )

        food_ratio = self.random.uniform(
            ratios["food"]["min"],
            ratios["food"]["max"]
        )

        utilities_ratio = self.random.uniform(
            ratios["utilities"]["min"],
            ratios["utilities"]["max"]
        )

        transport_ratio = self.random.uniform(
            ratios["transport"]["min"],
            ratios["transport"]["max"]
        )

        debt_ratio = self.random.uniform(
            ratios["debt"]["min"],
            ratios["debt"]["max"]
        )

        discretionary_ratio = self.random.uniform(
            ratios["discretionary"]["min"],
            ratios["discretionary"]["max"]
        )

        investment_ratio = self.random.uniform(
            ratios["investment"]["min"],
            ratios["investment"]["max"]
        )

        # -------------------------------------------------
        # 4. Calculate individual expenses
        # -------------------------------------------------

        housing = monthly_income * housing_ratio
        food = monthly_income * food_ratio
        utilities = monthly_income * utilities_ratio
        transport = monthly_income * transport_ratio

        debt = monthly_income * debt_ratio

        discretionary = monthly_income * discretionary_ratio

        investment = monthly_income * investment_ratio

        # -------------------------------------------------
        # 5. Calculate essential expenses
        # -------------------------------------------------

        essential_expenses = (
            housing
            + food
            + utilities
            + transport
        )

        # -------------------------------------------------
        # 6. Calculate savings
        # -------------------------------------------------

        savings = (
            monthly_income
            - essential_expenses
            - debt
            - discretionary
            - investment
        )

        # -------------------------------------------------
        # 7. Return compact financial profile
        # -------------------------------------------------

        return {
            "customer_id": customer["customer_id"],
            "archetype_id": archetype_id,

            "annual_income": annual_income,

            "monthly_income": round(monthly_income, 2),

            "essential_expenses": {
                "total": round(essential_expenses, 2),
                "housing": round(housing, 2),
                "food": round(food, 2),
                "utilities": round(utilities, 2),
                "transport": round(transport, 2)
            },

            "debt_burden": round(debt, 2),

            "discretionary_spending": round(
                discretionary, 2
            ),

            "savings": round(savings, 2),

            # Kept internally because the transaction
            # generator still needs investment information.
            "investment": round(investment, 2)
        }