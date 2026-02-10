import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from ddos.mitigator import DDoSDetector, RateLimiter

class TestDetector(unittest.TestCase):
    def test_threshold(self):
        d = DDoSDetector(threshold=5, window=60)
        for i in range(10):
            d.record_connection("1.2.3.4")
        self.assertTrue(d.is_attack("1.2.3.4"))
        self.assertFalse(d.is_attack("5.6.7.8"))

class TestRateLimiter(unittest.TestCase):
    def test_limit(self):
        rl = RateLimiter(max_requests=3, window=60)
        self.assertTrue(rl.allow("user1"))
        self.assertTrue(rl.allow("user1"))
        self.assertTrue(rl.allow("user1"))
        self.assertFalse(rl.allow("user1"))

if __name__ == "__main__": unittest.main()
