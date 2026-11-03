from dataclasses import dataclass
from typing import List, Set, Dict, Any


@dataclass
class Rule:
    antecedents: List[str]
    consequent: str
    priority: int = 0
    name: str = ""


class ForwardChainingEngine:
    def __init__(self, rules: List[Rule]):
        self.rules = rules
        self.facts: Set[str] = set()
        self.trace: List[Dict[str, Any]] = []

    def assert_facts(self, initial: List[str]) -> None:
        """Add the user's initial facts to working memory."""
        self.facts.update(initial)

    def can_fire(self, rule: Rule) -> bool:
        """A rule fires when every condition is known and its result is new."""
        return all(condition in self.facts for condition in rule.antecedents) and rule.consequent not in self.facts

    def run(self) -> None:
        """Apply the highest-priority available rule until no rule can fire.

        Ties use the order in which rules appear in the JSON file.
        """
        while True:
            applicable = [rule for rule in self.rules if self.can_fire(rule)]
            if not applicable:
                break
            rule = max(applicable, key=lambda item: item.priority)
            self.facts.add(rule.consequent)
            self.trace.append({
                "rule": rule.name,
                "antecedents": list(rule.antecedents),
                "consequent": rule.consequent,
                "priority": rule.priority,
            })

    def conclusions(self) -> Dict[str, List[str]]:
        """Separate recommendations, specs and the remaining known facts."""
        return {
            "recommendations": sorted(fact.split(":", 1)[1] for fact in self.facts if fact.startswith("recommend:")),
            "specs": sorted(fact.split(":", 1)[1] for fact in self.facts if fact.startswith("spec:")),
            "other_facts": sorted(fact for fact in self.facts if not fact.startswith(("recommend:", "spec:"))),
        }
