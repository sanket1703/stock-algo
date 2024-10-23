import socket
import dns


def check_mo_resolution():
    try:
        ip_address = socket.gethostbyname('openapi.motilaloswal.com')
        print(f"Domain resolved to IP: {ip_address}")
        return True
    except socket.gaierror:
        print("Can't resolve MO. Issue Connecting to MO.")
        return False
    
def check_connectivity():
    try:
        ip_address = socket.gethostbyname('google.com')
        print(f"Google resolved to IP: {ip_address}")
        if(not check_mo_resolution()):return False
        return True
    except socket.gaierror:
        print("Can't resolve google.Connectivity issue.")
        return False


def resolve_with_custom_dns(domain):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8']  # Use Google's public DNS
    try:
        answers = resolver.resolve(domain)
        print(answers)
        for rdata in answers:
            print(f"Resolved IP: {rdata}")
    except Exception as e:
        print(f"Failed to resolve {domain}: {e}")