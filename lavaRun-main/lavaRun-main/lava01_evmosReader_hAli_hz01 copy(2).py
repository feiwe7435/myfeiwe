import requests
import json
import time
import random

# 将你的所有Evmos节点RPC URL存储在一个列表中
EVMOS_RPC_URLS = [
    'https://eth1.lava.build/lava-referer-aba21921-66ed-4d62-9424-4b36f92be407/',
    'https://eth1.lava.build/lava-referer-a418ce01-4a9a-4690-ab37-88f1705c8e42/',
    'https://eth1.lava.build/lava-referer-5c1d6746-77ce-4a20-b408-d6432e8851e5/',
    'https://eth1.lava.build/lava-referer-352973e6-c0a7-455f-ba22-dfb862717d50/',
    'https://eth1.lava.build/lava-referer-7bce48bf-5d4f-40d9-8a2a-a3bc1874495f/',
    'https://eth1.lava.build/lava-referer-7206c8dc-bab5-43e8-b1cc-f0888bf66c16/',
    'https://eth1.lava.build/lava-referer-7d5d102a-8015-415b-8da4-a079220a462a/',
    'https://eth1.lava.build/lava-referer-6fa09fff-1d8a-493b-8886-21f82c602d13/',
    'https://eth1.lava.build/lava-referer-9de9367f-7944-44ff-8280-e7c0ac6260a7/',
    'https://eth1.lava.build/lava-referer-a650507b-8a27-4c29-b5b5-f446742f9f15/'

]


def get_evmos_balance(address):
    # 随机选择一个EVMOS_RPC_URL
    evmos_rpc_url = random.choice(EVMOS_RPC_URLS)

    # 构建JSON-RPC请求
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        # 发起POST请求
        response = requests.post(evmos_rpc_url, headers=headers, data=json.dumps(payload))
        # 解析响应并返回以太坊余额（以wei为单位）
        if response.status_code == 200:
            balance_wei = int(response.json()['result'], 16)
            return balance_wei
        else:
            print(
                f"Failed to fetch balance for address {address} from {evmos_rpc_url}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching balance for address {address} from {evmos_rpc_url}: {str(e)}")
        return None


# 读取外部JSON文件，获取大地址列表
with open('1_address.json', 'r') as json_file:
    big_address_list = json.load(json_file)

while True:
    # 随机选择一个地址
    random_address = random.choice(big_address_list)

    # 在请求之前暂停一个随机的时间间隔
    time_to_sleep = random.uniform(1, 2)
    print(f"Waiting for {time_to_sleep:.2f} seconds...")
    time.sleep(time_to_sleep)

    balance_wei = get_evmos_balance(random_address)
    if balance_wei is not None:
        # 将wei转换为以太币，并打印结果
        balance_evmos = balance_wei / 10 ** 18
        print(f"Address: {random_address}, Balance: {balance_evmos} EVMOS")

    # 在每次迭代结束时暂停，以避免无限快速循环
    # 这里的暂停时间（例如，10秒）可以根据需要调整
    time.sleep(3)
    # 可以在这里添加一个退出条件
    # 例如，检查某个特定的文件是否存在，如果存在则中断循环
    # if os.path.exists('stop.txt'):
    #     break
