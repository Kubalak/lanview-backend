from django.utils.timezone import make_aware
from celery import shared_task
from .celery import app
import ipaddress, nmap, traceback

@shared_task
def scan():

    from usermngr.models import  Ticket
    from scanner.models import Config
    result = []
    try:
        scanner = nmap.PortScanner()
        config = Config.objects.first()
        result = [*map(lambda ip: {"ip": str(ip), "scan": scanner.scan(str(ip),arguments="-v -sP -sn -PR", sudo=True)}, ipaddress.IPv4Network(f"{config.network}/{config.mask_length}"))]
    except Exception as e:
        print("Warn: ", e)
        ticket = Ticket.objects.create(
            name = str(e),
            context = __file__,
            info = traceback.format_exc()
        )
        ticket.save()
    try:
        hosts = [*filter(lambda z: z is not None, map(lambda z: z["ip"] if int(z["scan"]["nmap"]["scanstats"]["uphosts"]) >= 1 else None, result))]
        
        for host in hosts:
            scanHost.delay(host)
    except Exception as e:
        ticket = Ticket.objects.create(
            name = str(e),
            context = __file__,
            info = traceback.format_exc()
        )
        ticket.save()

@shared_task
def scanHost(host:str):
    """Performs network scan for host given in `host` param.\n
    Scan creates a new entry in `ScanResult` table.\n
    New hosts are saved in `Host` table.\n
    Exceptions are not saved (for now)
    """
    import nmap
    from datetime import datetime
    from usermngr.models import Ticket
    from scanner.models import Host, Config
    import traceback
    
    config = Config.objects.first()
    scanner = nmap.PortScanner()
    result = scanner.scan(host, ports=config.tcp_nmap_str, sudo=True)
    
    hosts = Host.objects.filter(ip_address=host)
    
    if "scan" not in result and hosts.count() == 0:
        Host(
            name = "N/A",
            ip_address = host,
            mac_adress = "N/A",
            vendor = "N/A",
            tcp_services = [],
            udp_services = [],
            last_seen = make_aware(datetime.now())
        ).save()
        return
    elif "scan" not in result or host not in result["scan"]:
        return 
    scan = result["scan"][host]
    mac = scan["addresses"]["mac"] if "mac" in scan["addresses"] else None
    
    if hosts.count() > 1 and mac is not None:
        hosts = hosts.filter(mac_address=mac)
    
    tcp = []
    udp = []
    if "tcp" in scan:
        tcp = [*map(lambda z: {
            'port': z,
            'state': scan["tcp"][z]['state'],
            'reason': scan["tcp"][z]['reason'],
            'name': scan["tcp"][z]['name'],
            'product': scan["tcp"][z]['product'],
            'version': scan["tcp"][z]['version'],
            'extra': scan["tcp"][z]['version'],
        }, scan["tcp"])]
    
    try:
        if hosts.count() == 0:  
            hostinfo = Host(
                name = scan["hostnames"][0]["name"],
                ip_address = host,
                mac_address = scan["addresses"]["mac"] if "mac" in scan["addresses"] else "N/A",
                vendor = scan["vendor"][scan["addresses"]["mac"]] if "mac" in scan["addresses"] and scan["addresses"]["mac"] in scan["vendor"] else "N/A",
                tcp_services = tcp,
                udp_services = udp,
                last_seen = make_aware(datetime.now())
            )
            hostinfo.save()
        elif hosts.count() == 1:
            hostinfo = hosts[0]
            if mac is not None:
                hostinfo.mac_address = mac
            if hostinfo.vendor == "N/A":
                hostinfo.vendor = scan["vendor"][scan["addresses"]["mac"]] if "mac" in scan["addresses"] and scan["addresses"]["mac"] in scan["vendor"] else "N/A"
            hostinfo.tcp_services = tcp
            hostinfo.udp_services = udp
            hostinfo.last_seen = make_aware(datetime.now())
            hostinfo.save()
        else:
            print("Not implemented!")
    except Exception as e:
        ticket = Ticket.objects.create(
            name=str(e),
            context=__file__,
            info=traceback.format_exc(),
        )
        ticket.save()

@app.task(bind=True)
def is_online(self, host):
    try:
        scanner = nmap.PortScanner()
        result = scanner.scan(host, arguments="-v -PR -sn -sP", sudo=True)
        if result['nmap']['scanstats']["uphosts"] == '1':
            return True
        return False
    except Exception as e:
        self.update_state(state='FAILURE')
