import sys
from os.path import exists
from re import findall
from requests import get as send_request
from socket import gethostname
from psutil import net_if_addrs as get_ip_address
from json import loads as eval_json
from exceptions import *
from predefined import *

STDOUT=sys.stdout
STDERR=sys.stderr
args=iter(sys.argv)

class Config:
    def __init__(self,**kwargs):
        self.__dict__=kwargs
        
    def __setitem__(self, key, value):
        if key in AVAILABLE_ARGUMENTS:
            self.__dict__[key]=value
def load_configuration_file(filepath: str):
    """加载配置文件"""
    try:
        if exists(filepath):
            config = eval_json(open(filepath,encoding='utf-8').read())
        else:
            raise FileNotFoundError("无法打开 {}：没有哪个文件和目录".format(filepath))
    except UnicodeError:
        exit("无法读取 {}：配置文件编码错误（仅支持UTF-8编码）".format(filepath))
    except JSONDecodeError:
        exit("无法读取 {}：配置文件必须符合JSON格式".format(filepath))
    # except KeyError:
    #     exit("无法读取 {}：缺少参数{}".format(filepath,missing_arguments))
    # return token, hostname, ip
