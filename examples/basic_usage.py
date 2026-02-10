from ddos.mitigator import DDoSDetector, RateLimiter
d = DDoSDetector(threshold=50)
for i in range(100):
    d.record_connection("attacker.ip")
print("Attackers:", d.get_attackers())
print("Rules:", d.generate_iptables_rules())
