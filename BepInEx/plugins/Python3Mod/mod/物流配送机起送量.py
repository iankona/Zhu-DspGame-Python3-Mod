import System
import UnityEngine

from HarmonyLib import AccessTools, Traverse

from dsptype import PlanetFactory, VeinData, GameMain, MinerComponent, PowerSystem, PrefabDesc, GameHistoryData, DispenserComponent
from dspharmony import HarmonyPatchDefaultPostfix, HarmonyPatchParameterPrefix, HarmonyPatchParameterPrefixWithReturn
from UnityEngine import Vector3, Time, Quaternion, MeshRenderer, MotionVectorGenerationMode, Material, Color, Component, MeshFilter, Mesh
 
from UnityEngine.Rendering import ShadowCastingMode



def Start():
    HarmonyPatchDefaultPostfix(GameHistoryData, "UnlockTechFunction", Postfix)
    HarmonyPatchParameterPrefixWithReturn(DispenserComponent, "PickFromStoragePrecalc", System.Int32, [System.Int32, System.Int32], Prefix_Return, System.Boolean, Prefix_Boolean)


def Update():
    pass

def OnGUI():
    pass



carries = 100
def Postfix(__instance): # 解锁全球送
    if __instance.logisticCourierCarries < carries: __instance.logisticCourierCarries = carries # 运载量
    __instance.dispenserDeliveryMaxAngle = 180 # 配送角度


def Prefix_Return(__instance, itemId, needCnt, __result):
    if needCnt < carries: __result = 0
    return __result

def Prefix_Boolean(__instance, itemId, needCnt, __result):
    if needCnt < carries: return False
    return True

