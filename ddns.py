import requests
import http.client
import json
from datetime import datetime

def clear_ip_file():
    # 清除ip.txt的内容
    open('ip.txt', 'w').close()

def get_ip_and_save():
    url = 'http://api.ipify.org'
    response = requests.get(url)

    if response.status_code == 200:
        with open('ip.txt', 'w') as file:
            file.write(response.text + '\n')

        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        with open('logs.txt', 'a') as log_file:
            log_file.write(f"{current_time} - {response.text}\n")

        print('IP地址已保存到ip.txt文件中，并已保存日志到logs.txt文件中。')
    else:
        print('获取IP地址失败。')

def get_current_ip():
    with open('ip.txt', 'r') as file:
        ip = file.readline().strip()
    return ip

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

def main():
    clear_ip_file()
    get_ip_and_save()
    ip = get_current_ip()
    dns_update_ip(ip)

if __name__ == '__main__':
    main()
