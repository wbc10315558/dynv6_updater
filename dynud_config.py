import sys
from os import system
import json

#定义程序能够执行的动作
verbs=[
    "set",
    "get",
]
#定义set动作之后能配哪些参数
allow_set=[
    "token",
    "domain",
    "interval",
    "retry_interval"
]
#定义get动作之后能配哪些参数
allow_get=[
    "token",
    "domain",
    "interval",
    "retry_interval",
]
#定义帮助字符串
help_message="""用法: dynud_config <verb> <option>

set:设定某个字段为特定值
get:获取某个字段的值

示例：
dynud_config set token ABCDEFG12345678\t--------设置HTTP标识符为ABCDEFG12345678
dynud_config set domain example.dynv6.net\t--------设置解析的域名为example.dynv6.net
"""

#定义Config对象，用于自动以默认值补全对应的参数
class Config:
    
    def __init__(self,token="",domain="",
                 interval=60,retry_interval=10):
        self.token = token
        self.domain = domain
        self.interval = interval
        self.retry_interval = retry_interval
        
    def self_dump(self):
        return self.__dict__

#读取配置文件，若文件不存在则从默认配置开始
try:
    config = json.load(open("dynud.json", "r+"))
except FileNotFoundError:
    config = Config(**{}).self_dump()
except json.JSONDecodeError:
    config = Config(**{}).self_dump()

def count(a:list,b:list):
    ct=0
    for i in a:
        ct+=b.count(i)
    return ct

def main():
    
    #如果没有指定动作，默认打印帮助字符串
    if count(verbs,sys.argv)==0:
        print(help_message)
        return 0
    
    #如果存在多个动作参数，打印错误消息
    elif count(verbs,sys.argv)>1:
        print("错误：动作参数（set,get）每次只能使用一个")
        return 1
    
    #其他情况则继续操作
    else:
        
        #如果发现set动作，检查要设置的字段是否在allow_set的范围内
        #以防用户写入无关的参数
        if "set" in sys.argv:
            try:
                key=sys.argv[sys.argv.index("set")+1]
                if key in allow_set:
                    value=sys.argv[sys.argv.index("set")+2]
                    config[key]=value
                    print("字段 {} 已被设置为 {}".format(key,value))
                    return 0
                else:
                    print("未知字段: {}".format(key))
                    return 1
            except IndexError:
                print("错误用法：{}".format(' '.join(sys.argv)))
                return 1
            
        elif "get" in sys.argv:
            try:
                key=sys.argv[sys.argv.index("get")+1]
            except IndexError:
                print("错误用法：{}".format(' '.join(sys.argv)))
                return 1
            if key == "token":
                print("安全策略禁止获取HTTP标识符的操作")
                return 0
            elif key in allow_get:
                value=config[key]
                print(value)
                return 0
            
main()
print("正在将配置保存到文件......")
json.dump(config,open("dynud.json","w"))
system("pause")
            