from module.wallet_module import password_check
from module.wallet_error import WalletNumError, PasswordError

try:
    acct_address_list, acct_list, wallet_group_name = password_check()
    
    # 询问要查找的钱包序号
    wallet_num = int(input("请输入要查找的钱包序号: "))
    # 如果钱包序号不存在,则报错
    if wallet_num > len(acct_address_list):
        raise WalletNumError('钱包序号不存在')
    else:
        acct_address = acct_address_list[wallet_num]
        # 打印地址和校验地址
        print(f'address:{acct_address}')
    
except FileNotFoundError as e:
    print(e)
except PasswordError as e:
    print(e)
except WalletNumError as e:
    print(e)

else:
    # 询问是否打印private_key_hex
    print("是否打印该钱包私钥? y/n")
    # 如果输入y,则打印私钥
    if input() == 'y':
        print(
            f"""钱包组:{wallet_group_name}\n
            钱包编号:{wallet_num}\n
            钱包地址:{acct_address}\n
            private_key:{acct_list[wallet_num]._private_key.hex()}"""
            )
    else:
        print("已取消打印")

finally:
    print('程序结束')