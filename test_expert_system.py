import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine import ForwardChainingEngine, Rule
from kb_loader import load_rules

KB_PATH = Path(__file__).resolve().parents[1] / "kb" / "laptop_rules.json"


class TestExpertSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules(str(KB_PATH))

    def evaluate(self, facts):
        engine = ForwardChainingEngine(self.rules)
        engine.assert_facts(facts)
        engine.run()
        return engine

    def test_at_least_ten_rules(self):
        self.assertGreaterEqual(len(self.rules), 10)

    def test_premium_ultrabook(self):
        engine = self.evaluate(["budget_high", "portable", "long_battery"])
        self.assertIn("recommend:premium_ultrabook", engine.facts)
        self.assertIn("spec:512gb_ssd", engine.facts)

    def test_gaming_laptop(self):
        engine = self.evaluate(["budget_high", "gaming"])
        self.assertIn("recommend:gaming_laptop", engine.facts)
        self.assertIn("spec:dedicated_gpu", engine.facts)

    def test_budget_student(self):
        engine = self.evaluate(["budget_low", "student"])
        self.assertIn("recommend:budget_student_laptop", engine.facts)
        self.assertIn("spec:all_day_battery", engine.facts)

    def test_budget_coding(self):
        engine = self.evaluate(["budget_low", "programming"])
        self.assertIn("recommend:budget_developer_laptop", engine.facts)

    def test_creator_workstation(self):
        engine = self.evaluate(["budget_high", "content_creation"])
        self.assertIn("recommend:creator_workstation", engine.facts)
        self.assertIn("spec:32gb_ram", engine.facts)

    def test_no_matching_rules(self):
        engine = self.evaluate(["budget_high"])
        self.assertEqual(engine.conclusions()["recommendations"], [])
        self.assertEqual(engine.trace, [])

    def test_can_fire_only_once(self):
        engine = ForwardChainingEngine([Rule(["a"], "b", name="A to B")])
        engine.assert_facts(["a"])
        self.assertTrue(engine.can_fire(engine.rules[0]))
        engine.run()
        self.assertFalse(engine.can_fire(engine.rules[0]))
        engine.run()
        self.assertEqual(len(engine.trace), 1)

    def test_multistep_forward_chaining(self):
        engine = ForwardChainingEngine([
            Rule(["b"], "c", priority=5, name="B to C"),
            Rule(["a"], "b", priority=1, name="A to B"),
        ])
        engine.assert_facts(["a"])
        engine.run()
        self.assertIn("c", engine.facts)
        self.assertEqual([step["rule"] for step in engine.trace], ["A to B", "B to C"])

    def test_priority_order(self):
        engine = ForwardChainingEngine([
            Rule(["a"], "lower", priority=1, name="Lower"),
            Rule(["a"], "higher", priority=9, name="Higher"),
        ])
        engine.assert_facts(["a"])
        engine.run()
        self.assertEqual(engine.trace[0]["rule"], "Higher")


if __name__ == "__main__":
    unittest.main()
