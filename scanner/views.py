import traceback, json
from time import sleep
from rest_framework.decorators import api_view
from django.http import HttpRequest, JsonResponse
from django.utils.timezone import now
from .models import Host, Config
from usermngr.models import Ticket
from .serializers import SimpleHostSerializer, DetailedConfigSerializer, DetailedHostSerializer
from usermngr.utils import isNotAuthenticated, DataResponse, ErrorResponse, check_login
from celerytasks.tasks import is_online



# Create your views here.
@api_view(['GET'])
@check_login
def index(request: HttpRequest):
    hosts = Host.objects.all().order_by('ip_address')
    return JsonResponse({"data": SimpleHostSerializer(hosts, many=True).data})
    

@api_view(['GET'])
@check_login
def host(request, id):
    host = Host.objects.filter(pk=id).first()
    return JsonResponse({"host": DetailedHostSerializer(host).data})


@api_view(['GET'])
@check_login
def config(request):
    config = Config.objects.all().first()
    return DataResponse(DetailedConfigSerializer(config).data, "config")

@api_view(["GET"])
@check_login
def online(request, id):
    host = Host.objects.filter(pk=id).first()
    if host is None:
        return DataResponse("Host does not exist!", "error", status=400)
    
    curtime = now()
    delta = curtime - host.last_seen
    if delta.total_seconds() <= 300: # If host has been online less or equal than 5 minutes ago
        return DataResponse(True, "online")
    
    # If last online was more than 5 minutes ago
    try:
        task = is_online.delay(host.ip_address)
        start = now()
        
        while not task.ready() and (now() - start).total_seconds() <= 30: # Waits for 30s then cancel
            sleep(0.1)
        
        if task.state == 'FAILURE':
            return DataResponse("Host discovery task has failed!", "error", status=500)
        
        if task.state != 'SUCCESS':
            return DataResponse("n/a", "online", status=204)
    
        if task.get():
            host.last_seen = now()
            host.save()
            return DataResponse(True, "online")
        return DataResponse(False, "online")
    except Exception as e:
        Ticket(
            name=str(e),
            context=__file__,
            info=traceback.format_exc()
        ).save()
        return DataResponse("Something went wrong", "error", status=500)

@api_view(['POST'])
@check_login
def update(request):
    try:
        data = json.loads(request.POST['ports'])
        ranges = [*map(lambda z: (int(data[z]['low']), int(data[z]['high'])), filter(lambda z: 'low' in data[z] and 'high' in data[z], data))]
        ports = [*map(lambda z: int(data[z]['port']), filter(lambda z: 'port' in data[z], data))]
        print(ranges, ports, sep='\n')
        full_ranges = [*map(lambda z: [*range(z[0], z[1] + 1)], ranges)]
        all_ports = []
        for rng in full_ranges:
            all_ports.extend(rng)
        all_ports.extend(ports)
        all_ports = [*filter(lambda z: z >= 22 and z <= 41951, all_ports)]
        all_ports = list(dict.fromkeys(all_ports))
        all_ports.sort()
        ranges = []
        ports = []
        
        
        i = 0
        while i < len(all_ports):
            j = i + 1
            while j < len(all_ports) and all_ports[j] - all_ports[j - 1] == 1:
                j += 1
            
            if j == i + 1:
                ports.append(all_ports[i])
                i += 1
            else:
                ranges.append((all_ports[i], all_ports[j - 1]))
                i = j
        print(ports)
        print(ranges)
            
    except Exception as e:
        Ticket(
            name=str(e),
            context=__file__,
            info=traceback.format_exc()
        ).save()
        return ErrorResponse("Failed to process request", code=500)
    
    return DataResponse('OK', 'status')