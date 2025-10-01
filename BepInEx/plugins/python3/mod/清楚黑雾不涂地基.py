
from dsptype import BuildTool_Reform
from dspharmony import HarmonyPatch_Prefix_Result



def Start():
    HarmonyPatch_Prefix_Result(BuildTool_Reform, "RemoveBasePit", preresult=PrefixResult) # bool RemoveBasePit(int removeBasePitRuinId)

def Update():
    pass

def OnGUI():
    pass



def PrefixResult(__instance, removeBasePitRuinId, __result):
    __instance.factory.enemySystem.RemoveBasePit(removeBasePitRuinId)
    return True  # __result = true;