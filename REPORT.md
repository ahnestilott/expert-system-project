# Expert System Mini Project — Explanation Report

## Project goal
This Python project recommends laptop types using a rule-based expert system and **forward chaining**. It does not rely on a hardcoded decision tree: rules are loaded from `kb/laptop_rules.json`.

## Components
- `engine.py` defines `Rule` and `ForwardChainingEngine`.
- `kb_loader.py` loads rules from the JSON knowledge base.
- `kb/laptop_rules.json` contains **20 IF–THEN rules**, including rules that infer specifications from recommendations.
- `main.py` collects user preferences and displays results and the fired-rule trace.
- `tests/test_expert_system.py` checks common scenarios, rule priority, repeat firing and multi-step inference.

## Forward-chaining process
1. User answers questions. Answers are stored as facts like `portable`, `long_battery`, `budget_high`, or `budget_low`.
2. `can_fire(rule)` checks that every antecedent is in working memory and that the consequent has not already been inferred.
3. `run()` chooses the highest-priority applicable rule (ties go to the first rule listed), adds its consequent to working memory, and records the rule in the trace.
4. The loop continues until no rule can add a new fact. The `conclusions()` method separates `recommend:` facts from `spec:` facts and other facts.

## Example
Input facts: `portable`, `long_battery`, `budget_high`.

- **Premium Ultrabook** fires and adds `recommend:premium_ultrabook`.
- **Ultrabook Memory** adds `spec:16gb_ram`.
- **Ultrabook Storage** adds `spec:512gb_ssd`.

Final recommendation: `premium_ultrabook`. This example shows multi-step inference: specs are inferred from a recommendation derived from the original inputs.

## Tests and limitations
Run `python -m unittest discover -s tests -v`. Rules suggest categories and approximate specs rather than real brands, prices, or compatibility. Multiple recommendations may be returned when the user selects multiple use cases. For simplicity, budget is treated as either high or low, and unanswered use cases are omitted from the known facts.

## Extra feature
The program prints the name, conditions, and conclusion of each fired rule, offering a transparent explanation of its reasoning.
