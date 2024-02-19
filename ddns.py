import requests
import http.client
import json
from datetime import datetime

# 获取当前IP地址
def get_current_ip():
    with open('ip.txt', 'r') as file:
        ip = file.readline().strip()
    return ip

# 上传IP地址到Cloudflare
def dns_update_ip(ip):
    CF_Email = "alice@example.com"
    CF_Token = "0932a09c9a9d"
    CF_Zone_ID = "a900b9a9d8a9"
    CF_API_Key = "cb7de90"

    headers = {
        'Content-Type': "application/json",
        'X-Auth-Email': CF_Email,
        'X-Auth-Key': CF_API_Key,
        'Authorization': 'Bearer ' + CF_Token,
    }

    conn = http.client.HTTPSConnection("api.cloudflare.com")

    payload = {
        "type": "A",
        "name": "example.com",  # 修改为你的域名
        "content": ip,
        "ttl": 120,
    }

    conn.request("PUT", f"/client/v4/zones/{CF_Zone_ID}/dns_records/09f0ea0", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

# 主函数
def main():
    ip = get_current_ip()
    dns_update_ip(ip)

if __name__ == '__main__':
    main()
