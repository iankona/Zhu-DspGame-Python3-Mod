from dsptype import GameMain, UIRoot, LDB
from . import 解锁科技
from . import 添加物品
from . import 解锁传送带坡度限制



继承物品 = False

def 函数():
    global 继承物品
    if 继承物品: return
    if GameMain.history == None: return
    if GameMain.mainPlayer == None: return
    if GameMain.history.currentTech != 1001: return # 电磁学
    解锁科技.函数()
    添加物品.函数()
    解锁传送带坡度限制.函数()
    继承物品 = True