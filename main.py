from pathlib import Path
from kb_loader import load_rules
from engine import ForwardChainingEngine

KB_PATH = Path(__file__).resolve().parent / "kb" / "laptop_rules.json"


def ask_yes_no(question):
    """Keep asking until the answer is yes or no."""
    while True:
        answer = input(question + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


def collect_initial_facts():
    facts = []
    questions = [
        ("Is portability important?", "portable"),
        ("Do you need long battery life?", "long_battery"),
        ("Is your budget high?", "budget_high"),
        ("Will you use the laptop for gaming?", "gaming"),
        ("Will you use it for programming?", "programming"),
        ("Will you use it for video, photo, or design work?", "content_creation"),
        ("Are you shopping for schoolwork?", "student"),
    ]
    for question, fact in questions:
        response = ask_yes_no(question)
        if fact == "budget_high":
            facts.append("budget_high" if response else "budget_low")
        elif response:
            facts.append(fact)
    return facts


def main():
    rules = load_rules(str(KB_PATH))
    engine = ForwardChainingEngine(rules)
    engine.assert_facts(collect_initial_facts())
    engine.run()
    results = engine.conclusions()

    print("\n=== Laptop Expert System Results ===")
    if results["recommendations"]:
        for recommendation in results["recommendations"]:
            print(f"=> Recommendation: {recommendation}")
    else:
        print("=> No matching recommendation. Try different preferences.")
    if results["specs"]:
        print("=> Suggested specs: " + ", ".join(results["specs"]))
    print("\nRules fired (in order):")
    if not engine.trace:
        print("  None")
    for step in engine.trace:
        conditions = " AND ".join(step["antecedents"]) or "(always)"
        print(f"  - {step['rule']}: IF {conditions} THEN {step['consequent']}")


if __name__ == "__main__":
    main()
