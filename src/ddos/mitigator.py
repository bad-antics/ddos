"""DDoS mitigation and detection"""
import time, os
from collections import defaultdict

class DDoSDetector:
    def __init__(self, threshold=100, window=10):
        self.threshold = threshold
        self.window = window
        self.connection_counts = defaultdict(list)
    
    def record_connection(self, source_ip):
        now = time.time()
        self.connection_counts[source_ip].append(now)
        self.connection_counts[source_ip] = [t for t in self.connection_counts[source_ip] if now - t < self.window]
    
    def is_attack(self, source_ip):
        return len(self.connection_counts.get(source_ip, [])) > self.threshold
    
    def get_attackers(self):
        return {ip: len(times) for ip, times in self.connection_counts.items() if len(times) > self.threshold}
    
    def generate_iptables_rules(self, attackers=None):
        rules = []
        for ip in (attackers or self.get_attackers()):
            rules.append(f"iptables -A INPUT -s {ip} -j DROP")
        return rules

class RateLimiter:
    def __init__(self, max_requests=100, window=60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)
    
    def allow(self, client_id):
        now = time.time()
        self.requests[client_id] = [t for t in self.requests[client_id] if now - t < self.window]
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        self.requests[client_id].append(now)
        return True
