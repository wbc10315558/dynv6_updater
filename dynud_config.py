import sys
from psutil import net_if_stats
import json

ifaces=net_if_stats()
available_ifaces=[interface for interface in ifaces if ifaces[interface].isup]

class Config:
    
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
        if "token" not in self.__dict__:
            self.token = ""
        if "domain" not in self.__dict__:
            self.domain = ""
        if "use_temp_address" not in self.__dict__:
            self.use_temp_address = True
        if "interval" not in self.__dict__:
            self.interval = 30
        if "retry_interval" not in self.__dict__:
            self.retry_interval = 10
        if "enable_ipv4" not in self.__dict__:
            self.enable_ipv4 = False
        if "enable_ipv6" not in self.__dict__:
            self.enable_ipv6 = True
        if "ipv4_iface" not in self.__dict__:
            self.ipv4_iface = ""
        if "ipv6_iface" not in self.__dict__:
            self.ipv6_iface = ""
    
    def self_dump(self):
        return self.__dict__
    
try:
    config=json.load(open("dynud.json","r+"))
except FileNotFoundError:
    config=Config(**{}).self_dump()
except json.JSONDecodeError:
    config=Config(**{}).self_dump()
    
#程序能够执行的动作
verbs=[
    "set",
    "get",
    "enable",
    "disable",
    "help",
]
#以具体值呈现的设置
allow_set=[
    "token",
    "domain",
    "ipv4_iface",
    "ipv6_iface",
    "interval",
    "retry_interval"
]
#允许获取的设置
allow_get=[
    "token",
    "domain",
    "ipv4_iface",
    "ipv6_iface",
    "ifaces",
    "ipv4",
    "ipv6",
    "interval",
    "retry_interval",
    "use_temp_address",
]
#以布尔逻辑形式呈现的设置
allow_enable_disable=[
    "ipv4",
    "ipv6",
    "use_temp_address",
]

def count(a:list,b:list):
    ct=0
    for i in a:
        ct+=b.count(i)
    return ct

def main():
    if count(verbs,sys.argv)==0:
        print("No verbs found, try ‘help’ for more information.")
        return 0
    elif count(verbs,sys.argv)>1:
        print("Too many verbs.")
        return 0
        
    else:
        
        if "set" in sys.argv:
            key=sys.argv[sys.argv.index("set")+1]
            if key in allow_set:
                value=sys.argv[sys.argv.index("set")+2]
                config[key]=value
                print("Option {} has been set to {}".format(key,value))
                return 0
            else:
                print("Unknown option: {}".format(key))
                return 1
            
        elif "get" in sys.argv:
            key=sys.argv[sys.argv.index("get")+1]
            if key == "ipv4":
                print(config["enable_ipv4"])
                return 0
            elif key == "ipv6":
                print(config["enable_ipv6"])
                return 0
            elif key == "ifaces":
                print("\n".join(available_ifaces))
                return 0
            elif key == "token":
                print("Operation not allowed.")
                return 0
            elif key in allow_get:
                value=config[key]
                print(value)
                return 0
            
        elif "enable" in sys.argv:
            setting_to_be_enabled=sys.argv[sys.argv.index("enable")+1]
            if setting_to_be_enabled in allow_enable_disable:
                config["enable_"+setting_to_be_enabled]=True
                print("Enabled {}".format(setting_to_be_enabled))
                return 0
            else:
                print("Unknown option: {}".format(setting_to_be_enabled))
                return 1
                
        elif "disable" in sys.argv:
            setting_to_be_disabled=sys.argv[sys.argv.index("disable")+1]
            if setting_to_be_disabled in allow_enable_disable:
                config["enable_"+setting_to_be_disabled]=False
                print("Disabled {}".format(setting_to_be_disabled))
                return 0
            else:
                print("Unknown option: {}".format(setting_to_be_disabled))
                return 1
main()
json.dump(config,open("dynud.json","w"))
            