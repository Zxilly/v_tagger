import json

def init():
    try:
        with open("../data/config.json", 'r+') as f:
            config = json.loads(f.read())
    except:
        check = False
        while not check:
            sqladdress = input("SQL地址是：")
            sqlport = input("SQL端口是：")
            sqluser = input("SQL用户是：")
            sqlpassword = input("SQL用户密码是：")
            sqldbname = input("指定给此程序的数据库是:")