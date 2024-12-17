
from dsptype import PlayerAction_Inspect, GameMain
from dspharmony import HarmonyPatch_Prefix_Result
from UnityEngine import Mathf


def Start():
    HarmonyPatch_Prefix_Result(PlayerAction_Inspect, "GetObjectSelectDistance", preresult=PreResult) # float GetObjectSelectDistance(EObjectType objType, int objid)

def Update():
    pass

def OnGUI():
    pass


def PreResult(__instance, objType, objid, __result):
    if objid == 0 or __instance.player.factory == None: __result = range

    range = 600
    if GameMain.localPlanet != None and GameMain.localPlanet.realRadius > 201:
        range = int(GameMain.localPlanet.realRadius * Mathf.PI)
    __result = range # 默认35f
    return __result
