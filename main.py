from src.archetypes.archetype_engine import ArchetypeEngine
from src.archetypes.customer_generator import CustomerGenerator
from src.archetypes.financial_profile_generator import (
    FinancialProfileGenerator
)
from src.transactions.transaction_generator import (
    TransactionGenerator
)


# =========================================================
# ARCHETYPE ENGINE
# =========================================================

engine = ArchetypeEngine(
    "config/archetypes.json"
)


# =========================================================
# CUSTOMER GENERATOR
# =========================================================

customer_generator = CustomerGenerator(
    archetype_engine=engine,
    seed=42
)


customers = customer_generator.generate_customers(
    archetype_id="A1",
    count=1
)


# =========================================================
# FINANCIAL PROFILE GENERATOR
# =========================================================

financial_generator = FinancialProfileGenerator(
    parameter_path="config/archetype_parameters.json",
    seed=42
)


# =========================================================
# TRANSACTION GENERATOR
# =========================================================

transaction_generator = TransactionGenerator(
    seed=42,
    opening_balance=5000,
    use_hawkes=True
)


# =========================================================
# GENERATE DATA
# =========================================================

for customer in customers:

    # -----------------------------------------------------
    # Generate Financial Profile
    # -----------------------------------------------------

    profile = financial_generator.generate_profile(
        customer
    )

    # -----------------------------------------------------
    # Generate Transactions
    # -----------------------------------------------------

    account_data = (
        transaction_generator.generate_transactions(
            customer=customer,
            financial_profile=profile,
            start_date="2026-01-01",
            months=3
        )
    )

    # =====================================================
    # CUSTOMER
    # =====================================================

    print("\n" + "=" * 70)
    print("CUSTOMER")
    print("=" * 70)

    print(customer)

    # =====================================================
    # FINANCIAL PROFILE
    # =====================================================

    print("\n" + "=" * 70)
    print("FINANCIAL PROFILE")
    print("=" * 70)

    print(profile)

    # =====================================================
    # OPENING BALANCE
    # =====================================================

    print("\nOpening Balance:", end=" ")
    print(
        f"{account_data['opening_balance']:.0f}"
    )

    # =====================================================
    # TRANSACTIONS
    # =====================================================

    print("\nTRANSACTIONS")

    for transaction in account_data["transactions"]:
        print(transaction)

    # =====================================================
    # CLOSING BALANCE
    # =====================================================

    print("\nClosing Balance:", end=" ")
    print(
        f"{account_data['closing_balance']:.2f}"
    )

    # =====================================================
    # BALANCE VALIDATION
    # =====================================================

    balance_valid = (
        transaction_generator.validate_balance(
            account_data
        )
    )

    print(
        "Balance Validation:",
        balance_valid
    )