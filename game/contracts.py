# game/contracts.py

def create_contract(person, role_type, months, salary=None, exclusive=True):
    """
    Creates a contract object for an actor, writer, or director.
    """
    if salary is None:
        salary = person.get("salary", 1.0)

    return {
        "type": role_type,  # 'actor', 'writer', or 'director'
        "person": person,
        "duration": months,
        "salary": salary,
        "exclusive": exclusive,
        "remaining": months,
    }

def age_contracts(contracts_by_type):
    """
    Reduces contract durations by 1 month and removes expired ones.
    """
    for role in ["actors", "writers", "directors"]:
        new_list = []
        for contract in contracts_by_type.get(role, []):
            contract["remaining"] -= 1
            if contract["remaining"] > 0:
                new_list.append(contract)
            else:
                print(f"📄 Contract expired: {contract['person']['name']} ({role[:-1]})")
        contracts_by_type[role] = new_list

def find_active_contracts(contracts_by_type, role):
    """
    Returns a list of people still under contract for the specified role.
    """
    return [c["person"] for c in contracts_by_type.get(role, []) if c["remaining"] > 0]

def contract_phase(studio, casting_pool):
    print("\n🤝 Contract Phase: Sign new talent to your studio.")

    options = {
        "1": "Actors",
        "2": "Writers",
        "3": "Directors",
        "4": "Skip"
    }

    for key, label in options.items():
        print(f"{key}. {label}")

    choice = input("Select contract type (1–4): ").strip()
    if choice == "4" or choice == "":
        print("⏩ Skipping contract phase.")
        return

    if choice not in options:
        print("❌ Invalid choice.")
        return

    if choice == "1":
        candidates = casting_pool.get_actor_choices(3)
        role = "actors"
    elif choice == "2":
        candidates = casting_pool.get_writer_choices(3)
        role = "writers"
    elif choice == "3":
        candidates = casting_pool.get_director_choices(3)
        role = "directors"

    print(f"\nAvailable {options[choice]} to Sign:")
    for i, c in enumerate(candidates, 1):
        print(f"{i}. {c['name']} — Fame: {c['fame']} | Salary Expectation: ${c['salary']}M")

    idx = input("Select someone to sign: ").strip()
    if not idx.isdigit() or not (1 <= int(idx) <= len(candidates)):
        print("❌ Invalid selection.")
        return

    selected = candidates[int(idx) - 1]

    months = input("For how many months? (1–12): ").strip()
    if not months.isdigit() or not (1 <= int(months) <= 12):
        print("❌ Invalid duration.")
        return

    contract = create_contract(
        person=selected,
        role_type=role[:-1],  # 'actors' -> 'actor'
        months=int(months),
        salary=selected["salary"],
        exclusive=True
    )

    studio.contracts[role].append(contract)
    print(f"✅ Signed {selected['name']} to a {months}-month exclusive contract!")
