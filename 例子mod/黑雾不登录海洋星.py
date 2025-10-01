import System
import UnityEngine

from HarmonyLib import AccessTools, Traverse

from dsptype import SpaceSector, StarData, EnemyDFHiveSystem, VectorLF3, EPlanetType, DFRelayComponent
from dspharmony import HarmonyPatch_Prefix_DefaultAndResult, HarmonyPatch_Postfix_Result
from UnityEngine import Vector3, Time, Quaternion, MeshRenderer, MotionVectorGenerationMode, Material, Color, Component, MeshFilter, Mesh
 
from UnityEngine.Rendering import ShadowCastingMode




def Start():
    # int CreateEnemyFinal( EnemyDFHiveSystem hive, int protoId, int astroId, VectorLF3 lpos, Quaternion lrot)
    类型列表 = [EnemyDFHiveSystem, System.Int32, System.Int32, VectorLF3, Quaternion]
    HarmonyPatch_Prefix_DefaultAndResult(SpaceSector, "CreateEnemyFinal", parastype=类型列表, prefunc=Prefix_Bool, preresult=Prefix_Result) 
    HarmonyPatch_Postfix_Result(DFRelayComponent, "SearchTargetPlaceProcess", postresult=Postfix) # bool SearchTargetPlaceProcess()

def Update():
    pass


def OnGUI():
    pass


# _DefaultAndResult 中 bool函数 参数个数需要和 result函数 一致，这与单独的 _Default 是不同的。
def Prefix_Bool(__instance, hive, protoId, astroId, lpos, lrot, __result):       
    if protoId != 8116: return True # 中继站
    planetData = hive.galaxy.PlanetById(astroId)
    if planetData == None: return True
    if planetData.type == EPlanetType.Ocean: return False
    return True


def Prefix_Result(__instance, hive, protoId, astroId, lpos, lrot, __result):  
    __result = 0
    return __result


def Postfix(__instance, __result):
    planetData = __instance.hive.galaxy.PlanetById(__instance.searchAstroId)
    if planetData != None and planetData.type == EPlanetType.Ocean:
        __instance.ResetSearchStates()
        __result = False
    return __result

