import System
from HarmonyLib import AccessTools, Traverse

from dsptype import PlanetAlgorithm, PlanetAlgorithm12, PlanetAlgorithm13, EPlanetType, VeinData
from dspharmony import HarmonyPatchDefaultPostfix, HarmonyPatchDefaultPrefix

from . import 初始星球
from . import 冻土星添加矿物
from . import 荒漠星添加矿物



def Start():

    HarmonyPatchDefaultPrefix(PlanetAlgorithm, "GenerateVeins", Prefix) # 海洋星删除矿物
    HarmonyPatchDefaultPostfix(PlanetAlgorithm, "GenerateVeins", Postfix) # 冻土星添加矿物, 荒漠星添加矿物

    HarmonyPatchDefaultPrefix(PlanetAlgorithm13, "GenerateVeins", Prefixf)  # 潘多拉沼泽, 删除矿物

    HarmonyPatchDefaultPostfix(PlanetAlgorithm12, "GenerateVeins", Postfix12)  # 极寒冻土星添加矿物



def Update():
    pass

def OnGUI():
    pass

# planet.algoId ->  PlanetAlgorithm1~13
def Prefixf(__instance):
    return False


def Prefix(__instance): 
    planet = Traverse.Create(__instance).Field("planet").GetValue()
    初始星球.计算出生点(planet)
    if planet.type == EPlanetType.Ocean: return False
    return True

def Postfix(__instance): 
    planet = Traverse.Create(__instance).Field("planet").GetValue()
    System.Threading.Monitor.Enter(planet)
    if planet.type == EPlanetType.Ice:     冻土星添加矿物.函数(planet)
    if planet.type == EPlanetType.Desert:  荒漠星添加矿物.函数(planet)
    System.Threading.Monitor.Exit(planet)


def Postfix12(__instance): 
    planet = Traverse.Create(__instance).Field("planet").GetValue()
    System.Threading.Monitor.Enter(planet) 
    if planet.type == EPlanetType.Ice:     冻土星添加矿物.函数(planet)
    System.Threading.Monitor.Exit(planet)