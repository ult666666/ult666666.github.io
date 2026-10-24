"""Verify public trading case explicitly links to a safe runnable example."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DEMO = "https://github.com/ult666666/agentic-trading-research/tree/main/examples"


class TradingShowcaseTests(unittest.TestCase):
    def test_home_and_case_offer_direct_demo_route(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        case = (ROOT / "projects/trading-research.html").read_text(encoding="utf-8")
        self.assertIn(DEMO, home)
        self.assertIn(DEMO, case)
        self.assertIn("no broker or market data", case.lower())
        self.assertIn("No automated order execution", home)

    def test_case_links_to_traceable_evidence(self):
        case = (ROOT / "projects/trading-research.html").read_text(encoding="utf-8")
        for path in ("examples/fail_closed_gate.py", "examples/test_fail_closed_gate.py",
                     "actions/workflows/research-demo.yml"):
            self.assertIn(path, case)
        self.assertNotIn("/Users/prince/", case)


if __name__ == "__main__":
    unittest.main()
