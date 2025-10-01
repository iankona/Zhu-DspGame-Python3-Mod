import System
from HarmonyLib import AccessTools, Traverse

from dsptype import PlanetAlgorithm, PlanetAlgorithm12, PlanetAlgorithm13, EPlanetType, VeinData
from dspharmony import HarmonyPatch_Prefix_Default, HarmonyPatch_Postfix_Default

from . import 初始星球
from . import 冻土星添加矿物
from . import 荒漠星添加矿物



def Start():

    HarmonyPatch_Prefix_Default(PlanetAlgorithm, "GenerateVeins", prefunc=Prefix) # 海洋星删除矿物 # void GenerateVeins()
    HarmonyPatch_Postfix_Default(PlanetAlgorithm, "GenerateVeins", postfunc=Postfix) # 冻土星添加矿物, 荒漠星添加矿物 # void GenerateVeins()

    HarmonyPatch_Postfix_Default(PlanetAlgorithm12, "GenerateVeins", postfunc=Postfix12)  # 极寒冻土星添加矿物 # void GenerateVeins()
    
    HarmonyPatch_Prefix_Default(PlanetAlgorithm13, "GenerateVeins", prefunc=Prefix00)  # 潘多拉沼泽, 删除矿物 # void GenerateVeins()




def Update():
    pass

def OnGUI():
    pass




def Prefix(__instance): 
    planet = Traverse.Create(__instance).Field("planet").GetValue()
    初始星球.计算出生点(planet)
    if planet.type == EPlanetType.Ocean: return False
    return True

def Postfix(__instance): 
    planet = Traverse.Create(__instance).Field("planet").GetValue()
    System.Threading.Monitor.Enter(planet)
    if planet.type == EPlanetType.Ice: 冻土星添加矿物.函数(planet)
    if planet.type == EPlanetType.Desert: 荒漠星添加矿物.函数(planet)
    System.Threading.Monitor.Exit(planet)


def Postfix12(__instance): 
    planet = Traverse.Create(__instance).Field("planet").GetValue()
    System.Threading.Monitor.Enter(planet) 
    if planet.type == EPlanetType.Ice: 冻土星添加矿物.函数(planet)
    System.Threading.Monitor.Exit(planet)


# planet.algoId ->  PlanetAlgorithm1~13
def Prefix00(__instance):
    return False