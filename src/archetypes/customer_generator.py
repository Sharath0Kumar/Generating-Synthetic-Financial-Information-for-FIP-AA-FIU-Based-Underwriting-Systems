import random


class CustomerGenerator:

    def __init__(self, archetype_engine, seed=42):
        self.archetype_engine = archetype_engine
        self.random = random.Random(seed)
        self.customer_counter = 0

    def generate_customer(self, archetype_id):
        archetype = self.archetype_engine.get_archetype(archetype_id)

        self.customer_counter += 1

        customer_id = f"C{self.customer_counter:06d}"

        demographic_profile = archetype["demographic_profile"]
        income_profile = archetype["income_profile"]

        # Temporary age range until research-backed values are added.
        age_range = demographic_profile.get("age_range")

        if age_range is None:
            age = self.random.randint(21, 60)
        else:
            age = self.random.randint(
                age_range["min"],
                age_range["max"]
            )

        location_type = self.random.choice(
            demographic_profile["location_type"]
        )

        customer = {
            "customer_id": customer_id,
            "archetype_id": archetype["archetype_id"],
            "archetype_name": archetype["name"],

            "age": age,

            "employment_type": archetype["employment_type"],
            "income_segment": archetype["income_segment"],

            "location_type": location_type,

            "primary_income_type":
                income_profile["primary_income_type"],

            "income_regularity":
                income_profile["regularity"],

            "income_frequency":
                income_profile["frequency"]
        }

        return customer

    def generate_customers(self, archetype_id, count):
        customers = []

        for _ in range(count):
            customer = self.generate_customer(archetype_id)
            customers.append(customer)

        return customers