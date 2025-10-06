# HollywoodSim/game/funding.py
import random

FUNDING_SOURCES = [
    {
        "type": "Bank Loan",
        "base_amount": 0.5,  # % of budget
        "interest_range": (5, 12),
        "conditions": ["Repay after release", "Fixed interest rate"]
    },
    {
        "type": "Private Investor",
        "base_amount": 0.7,
        "profit_share_range": (10, 30),
        "conditions": ["Creative input possible", "Profit share deal"]
    },
    {
        "type": "Crowdfunding",
        "base_amount": 0.3,
        "conditions": ["Public campaign required", "Boosts early buzz"]
    },
    {
        "type": "Self-Funding",
        "base_amount": 1.0,
        "conditions": ["Full creative control", "High personal risk"]
    }
]


def generate_funding_offers(project_budget, studio_reputation):
    """
    Generates a list of funding offers for a GUI or API to display.
    Each offer is a dictionary with type, amount, and conditions.
    """
    offers = []
    for source in FUNDING_SOURCES:
        # Base funding amount
        amount = round(project_budget * source["base_amount"], 2)

        # Modify slightly based on reputation (reputation: 0–100)
        amount *= (0.9 + (studio_reputation / 100) * 0.2)
        amount = round(amount, 2)

        offer = {
            "type": source["type"],
            "amount": amount,
            "conditions": list(source["conditions"])  # Copy list
        }

        # Optional parameters
        if "interest_range" in source:
            offer["interest_rate"] = random.randint(*source["interest_range"])
        if "profit_share_range" in source:
            offer["profit_share"] = random.randint(*source["profit_share_range"])

        offers.append(offer)

    return offers


def choose_funding_offer(offers, choice_index):
    """
    Selects a funding offer by index. 
    Used by GUI layer after player chooses.
    """
    if choice_index < 0 or choice_index >= len(offers):
        raise ValueError("Invalid funding choice index.")
    return offers[choice_index]


# Example GUI/API usage
if __name__ == "__main__":
    budget = 10_000_000
    reputation = 65

    offers = generate_funding_offers(budget, reputation)
    
    # Instead of printing or asking input(), 
    # we return structured data for GUI display
    for idx, offer in enumerate(offers):
        print(f"[{idx}] {offer['type']} - ${offer['amount']:,}")
        if "interest_rate" in offer:
            print(f"    Interest: {offer['interest_rate']}%")
        if "profit_share" in offer:
            print(f"    Profit Share: {offer['profit_share']}%")
        print(f"    Conditions: {', '.join(offer['conditions'])}")
