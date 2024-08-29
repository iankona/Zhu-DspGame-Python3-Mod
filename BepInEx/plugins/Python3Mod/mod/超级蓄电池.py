import System

from dsptype import PowerSystem
from dspharmony import HarmonyPatchDefaultPostfixWithReturn


def Start():
    HarmonyPatchDefaultPostfixWithReturn(PowerSystem, "NewAccumulatorComponent", System.Int32, Postfix)



def Update():
    pass

def OnGUI():
    pass



MW = 1000020
GJ = 1000000000
def Postfix(__instance, __result):
    MW_PerTick = MW / 60
    __instance.accPool[__result].inputEnergyPerTick = 315 * MW_PerTick    # 原始，25000 -> 1.5MW
    __instance.accPool[__result].outputEnergyPerTick = 315 * MW_PerTick   # 原始，37500 -> 2.25MW
    __instance.accPool[__result].maxEnergy = 10.26 * GJ                   # 原始，540000000 -> 540MJ
    return __result

