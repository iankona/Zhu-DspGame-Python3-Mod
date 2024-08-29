import System
import UnityEngine

from HarmonyLib import AccessTools, Traverse

from dsptype import SpaceSector, StarData
from dspharmony import HarmonyPatchDefaultPrefix, HarmonyPatchDefaultPostfix, HarmonyPatchParameterPrefix
from UnityEngine import Vector3, Time, Quaternion, MeshRenderer, MotionVectorGenerationMode, Material, Color, Component, MeshFilter, Mesh
 
from UnityEngine.Rendering import ShadowCastingMode




def Start():
    HarmonyPatchDefaultPrefix(SpaceSector, "SetForNewGame", Prefix) 
    HarmonyPatchParameterPrefix(SpaceSector, "TryCreateNewHive", [StarData], Prefix1)

def Update():
    pass


def OnGUI():
    pass



def Prefix(__instance):
    birthstarindex = __instance.galaxy.birthStarId - 1
    for i in range(__instance.galaxy.starCount):
        star = __instance.galaxy.stars[i]
        if i == birthstarindex:
            star.initialHiveCount = 0
            break
    return True



def Prefix1(__instance, star):
    if star == None: return True
    birthstarindex = __instance.galaxy.birthStarId - 1
    if star.index == birthstarindex: return False
    return True


