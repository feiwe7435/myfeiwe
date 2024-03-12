
# 密码错误异常类
class PasswordError(Exception):
    def __init__(self, message):
        self.message = message

# 钱包序号不存在异常类
class WalletNumError(Exception):
    def __init__(self, message):
        self.message = message