import System
from HarmonyLib import AccessTools, HarmonyMethod, Traverse
from System.Reflection import Assembly



class 程序集类型:
    def __init__(self, path=".\\BepInEx\\core\\0Harmony.dll", typename="HarmonyLib.Traverse"):
        self.assemly = Assembly.LoadFile(path)
        self.type = self.assemly.GetType(typename)
        self.methods = self.type.GetMethods()
        self.methoddict = {}
        for method in self.methods: self.methoddict[f"{method}"] = method
        
    def FindMethod(self, methodname=""):
        列表 = []
        for key, value in self.methoddict.items():
            if methodname in key: 列表.append(value)
        return 列表

    def PrintMethod(self, methodname=""):
        列表 = self.FindMethod(methodname)
        for i, method in enumerate(列表): print(f"{i}:: {method}")


    def GetType(self, typename=""):
        return self.assemly.GetType(typename)
    
    def PrintType(self, typename=""):
        runtype = self.GetType(typename)
        print(runtype)