import json
from module.wallet_module import password_check  
from module.wallet_error import PasswordError

try:
    # 通过该函数获取钱包组的地址,账户列表,钱包组名称,密码校验结果
    acct_address_list,acct_list,wallet_group_name = password_check()

    # 询问是否打印private_key_hex
    print("是否保存私钥? y/n")
    # 如果输入y,则打印私钥
    if input() == 'y':
        local_acct_list =[] # 创建新的json列表
        for acct in acct_list: # 保存私钥到新的json列表
            local_acct_list.append(acct._private_key.hex()) 
        #保存私钥到新的json文件
        with open(f'.\\eth_acc\\{wallet_group_name}_pkeys_decrypt.json', 'w') as f:
            json.dump(local_acct_list, f, indent=4)
    else:
        print("已取消打印")

except FileNotFoundError as e:
    print(e)
except PasswordError as e:
    print(e)

finally:
    print('程序结束')