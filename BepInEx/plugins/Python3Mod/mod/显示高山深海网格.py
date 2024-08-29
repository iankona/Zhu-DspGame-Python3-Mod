import System
from HarmonyLib import AccessTools, Traverse

from dsptype import UIBuildingGrid, GameMain
from dspharmony import HarmonyPatchDefaultPostfix

from UnityEngine import Color

def Start():
    HarmonyPatchDefaultPostfix(UIBuildingGrid, "Update", Postfix)

def Update():
    pass

def OnGUI():
    pass



def Postfix(__instance):
    修改网格高低(__instance)
    修改网格颜色(__instance)



def 修改网格高低(__instance):
    material = Traverse.Create(__instance).Field("material").GetValue()
    if GameMain.mainPlayer != None:
        material.SetFloat("_ZMin", -8.0)  # Mountains
        material.SetFloat("_ZMax",  8.0)  # Oceans


修改颜色 = False
def 修改网格颜色(__instance):
    global 修改颜色
    if 修改颜色: return
    __instance.buildColor = Color(0.07, 0.43, 0.17, 1.0) # 会闪烁？？？
    # __instance.buildColor.r = 0.17 # 修改不起作用
    # __instance.buildColor.g = 0.25 
    # __instance.buildColor.b = 0.17
    # __instance.buildColor.a = 1.0
    修改颜色 = True