import System
import UnityEngine

from HarmonyLib import AccessTools, Traverse

from dsptype import PlanetFactory, VeinData, GameMain, MinerComponent
from dspharmony import HarmonyPatchDefaultPostfix, HarmonyPatchParameterPrefix
from UnityEngine import Vector3, Time, Quaternion, MeshRenderer, MotionVectorGenerationMode, Material, Color, Component, MeshFilter, Mesh
 
from UnityEngine.Rendering import ShadowCastingMode



def Start():
    HarmonyPatchParameterPrefix(MinerComponent, "InternalUpdate", [ PlanetFactory, System.Array[VeinData], System.Single, System.Single, System.Single, System.Array[System.Int32] ], Prefix)


def Update():
    pass

def OnGUI():
    pass


def Prefix(__instance, factory, veinPool, power, miningRate, miningSpeed, productRegister):
    System.Threading.Monitor.Enter(veinPool) 
    都小于 = True
    for i in range(__instance.veinCount):
        vein = veinPool[__instance.veins[i]]
        if vein.amount > 101:
            都小于 = False
            __instance.currentVeinIndex = i
            break
    System.Threading.Monitor.Exit(veinPool)
    if 都小于 and GameMain.history.techStates[3606].curLevel < 157:
        return False # 禁用原函数
    else:
        return True  # 原函数正常运行

        







