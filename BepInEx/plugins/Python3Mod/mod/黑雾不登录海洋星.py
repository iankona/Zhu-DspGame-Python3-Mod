import System
import UnityEngine

from HarmonyLib import AccessTools, Traverse

from dsptype import SpaceSector, StarData, EnemyDFHiveSystem, VectorLF3, EPlanetType, DFRelayComponent
from dspharmony import HarmonyPatchDefaultPrefix, HarmonyPatchDefaultPostfix, HarmonyPatchParameterPrefix, HarmonyPatchParameterPrefixWithReturn, HarmonyPatchParameterPostfixWithReturn, HarmonyPatchDefaultPostfixWithReturn
from UnityEngine import Vector3, Time, Quaternion, MeshRenderer, MotionVectorGenerationMode, Material, Color, Component, MeshFilter, Mesh
 
from UnityEngine.Rendering import ShadowCastingMode




def Start():
    HarmonyPatchParameterPrefixWithReturn(SpaceSector, "CreateEnemyFinal", System.Int32, [EnemyDFHiveSystem, System.Int32, System.Int32, VectorLF3, Quaternion], Prefix_Return, System.Boolean, Prefix_Boolean) 
    HarmonyPatchDefaultPostfixWithReturn(DFRelayComponent, "SearchTargetPlaceProcess", System.Boolean, Postfix)

def Update():
    pass


def OnGUI():
    pass

def Prefix_Return(__instance, hive, protoId, astroId, lpos, lrot):  
    __result = 0
    return __result



def Prefix_Boolean(__instance, hive, protoId, astroId, lpos, lrot):       
    if protoId != 8116: return True # 中继站
    planetData = hive.galaxy.PlanetById(astroId)
    if planetData == None: return True
    if planetData.type == EPlanetType.Ocean: return False
    return True



def Postfix(__instance, __result):
    planetData = __instance.hive.galaxy.PlanetById(__instance.searchAstroId)
    if planetData != None and planetData.type == EPlanetType.Ocean:
        __instance.ResetSearchStates()
        __result = False
    return __result

