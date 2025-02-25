import json
import time

import requests
from bs4 import BeautifulSoup

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.xiaoyuzhoufm.com/',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}

url = "https://www.xiaoyuzhoufm.com/collection/podcast/67bc1526d3fc170cb3ec380e"

try:
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            break
        except requests.RequestException as e:
            if attempt == 2:
                raise e
            time.sleep(2)

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    scripts = soup.find_all("script", id="__NEXT_DATA__")
    for script in scripts:
        if script.string:
            try:
                data = json.loads(script.string)
                target_data = data["props"]["pageProps"]["collection"]["target"]
                pids = [item["pid"] for item in target_data if "pid" in item]
                print(f"所有 pid: {pids}")
            except json.JSONDecodeError:
                continue

except Exception as e:
    print(f"请求失败，错误信息: {e}") 