import sys
from os.path import exists
from re import findall
from requests import get as send_request
from socket import gethostname,getaddrinfo
from psutil import net_if_addrs as get_all_local_ip
from json import loads as eval_json
from exceptions import *
from predefined import *

STDOUT=sys.stdout
STDERR=sys.stderr
args=iter(sys.argv)

class Config:
    
    def __init__(self,**kwargs):
        self.__dict__=kwargs
        if "token" not in self.__dict__:
            exit("Missing argument: token")
        if "domain" not in self.__dict__:
            exit("Missing argument: domain")
        if "online_get_ip" not in self.__dict__:
            self.online_get_ip=False
        if "use_temp_address" not in self.__dict__:
            self.use_temp_address=True
        if "interval" not in self.__dict__:
            self.interval=60
        if "retry_interval" not in self.__dict__:
            self.retry_interval=10
        if "enable_ipv4" not in self.__dict__:
            self.enable_ipv4=False
        if "enable_ipv6" not in self.__dict__:
            self.enable_ipv6=True
    
    def __repr__(self):
        return "<Config File object>"
        
def load_configuration_file(filepath: str) ->Config:
    """加载配置文件"""
    try:
        if exists(filepath):
            config_data = eval_json(open(filepath,encoding='utf-8').read())
            return Config(**config_data)
        else:
            raise FileNotFoundError("无法打开 {}：没有那个文件和目录".format(filepath))
    except UnicodeError:
        exit("无法读取 {}：编码错误（仅支持UTF-8编码）".format(filepath))
    except JSONDecodeError:
        exit("无法读取 {}：配置文件必须符合JSON格式".format(filepath))
    
def make_url(token, hostname, ipv6_address):
    """根据提供的信息，生成用于访问的网址"""
    url = f"http://dynv6.com/api/update?hostname={hostname}&ipv6={ipv6_address}&token={token}"
    return url

def get_ipv4_address_locally():
    all_ip=get_all_local_ip()
a= get_all_local_ip()
pass