import requests
import http.client
import json
from datetime import datetime

domain = ""
CF_Email = ""
CF_Zone_ID = ""
CF_API_Key = ""
CF_Token = ""

def clear_ip_file():
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

def get_record_id(dns_name, zone_id):
    resp = requests.get(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(zone_id),
        headers={
            'Authorization': 'Bearer ' + CF_Token,
            'Content-Type': 'application/json'
        })
    if not json.loads(resp.text)['success']:
        return None
    domains = json.loads(resp.text)['result']
    for domain in domains:
        if dns_name == domain['name']:
            return domain['id']
    return None

def dns_update_ip(ip, dns_name, zone_id):
    record_id = get_record_id(dns_name, zone_id)
    if record_id is None:
        print('找不到DNS记录。')
        return

    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer ' + CF_Token,
    }

    conn = http.client.HTTPSConnection("api.cloudflare.com")

    payload = {
        "type": "A",
        "name": dns_name,
        "content": ip,
    }

    conn.request("PUT", f"/client/v4/zones/{zone_id}/dns_records/{record_id}", json.dumps(payload), headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

def main():
    clear_ip_file()
    get_ip_and_save()
    ip = get_current_ip()
    dns_name = domain  
    dns_update_ip(ip, dns_name, CF_Zone_ID)

if __name__ == '__main__':
    main()