from dsptype import SpaceSector
from dspharmony import HarmonyPatch_Prefix_Default



def Start():
    HarmonyPatch_Prefix_Default(SpaceSector, "SetForNewGame", prefunc=Prefix0) # void SetForNewGame()
    HarmonyPatch_Prefix_Default(SpaceSector, "TryCreateNewHive", prefunc=Prefix1) # EnemyDFHiveSystem TryCreateNewHive(StarData star)


def Update():
    pass


def OnGUI():
    pass



def Prefix0(__instance):
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


