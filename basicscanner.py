class ScanResult():
    def __init__(self,ip_addr:str, mac_addr:str,vendor:str=None, tcp_ports:dict=None, udp_ports:dict=None):
        self.ip = ip_addr
        self.mac_address = mac_addr
        self.tcp_ports = tcp_ports
        self.udp_ports = udp_ports
    
    @property
    def tcp_open_ports(self):
        """Override this property for your use case"""
        return []
    
    @property
    def udp_open_ports(self):
        """Override this property for your use case"""
        return []

class BasicScanner():
    
    def __init__(self):
        self.host = "127.0.0.1"
        self.ports = {"range": [22, 1023], "select": ["3306", "8080"]}
    
    
    def online(self, addr:str):
        """Checks if host is online"""
        return True
    
    
    def scan(self, host:str, ports=None):
        """Perform a scan of `host` and return `ScanResult`"""
        return ScanResult("127.0.0.1", "FF:FF:FF:FF:FF")
    
