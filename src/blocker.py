import subprocess
import os

class FirewallBlocker:
    def __init__(self):
        # Control the OS
        self.is_linux = os.name != 'nt'


    def block_ip(self, ip_address):
        """Adds a DROP rule for the given IP address using iptables."""
        if not self.is_linux:
            print(f"Blocking not supported on this OS: {ip_address}")
            return False

        try:
            command = ["sudo", "iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"]

            subprocess.run(command, check=True)
            print(f"[FIREWALL] Successfully blocked IP: {ip_address}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Firewall Error: Could not block {ip_address}. (Are you root?)")
            return False
