import requests
from datetime import datetime

# 清除ip.txt的内容
open('ip.txt', 'w').close()

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
