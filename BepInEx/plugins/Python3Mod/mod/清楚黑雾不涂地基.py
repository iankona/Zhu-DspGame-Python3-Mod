import System
from HarmonyLib import AccessTools, Traverse

from dsptype import BuildTool_Reform
from dspharmony import HarmonyPatchParameterPrefixWithReturn

from UnityEngine import Color

def Start():
    HarmonyPatchParameterPrefixWithReturn(BuildTool_Reform, "RemoveBasePit", System.Boolean, [System.Int32], PrefixReturn, System.Boolean, PrefixBoolean)


def Update():
    pass

def OnGUI():
    pass



def PrefixReturn(__instance, removeBasePitRuinId):
    __instance.factory.enemySystem.RemoveBasePit(removeBasePitRuinId)
    return True  # __result = true;

def PrefixBoolean(__instance, removeBasePitRuinId):
    return False # 拦截原函数
