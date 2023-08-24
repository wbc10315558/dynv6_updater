import sys
from time import sleep,asctime
from os.path import exists
from requests import get as send_request
from json import load as read_json
from json import JSONDecodeError

def load_configuration_file(filepath: str):
    """加载配置文件"""
    try:
        if exists(filepath):
            config_data = read_json(open(filepath,encoding='utf-8'))
            return config_data
        else:
            raise FileNotFoundError("无法打开 {}：没有那个文件和目录".format(filepath))
    except UnicodeError:
        exit("无法读取 {}：编码错误（仅支持UTF-8编码）".format(filepath))
    except JSONDecodeError:
        exit("无法读取 {}：配置文件必须符合JSON格式".format(filepath))
    
def make_url(token, domain, ipv6_address="auto"):
    url = f"http://dynv6.com/api/update?hostname={domain}&ipv6={ipv6_address}&token={token}"
    return url

def main():
    while True:
        config = load_configuration_file("dynud.json")
        res=send_request(make_url(config["token"],config["domain"]))
        if res.status_code==200:
            print("{} [INFO] Address Updated.".format(asctime()),file=open("dynud.log","r+"))
            sleep(config["interval"])
        else:
            print("{} [ERROR] Request Failed: {}".format(asctime(),res.status_code),file=open("dynud.log","r+"))
            sleep(config["retry_interval"])

main()
