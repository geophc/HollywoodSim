# game/contracts.py

def create_contract(person, role_type, months, salary=None, exclusive=True):
    """
    Creates a contract object for an actor, writer, director, or staff.
    """
    if salary is None:
        salary = person.get("salary", 1.0)

    return {
        "type": role_type,        # 'actors', 'writers', 'directors', or 'staff'
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
    for role in ["actors", "writers", "directors", "staff"]:
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
    Returns active contract dicts (with person + remaining months).
    """
    return [c for c in contracts_by_type.get(role, []) if c["remaining"] > 0]




def contract_phase(studio, casting_pool):
    """
    Handles a single contract-signing phase for the player.
    """
    print("\n🤝 Contract Phase: Sign new talent to your studio.\n")

    options = {
        "1": "Actors",
        "2": "Writers",
        "3": "Directors",
        "4": "Staff",
        "5": "Skip"
    }

    for key, label in options.items():
        print(f"{key}. {label}")

    choice = input("Select contract type (1–5): ").strip()
    if choice == "5" or choice == "":
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
    elif choice == "4":
        candidates = casting_pool.get_staff_choices(3)
        role = "staff"

    print(f"\nAvailable {options[choice]} to Sign:")
    for i, c in enumerate(candidates, 1):
        print(f"{i}. {c['name']} — Fame: {c.get('fame', 0)} | Salary Expectation: ${c.get('salary', 1.0)}M")

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
        role_type=role,
        months=int(months),
        salary=selected.get("salary", 1.0),
        exclusive=True
    )

    studio.contracts[role].append(contract)
    studio.hire(selected)
    print(f"✅ Signed {selected['name']} to a {months}-month exclusive contract!")


def print_roster(studio):
    """Prints the studio's current roster of signed talent and staff, sorted by expiring contracts."""
    
    def show_group(role, title, extra=""):
        contracts = sorted(find_active_contracts(studio.contracts, role), key=lambda c: c["remaining"])
        print(f"\n{title} ({len(contracts)}):")
        if contracts:
            for c in contracts:
                p = c["person"]
                line = f" - {p['name']} (Fame: {p.get('fame', 0)}"
                if "salary" in p: 
                    line += f", Salary: ${p['salary']}M"
                if role == "staff":
                    line += f", Role: {p['role']}"
                line += f", Contract: {c['remaining']} months left)"
                print(line)
        else:
            print("   None")

    show_group("actors", "🎭 Signed Actors")
    show_group("directors", "🎬 Signed Directors")
    show_group("writers", "🖋️ Signed Writers")
    show_group("staff", "👷 Signed Staff")
