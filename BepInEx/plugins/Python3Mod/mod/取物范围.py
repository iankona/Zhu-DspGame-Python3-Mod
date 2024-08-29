import System
from HarmonyLib import AccessTools, Traverse

from dsptype import PlayerAction_Inspect, GameMain
from dspharmony import HarmonyPatchDefaultPostfixWithReturn
from UnityEngine import Color, Mathf


def Start():
    HarmonyPatchDefaultPostfixWithReturn(PlayerAction_Inspect, "GetObjectSelectDistance", System.Single, Postfix)

def Update():
    pass

def OnGUI():
    pass




def Postfix(__instance, __result):
    range = 600
    if GameMain.localPlanet != None and GameMain.localPlanet.realRadius > 201:
        range = int(GameMain.localPlanet.realRadius * Mathf.PI)
    __result = range # 默认35f
    return __result
