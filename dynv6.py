from ipaddress import IPv6Address, IPv4Address,AddressValueError
from socket import getaddrinfo, gethostname, AF_INET6, AF_INET
from sys import argv, exit
from requests import request
from json import loads as json_load
from json.decoder import JSONDecodeError


def get_global_ip_address():
    """获取公网IP地址"""
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

def load_configuration_file(filepath):
    """加载配置文件"""
    try:
        file = open(filepath,encoding='utf-8')
        config = json_load(file.read())
        token, hostname, ip = config["token"], config["hostname"], config['ip']#这里需要切换成所有的检查参数函数
        if ip in ['auto', 'default', '']:
            ip = get_ipv6_address(ip)
        else:
            check_ipv6(ip)
        file.close()
    except FileNotFoundError:
        exit("无法打开 {}：没有哪个文件和目录".format(filepath))
    except UnicodeError:
        exit("无法读取 {}：配置文件编码错误（仅支持UTF-8编码）".format(filepath))
    except JSONDecodeError:
        exit("无法读取 {}：配置文件必须符合JSON格式".format(filepath))
    except KeyError:
        exit("无法读取 {}：缺少参数{}".format(filepath,missing_arguments))
    return token, hostname, ip

def case_no_config_file():
    """当无配置文件时主动引导用户进行配置"""
    print("\nConfiguration file not specified, changing to interactive mode.\n")
    token = input("HTTP Token: ")
    hostname = input("Configuring zone: ")
    ip = input("Destination IP address (leave it empty to use the current address by default): ")
    if ip in ['auto', 'default', '']:
        ip = get_ipv6_address(ip)
    else:
        check_ipv6(ip)
    return token, hostname, ip

def get_ipv6_address(mode):
    """从公网IP地址中获取所需的IPv6地址"""
    print("\nGetting current IPv6 address...")
    ipv6_pool = get_global_ip_address()[1]
    if mode == '' and len(ipv6_pool) >= 2:
        ipv6_address = case_multiple_ip(ipv6_pool)
    else:
        ipv6_address = ipv6_pool[0]
    print(f"Using address: [{ipv6_address}]")
    return ipv6_address

def check_ipv6(addr):
    """检查配置文件中或用户提供的IPv6地址是否合法以及是否能在公网上使用"""
    try:
        ip_object=IPv6Address(addr)
        if not ip_object.is_global:
            exit("Given address is not available on the Internet. Please use another one.")
    except AddressValueError:
        exit("Invalid IPv6 address.")

def case_multiple_ip(pool):
    """当检测到本机有多个公网IPv6地址时，引导用户选择其一"""
    print(
        '\nMultiple IPv6 Addresses were found on your device.\n'
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

def make_url(token, hostname, ipv6_address):
    """根据提供的信息，生成用于访问的网址"""
    url = f"http://dynv6.com/api/update?hostname={hostname}&ipv6={ipv6_address}&token={token}"
    return url

def make_request(url:str):
    """在dynv6.com上执行更新解析规则的操作，并对将执行结果反馈给用户"""
    print("\nSending HTTP request to dynv6.com...\n")
    response = request("get", url)
    if response.status_code == 200:
        print("Status: 200/OK\nAddress updated.")
        exit(0)
    elif response.status_code == 401:
        exit("Status: 401/Unauthorized\nInvalid auth token, the request was rejected.")
    elif response.status_code == 404:
        exit("Status: 404/Not found:\nZone not found.")
    else:
        exit(f"Status: {response.status_code}\nUnknown error, please check your information or try again later.")

def main():
    """程序入口"""
    if len(argv) < 2:
        make_request(make_url(*case_no_config_file()))
    else:
        if ('-h' in argv) or ('--help' in argv):
            print(f"Usage: python {argv[0]} [Configuration file path]")
        elif len(argv) == 2:
            make_request(make_url(*load_configuration_file(argv[1])))
        else:
            exit("Invalid arguments.")

if __name__ == "__main__":
    main()
