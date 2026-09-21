from src.archetypes.archetype_engine import ArchetypeEngine
from src.archetypes.customer_generator import CustomerGenerator
from src.archetypes.financial_profile_generator import FinancialProfileGenerator
from src.transactions.transaction_generator import TransactionGenerator
from src.llm.semantic_enricher import SemanticEnricher


# ============================================================
# 1. ARCHETYPE ENGINE
# ============================================================

engine = ArchetypeEngine(
    "config/archetypes.json"
)


# ============================================================
# 2. CUSTOMER GENERATOR
# ============================================================

customer_generator = CustomerGenerator(
    archetype_engine=engine,
    seed=42
)

customers = customer_generator.generate_customers(
    archetype_id="A1",
    count=1
)


# ============================================================
# 3. FINANCIAL PROFILE GENERATOR
# ============================================================

financial_generator = FinancialProfileGenerator(
    parameter_path="config/archetype_parameters.json",
    seed=42
)


# ============================================================
# 4. TRANSACTION GENERATOR
# ============================================================

transaction_generator = TransactionGenerator(
    seed=42,
    opening_balance=5000,
    use_hawkes=True
)


# ============================================================
# 5. SEMANTIC ENRICHER
# ============================================================

semantic_enricher = SemanticEnricher(
    seed=42
)


# ============================================================
# 6. GENERATE CUSTOMER DATA
# ============================================================

for customer in customers:

    # --------------------------------------------------------
    # Generate financial profile
    # --------------------------------------------------------

    profile = financial_generator.generate_profile(
        customer
    )

    # --------------------------------------------------------
    # Generate transaction history
    # --------------------------------------------------------

    transactions = transaction_generator.generate_transactions(
        customer=customer,
        financial_profile=profile,
        start_date="2026-01-01",
        months=3
    )

    # --------------------------------------------------------
    # Add semantic information
    # --------------------------------------------------------

    enriched_transactions = (
        semantic_enricher.enrich_transactions(
            transactions
        )
    )


    # ========================================================
    # DISPLAY CUSTOMER
    # ========================================================

    print("\n" + "=" * 70)
    print("CUSTOMER")
    print("=" * 70)

    print(customer)


    # ========================================================
    # DISPLAY FINANCIAL PROFILE
    # ========================================================

    print("\n" + "=" * 70)
    print("FINANCIAL PROFILE")
    print("=" * 70)

    print(profile)


    # ========================================================
    # DISPLAY ENRICHED TRANSACTIONS
    # ========================================================

    print("\n" + "=" * 70)
    print("ENRICHED TRANSACTIONS")
    print("=" * 70)

    for transaction in enriched_transactions:
        print(transaction)