import sys
from requests import get as send_request
from socket import gethostname
from psutil import net_if_addrs as get_ip_address

SYSTEM_PLATFORM=sys.platform
args=iter(sys.argv)

