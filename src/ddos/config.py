"""DDoS Config"""
ATTACK_TYPES = ["syn_flood", "udp_flood", "http_flood", "slowloris", "dns_amplification", "ntp_amplification"]
DEFAULT_THREADS = 50
DEFAULT_DURATION = 30
MAX_PACKET_SIZE = 65535
RATE_LIMIT = 10000
SAFE_MODE = True
