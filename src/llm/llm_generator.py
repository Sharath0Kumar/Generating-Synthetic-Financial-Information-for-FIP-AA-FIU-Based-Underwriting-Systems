import json
from openai import OpenAI


class LLMGenerator:

    def __init__(self, api_key, model="gpt-5.6-luna"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def load_json(self, file_path):
        with open(file_path, "r") as file:
            return json.load(file)

    def generate_customer(self, archetype_id):

        # Load archetype information
        archetypes_data = self.load_json(
            "config/archetypes.json"
        )

        # Load numerical parameters
        parameters_data = self.load_json(
            "config/archetype_parameters.json"
        )

        # Find the requested archetype
        archetype = None

        for item in archetypes_data["archetypes"]:
            if item["archetype_id"] == archetype_id:
                archetype = item
                break

        if archetype is None:
            raise ValueError(
                f"Archetype {archetype_id} not found"
            )

        # Get parameters for the archetype
        parameters = parameters_data[archetype_id]

        # Create the prompt
        prompt = f"""
You are a synthetic financial data generator.

Generate ONE completely fictional customer based on
the following archetype and financial parameters.

IMPORTANT:
- Do not use real people's information.
- Follow the given constraints.
- Generate realistic but synthetic information.
- Annual income must be within the specified range.
- Expense ratios must remain within the specified ranges.
- Follow the employment and income behavior of the archetype.
- Return ONLY valid JSON.
- Do not add explanations outside the JSON.

CUSTOMER ARCHETYPE:
{json.dumps(archetype, indent=2)}

FINANCIAL PARAMETERS:
{json.dumps(parameters, indent=2)}

Return the following JSON structure:

{{
    "customer": {{
        "customer_id": "",
        "name": "",
        "age": 0,
        "location_type": "",
        "employment_type": "",
        "occupation": ""
    }},

    "financial_profile": {{
        "annual_income": 0,
        "monthly_income": 0,
        "expense_ratios": {{
            "housing": 0,
            "food": 0,
            "utilities": 0,
            "transport": 0,
            "debt": 0,
            "discretionary": 0,
            "investment": 0
        }},
        "monthly_expenses": {{
            "housing": 0,
            "food": 0,
            "utilities": 0,
            "transport": 0,
            "debt": 0,
            "discretionary": 0,
            "investment": 0
        }}
    }}
}}
"""

        # Send prompt to the LLM
        response = self.client.responses.create(
            model=self.model,
            input=prompt
        )

        # Get the generated text
        result = response.output_text

        # Convert JSON text into Python dictionary
        customer_data = json.loads(result)

        return customer_data
        def generate_transactions(self, customer_data, months=3):

        # Create prompt using the generated customer
            prompt = f"""
You are a synthetic financial transaction generator.

Generate completely fictional financial transactions for the
following synthetic customer.

CUSTOMER INFORMATION:
{json.dumps(customer_data, indent=2)}

Generate transactions for {months} months.

Follow these rules:

1. Salary should be received monthly.
2. Transactions must be consistent with the customer's income.
3. Housing expenses should occur regularly.
4. Food and grocery transactions can occur frequently.
5. Utility payments should occur monthly or regularly.
6. Transport transactions can occur frequently.
7. Discretionary spending should remain relatively low.
8. Investment transactions should have low frequency.
9. Debt payments should only occur if debt exists.
10. Do not create impossible or negative transaction amounts.
11. Maintain a realistic running account balance.
12. All information must be completely synthetic.

Use these transaction categories where appropriate:

SALARY
RENT
GROCERIES
UTILITIES
TRANSPORT
SHOPPING
INVESTMENT
EMI
RESTAURANT
CASH_WITHDRAWAL
OTHER_INCOME
BUSINESS_RECEIPT
BUSINESS_EXPENSE

Return ONLY valid JSON.

Use this structure:

{{
    "transactions": [
        {{
            "date": "YYYY-MM-DD",
            "type": "",
            "description": "",
            "amount": 0,
            "transaction_direction": "CREDIT",
            "balance_after_transaction": 0
        }}
    ]
}}
"""

        # Send request to LLM
        response = self.client.responses.create(
            model=self.model,
            input=prompt
        )

        # Get generated JSON
        result = response.output_text

        # Convert JSON text into Python dictionary
        transactions = json.loads(result)

        return transactions