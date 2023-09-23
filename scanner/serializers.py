from rest_framework import serializers
from .models import Host, Config

class SimpleHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ['pk', 'name', 'ip_address', 'service_list', 'last_seen']

class DetailedHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ['name', 'ip_address', 'mac_address', 'vendor', 'udp', 'tcp', 'last_seen']


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ['network', 'mask_length', 'tcp_nmap_str', 'udp_nmap_str', 'dot_mask' ]

class DetailedConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ['network', 'mask_length', 'tcp_ports', 'udp_ports']