import os 
import sys
import importlib


import clr
from System import Console #, ConsoleColor
class NetConsole:
    def __init__(self):
        pass
    def write(self, message): # 1个print(), 调用2次write()
        if message == '\n': return
        # Console.ForegroundColor = ConsoleColor.DarkGreen # 不起作用
        Console.WriteLine('[Py   :   Console]  ' + message)
        # Console.ResetColor()
        
    def flush(self):
        pass
sys.stdout = NetConsole() # 接管print()输出 # print("你好，世界！")
sys.stderr = NetConsole()



moddir = ".\\BepInEx\\plugins\\Python3Mod\\mod"



def 名称处理():
    名称列表 = []
    basenamelist = os.listdir(moddir)
    for basename in basenamelist:
        if '__pycache__' in basename: continue
        charlist = basename.split('.')
        if charlist[0] == '': continue
        if charlist[0] not in 名称列表: 名称列表.append(charlist[0])
    return 名称列表


模块列表 = []


def 模块加载():
    global 模块列表
    模块列表 = []
    for name in 名称处理(): # 名称列表 = 名称处理() # Console.WriteLine(模块列表) # [Info   :   Console] ['zhuqtools', '星球内添加建造模式右键快速移动', '测试']
        # module = importlib.import_module(name)
        # 模块列表.append(module)
        try:
            module = importlib.import_module(name)
            模块列表.append(module)
            print(f"Python模块：'{name}' 加载成功 ... ")
        except Exception as e:
            print(f"Python模块：'{name}' 加载出错 ??? ??? ")
            print(e)


def 模块重载():
    global 模块列表
    模块列表 = []
    for name in 名称处理(): # 名称列表 = 名称处理() # Console.WriteLine(模块列表) # [Info   :   Console] ['zhuqtools', '星球内添加建造模式右键快速移动', '测试']
        try:
            module = importlib.reload(name)
            模块列表.append(module)
            print(f"Python模块：'{name}' 重载成功 ... ")
        except Exception as e:
            print(f"Python模块：'{name}' 重载出错 ??? ??? ")
            print(e)


模块加载()


def Start():
    for module in 模块列表: 
        try:
            module.Start()
        except Exception as e:
            print(e)



def Update():
    for module in 模块列表: 
        try:
            module.Update()
        except Exception as e:
            print(e)


def OnGUI():
    for module in 模块列表: 
        try:
            module.OnGUI()
        except Exception as e:
            print(e)



# basenamelist = os.listdir(moddir)
# Console.WriteLine(basenamelist) # [Info   :   Console] ['zhuqtools', '__pycache__', '星球内添加建造模式右键快速移动', '测试.py']