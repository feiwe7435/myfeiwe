from cryptography.fernet import Fernet,InvalidToken
from web3 import Web3
import json
import os
from module.wallet_error import PasswordError

# 生成钱包账户
def generate_wallet(num_wallets):
    w3 = Web3()
    wallets_address = []
    wallets_private_key01 = []
    wallets_private_key02 = []
    # 生成一个随机的加密密码,该密码为bytes格式
    password = Fernet.generate_key()
    
    # 生成指定数量的私钥和地址, 并加密私钥
    for i in range(num_wallets):
        acct = w3.eth.account.create() # 创建账户对象,该对象中包含了地址私钥等信息
        address = acct.address # 获取新创建账户的地址
        p_key = acct._private_key # 获取新创建账户的私钥
    
        fernet_obj = Fernet(password) # 生成Fernet对象,需要导入bytes格式的密码
        encrypted_private_key = fernet_obj.encrypt(p_key).decode('utf-8') # 通过Fernet对象加密私钥,并转换为utf-8格式
    
        encrypted_private_key_length = len(encrypted_private_key) // 2 # 获取加密后的私钥中间长度
        encrypted_private_key01 = encrypted_private_key[:encrypted_private_key_length] # 截取前半段
        encrypted_private_key02 = encrypted_private_key[encrypted_private_key_length:] # 截取后半段
    
        wallets_address.append(address) # 将地址添加到列表
        wallets_private_key01.append(
            encrypted_private_key01) # 将加密后的私钥第1段添加到列表
        wallets_private_key02.append(
            encrypted_private_key02) #  将加密后的私钥第2段添加到列表
        
    return wallets_address,password,wallets_private_key01,wallets_private_key02

# 解密合并的私钥并推导出的账户数据,该函数会导入下方的password_check函数
def get_acc(wallet_group_name, password):
        # 合并私钥json
        try:
            filepath01 = f'.\\eth_acc\\{wallet_group_name}_pkeys01.json' # 读取加密后的私钥第1段
            filepath02 = f'.\\eth_acc\\{wallet_group_name}_pkeys02.json' # 读取加密后的私钥第2段
            if not os.path.exists(filepath01) or not os.path.exists(filepath02):
                raise FileNotFoundError() # 如果文件1和文件2有任何一个不存在,则报错文件不存在
            # 从JSON文件1加载钱的私钥01
            with open(filepath01, 'r') as f01:
                pkeys_data01 = json.load(f01)
            # 从JSON文件2加载钱的私钥02
            with open(filepath02, 'r') as f02:
                pkeys_data02 = json.load(f02)
            # 通过正则表达式合并私钥列表
            pkeys_data = [x + y for x, y in zip(pkeys_data01, pkeys_data02)]
        except FileNotFoundError:
            return False # 不在此处处理错误,因为函数内报错的话,函数外的程序还会继续执行
        
        # 解密私钥
        private_key_bytes=[]
        # 遍历私钥列表
        for pkey_data in pkeys_data:
            try:
                # 将未解密的私钥一个一个解密
                private_key_byte = Fernet(password.encode('utf-8')).decrypt(pkey_data.encode('utf-8'))
            # 如果密码不是fernet格式,或者不是原始密码,则解密失败,报错    
            except  (ValueError, InvalidToken):
                return False
            # 将解密后的私钥添加到列表
            private_key_bytes.append(private_key_byte)

        # 将私钥转换为16进制字符串,为0x开头私钥列表
        private_key_hexs = [pk.hex() for pk in private_key_bytes]
        w3 = Web3()
        acct_list = []
        # 遍历16进制私钥列表
        for private_key_hex in private_key_hexs:
            # 创建一个LocalAccount对象列表,通过将16进制私钥转换为bytes推导出了地址等信息
            acct = w3.eth.account.from_key(bytes.fromhex(private_key_hex))
            # 将LocalAccount对象添加到列表
            acct_list.append(acct)
        return acct_list

# 检查密码是否正确
def password_check():
    try:
        # 输入钱包组名称
        wallet_group_name = input("请输入钱包组名称: ")
        file_path = f'.\\eth_acc\\{wallet_group_name}_address.json'
        # 查询文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError('未找到钱包组') 
        # 如果文件存在，读取文件内容
        with open(file_path, 'r') as f:
            check_address_list = json.load(f)
        # 输入密码
        password = input("请输入密码:")
        # 解密合并的私钥并推导出的账户数据
        acct_list = get_acc(wallet_group_name,password)
        # 如果密码错误,函数返回acct_list=false,则报错
        if acct_list == False:
            raise PasswordError('密码错误')
        # 通过列表推导式获取地址列表
        acct_address_list = [acct.address for acct in acct_list]
        # 如果地址列表和文件中的地址列表不一致,则报错
        if acct_address_list != check_address_list:
            raise PasswordError('密码错误')
        
    except FileNotFoundError:
        raise
    except PasswordError:
        raise
    # 如果没有报错,则返回地址列表,账户列表,钱包组名称,密码校验结果
    return acct_address_list,acct_list,wallet_group_name#,password_check_result