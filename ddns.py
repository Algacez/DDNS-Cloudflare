import requests
import http.client
import json
from datetime import datetime

# 清除ip.txt的内容
open('ip.txt', 'w').close()

# 发送GET请求获取IP地址
url = 'http://api.ipify.org'
response = requests.get(url)

if response.status_code == 200:
    # 将IP地址保存到ip.txt文件中
    with open('ip.txt', 'w') as file:
        file.write(response.text + '\n')
    
    # 将当前时间和IP地址保存到logs.txt文件中
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    with open('logs.txt', 'a') as log_file:
        log_file.write(f"{current_time} - {response.text}\n")
    
    print('IP地址已保存到ip.txt文件中，并已保存日志到logs.txt文件中。')

    # 上传IP地址到Cloudflare
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
        "content": response.text,
        "ttl": 120,
    }

    conn.request("PUT", f"/client/v4/zones/{CF_Zone_ID}/dns_records/09f0ea0", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
else:
    print('获取IP地址失败。')
