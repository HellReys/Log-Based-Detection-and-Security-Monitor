import re

class DetectionEngine:
    def __init__(self):
        self.rules = {
            "ssh_failed_password": r"Failed password for .* from (?P<ip>\d+\.\d+\.\d+\.\d+)",
            "invalid_user": r"Invalid user .* from (?P<ip>\d+\.\d+\.\d+\.\d+)",
            "sql_injection_attempt": r"(UNION SELECT|OR '1'='1'|SELECT.*FROM)"
        }


    def analyze(self,line):
        """It compares the log line against the rules."""
        if not line:
            return None

        for rule_name,pattern in self.rules.items():
            try:
                match = re.search(pattern,line)
                if match:
                    ip_address = "Unknown"
                    if "ip" in match.groupdict():
                        ip_address = match.group("ip")
                    return {
                        "rule": rule_name,
                        "ip": ip_address,
                        "message": line.strip()
                    }
            except re.error as e:
                print(f"Regex Error ({rule_name}): {e}")
        return None
