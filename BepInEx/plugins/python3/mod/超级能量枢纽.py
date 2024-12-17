
from dsptype import PowerSystem
from dspharmony import HarmonyPatch_Postfix_Result


def Start():
    HarmonyPatch_Postfix_Result(PowerSystem, "NewExchangerComponent", postresult=Postfix) # int NewExchangerComponent(int entityId, PrefabDesc desc)



def Update():
    pass

def OnGUI():
    pass




MW = 1000020
GJ = 1000000000
def Postfix(__instance, entityId, desc, __result):
    MW_PerTick = MW / 60
    __instance.excPool[__result].energyPerTick = 315 * MW_PerTick
    __instance.excPool[__result].maxPoolEnergy = 10.26*GJ
    return __result

# // 小太阳功率75MW,黑棒储能7.20GJ
# // 枢纽功率 45MW


