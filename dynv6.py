import socket
from sys import argv, exit
from os import system as cmd
from socket import getaddrinfo, gethostname, AF_INET6,AF_INET
from ipaddress import IPv6Address, IPv4Address
from typing import List

if len(argv)!=2:
    exit("Usage: dynv6 <Configuration file>")


def get_global_ip_address():
    global_ip: list[str] = []
    all_ips = getaddrinfo(gethostname(), 80)
    for ip_tuple in all_ips:
        af = ip_tuple[0]
        if af.value==AF_INET:
            ip_object=IPv4Address(ip_tuple[4][0])
            if ip_object.is_global:
                global_ip.append(str(ip_object))
        elif af.value==AF_INET6:
            ip_object=IPv6Address(ip_tuple[4][0])
            if ip_object.is_global:
                global_ip.append(ip_tuple[4][0])
    return global_ip


a = get_global_ip_address()
print(a)

try:
    config = eval(open(argv[1]).read())
    token = config["token"]
    hostname = config["host"]
except Exception as e:
    exit(e)
