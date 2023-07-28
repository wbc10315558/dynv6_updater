from ipaddress import IPv6Address, IPv4Address
from socket import getaddrinfo, gethostname, AF_INET6, AF_INET
from sys import argv, exit
from requests import request
from json import loads as json_load
from json.decoder import JSONDecodeError

# Created by wbc
# This tool aims to help dynv6 users to update ipv6 address to the dynv6 name server.
# You can either create a configuration file that contains information or just typing it
# when the program needs you to provide information.

def get_global_ip_address():
    """Get all global IP addresses"""
    global_ipv4: list[str] = []
    global_ipv6: list[str] = []
    for ip_tuple in getaddrinfo(gethostname(), 80):
        af = ip_tuple[0]
        ip_string = ip_tuple[4][0]
        if af.value == AF_INET:
            ip = IPv4Address(ip_string)
            if ip.is_global:
                global_ipv4.append(str(ip))
        elif af.value == AF_INET6:
            ip = IPv6Address(ip_string)
            if ip.is_global:
                global_ipv6.append(str(ip))
    return global_ipv4, global_ipv6

def case_multiple_ip(pool):
    """When multiple IPv6 addresses are found, call this function to let user choose one."""
    print(
        'Multiple IPv6 Addresses were found on your device.\n'
        "We strongly recommend you to choose the temporary address to avoid MAC address exposure."
    )
    for i in pool:
        print(i)
    while True:
        try:
            choice = int(input(f"Please choose [1-{len(pool)}]:"))-1
        except ValueError:
            choice = None
            continue
        if choice in range(len(pool)):
            break
    return pool[choice]

def load_configuration_file(filepath):
    try:
        file = open(filepath)
        config = json_load(file.read())
        token, hostname, ip = config["token"], config["hostname"], config['ip']
        if ip in ['auto', 'default', '']:
            ip = get_ipv6_address(ip)
        file.close()
    except FileNotFoundError:
        exit(f"Can't open {filepath}: No such file or directory.")
    except UnicodeError:
        exit(f"Can't read {filepath}: File encoding must be utf-8.")
    except JSONDecodeError:
        exit(f"Can't read {filepath}: A configuration file must follow JSON standard.")
    except KeyError:
        exit(f"Can't enable {filepath}: Missing key information.")
    return token, hostname, ip

def case_no_config_file():
    print("\nConfiguration file not specified, changing to interactive mode.\n")
    tk = input("HTTP Token: ")
    hstn = input("Configuring zone: ")
    ipa = input("Destination IP address (leave it empty to use the current address by default): ")
    if ipa in ['auto', 'default', '']:
        ipa = get_ipv6_address(ipa)
    return tk, hstn, ipa

def get_ipv6_address(mode):
    print("\nGetting current IPv6 address...")
    ipv6_pool = get_global_ip_address()[1]
    if mode == '' and len(ipv6_pool) >= 2:
        ipv6_address = case_multiple_ip(ipv6_pool)
    else:
        ipv6_address = ipv6_pool[0]
    return ipv6_address

def make_url(token, hostname, ipv6_address):
    url = f"http://dynv6.com/api/update?hostname={hostname}&ipv6={ipv6_address}&token={token}"
    return url

def make_request(url):
    response = request("get", url)
    if response.status_code == 200:
        print(response.text)

def main():
    if len(argv) < 2:
        make_request(make_url(*case_no_config_file()))
    else:
        if ('-h' in argv) or ('--help' in argv):
            print(f"Usage: python {argv[0]} [Configuration file path]")
        elif len(argv) == 2:
            make_request(make_url(*load_configuration_file("config.json")))
        else:
            print("Invalid arguments.")

main()
