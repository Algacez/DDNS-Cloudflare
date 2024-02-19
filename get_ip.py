import requests
from requests.structures import CaseInsensitiveDict
#获取公网ipv4
ipv4 = requests.get('https://ipinfo.io/ip').text.strip()
#获取公网ipv6
ipv6 = requests.get('https://6.ipw.cn/').text.strip()
