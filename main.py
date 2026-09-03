from src.archetypes.archetype_engine import ArchetypeEngine
from src.archetypes.customer_generator import CustomerGenerator
from src.archetypes.financial_profile_generator import FinancialProfileGenerator
from src.transactions.transaction_generator import TransactionGenerator


# ----------------------------------------
# Load archetypes
# ----------------------------------------

engine = ArchetypeEngine("config/archetypes.json")


# ----------------------------------------
# Generate customers
# ----------------------------------------

customer_generator = CustomerGenerator(
    archetype_engine=engine,
    seed=42
)

customers = customer_generator.generate_customers(
    archetype_id="A1",
    count=1
)


# ----------------------------------------
# Generate financial profile
# ----------------------------------------

financial_generator = FinancialProfileGenerator(
    parameter_path="config/archetype_parameters.json",
    seed=42
)


# ----------------------------------------
# Generate transactions
# ----------------------------------------

transaction_generator = TransactionGenerator(
    seed=42
)


for customer in customers:

    profile = financial_generator.generate_profile(
        customer
    )

    transactions = transaction_generator.generate_transactions(
        customer=customer,
        financial_profile=profile,
        start_date="2026-01-01",
        months=1
    )

    print("\nCustomer:")
    print(customer)

    print("\nFinancial Profile:")
    print(profile)

    print("\nTransactions:")

    for transaction in transactions:
        print(transaction)