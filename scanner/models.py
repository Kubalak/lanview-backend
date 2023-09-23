from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Host(models.Model):
    name = models.CharField(max_length=128)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=18)
    vendor = models.CharField(max_length=128)
    tcp_services = models.JSONField()
    udp_services = models.JSONField()
    last_seen = models.DateTimeField()
    
    
    @property
    def service_list(self):
        """
        Lists open ports returned by nmap as dict in format
        >>> host = Host.objects.all().first()
        >>> host.services
        {'udp': {'53': {'state': 'open', ...}}, 'tcp': {'80':{'state': 'open', ...}}}
        """
        tcp = filter(lambda z: z is not None,
            map(lambda z: z if self.tcp_services[z]["state"] == 'open' else None, self.tcp_services)
        )
        udp = filter(lambda z: z is not None,
            map(lambda z: z if self.udp_services[z]["state"] == 'open' else None, self.udp_services)
        )
        return {"udp":[*udp], "tcp": [*tcp]}

    
    @property
    def tcp(self):
        return [*filter(lambda z: z is not None,
            map(lambda z: {"port": z,"info": self.tcp_services[z]} if self.tcp_services[z]["state"] == 'open' else None, self.tcp_services))
        ]
        

    @property
    def udp(self):
        return [*filter(lambda z: z is not None,
            map(lambda z: {"port": z,"info": self.udp_services[z]} if self.udp_services[z]["state"] == 'open' else None, self.udp_services))
        ]

class Exclusion(models.Model):
    name = models.CharField(max_length=64)
    address = models.GenericIPAddressField(unique=True)
    tcp_ports = models.JSONField()
    udp_ports = models.JSONField()

class Config(models.Model):
    network = models.GenericIPAddressField()
    mask_length = models.IntegerField(
        default=24,
        validators=[
            MaxValueValidator(30),
            MinValueValidator(8)
        ]
    )
    tcp_ports = models.JSONField()
    udp_ports = models.JSONField()
    
    @classmethod
    def create(network,mask_length=24, tcp_ranges=None, tcp_select=None, udp_ranges=None, udp_select=None):
        if mask_length < 8 or mask_length > 30:
            raise ValueError("Bad network mask length")
        if tcp_ranges is not None and not isinstance(tcp_ranges, list):
            raise ValueError
        
    
    @property
    def tcp_nmap_str(self):
        """
        Returns tcp ports to scan in nmap compatible format.
        >>> config = Config.objects.first()
        >>> config.tcp_nmap_str
        20-1024,3000-3200,5000,8080
        """
        if "range" not in self.tcp_ports:
            raise ValueError("Missing \"range\" in tcp_ports")
        if "select" not in self.tcp_ports:
            raise ValueError("Missing \"select\" in tcp_ports")
        
        ranges = selected = ""
        
        if len(self.tcp_ports["range"]) > 0:
            ranges = ",".join([*map(lambda z: f"{z[0]}-{z[1]}",self.tcp_ports["range"])])
        if len(self.tcp_ports["select"]) > 0:
            selected = ",".join([*map(lambda z: str(z), self.tcp_ports["select"])])
            
        if selected != "" and ranges != "":
            return f"{ranges},{selected}"
        elif selected == "":
            return ranges
        elif ranges == "":
            return selected
        
        return ""
    
    @property
    def udp_nmap_str(self):
        if "range" not in self.udp_ports:
            raise ValueError("Missing \"range\" in tcp_ports")
        if "select" not in self.udp_ports:
            raise ValueError("Missing \"select\" in tcp_ports")
        
        ranges = selected = ""
        
        if len(self.udp_ports["range"]) > 0:
            ranges = ",".join([*map(lambda z: f"{z[0]}-{z[1]}",self.udp_ports["range"])])
        if len(self.udp_ports["select"]) > 0:
            selected = ",".join([*map(lambda z: str(z), self.udp_ports["select"])])
        
        if selected != "" and ranges != "":
            return f"{ranges},{selected}"
        elif selected == "":
            return ranges
        elif ranges == "":
            return selected
        
        return ""
    
    @property
    def dot_mask(self):
        full = int(self.mask_length / 8)
        last = self.mask_length % 8
        masks = ["0", "128", "192", "224", "240", "248", "252", "255"]
        mask = ["255" for _ in range(full)]
        mask.append(masks[last])
        for _ in range(4 - (full + 1)):
            mask.append("0")
        return ".".join(mask)

