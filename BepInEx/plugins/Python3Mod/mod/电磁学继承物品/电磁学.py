from dsptype import GameMain, UIRoot, LDB, UITechNode
from dspharmony import HarmonyPatchDefaultPostfix

from . import 解锁科技
from . import 添加物品
from . import 解锁传送带坡度限制


def 修补函数():
    HarmonyPatchDefaultPostfix(UITechNode, "DoStartTech", Postfix)


def Postfix(__instance):
    if __instance.techProto.ID == 1001: # 电磁学
        解锁科技.函数()
        添加物品.函数()
        解锁传送带坡度限制.函数()
