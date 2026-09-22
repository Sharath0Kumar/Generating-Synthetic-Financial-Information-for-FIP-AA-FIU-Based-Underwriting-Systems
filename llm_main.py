from src.llm.llm_generator import LLMGenerator


# API key will be added later
API_KEY = "YOUR_API_KEY_HERE"


# Create generator
generator = LLMGenerator(
    api_key=API_KEY,
    model="YOUR_MODEL_HERE"
)


# --------------------------------
# STEP 1: Generate customer
# --------------------------------

customer = generator.generate_customer("A1")

print("\n==============================")
print("GENERATED CUSTOMER")
print("==============================")

print(customer)


# --------------------------------
# STEP 2: Generate transactions
# --------------------------------

transactions = generator.generate_transactions(
    customer_data=customer,
    months=3
)


print("\n==============================")
print("GENERATED TRANSACTIONS")
print("==============================")

print(transactions)