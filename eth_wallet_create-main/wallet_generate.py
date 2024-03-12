from cryptography.fernet import Fernet
import json
import os
from module.wallet_module import generate_wallet

try :
    # 输入钱包组名称
    wallet_group_name = input("请输入钱包组名称: ")
    # 如果钱包已存在则报错
    if os.path.exists(f'.\\eth_acc\\{wallet_group_name}_password.json'):
        raise FileExistsError('钱包组已存在')
    # 输入希望创建钱包数量
    num_wallets = int(input("请输入要生成的钱包数量: "))
    
    # 通过该函数生成一个钱包组,包含密码,地址,加密后的私钥第1段,加密后的私钥第2段
    wallets_address,password,wallets_private_key01,wallets_private_key02 = generate_wallet(num_wallets)

    # 保存密码到一个单独的JSON文件,此处可修改保存路径
    with open(f'.\\eth_acc\\{wallet_group_name}_password_保存到其他位置.json', 'x') as f:# 保存密码到一个单独的JSON文件,x表示如果文件已存在则报错
        json.dump({'password': password.decode()}, f, indent=4)
    with open(f'.\\eth_acc\\{wallet_group_name}_address.json', 'x') as f: # 保存地址到一个单独的JSON文件,x表示如果文件已存在则报错
        json.dump(wallets_address, f, indent=4)
    with open(f'.\\eth_acc\\{wallet_group_name}_pkeys01.json', 'x') as f: # 保存加密后的私钥第1段到一个单独的JSON文件,x表示如果文件已存在则报错
        json.dump(wallets_private_key01, f, indent=4)
    with open(f'.\\eth_acc\\{wallet_group_name}_pkeys02.json', 'x') as f: # 保存加密后的私钥第2段到一个单独的JSON文件,x表示如果文件已存在则报错
        json.dump(wallets_private_key02, f, indent=4)

except FileExistsError:
    print('钱包组已存在')

finally:
    print('程序结束')