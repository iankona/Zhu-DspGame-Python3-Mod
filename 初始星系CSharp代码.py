import System
from HarmonyLib import AccessTools, HarmonyMethod, Traverse
from System.Reflection import Assembly, AssemblyName, TypeAttributes, FieldAttributes, MethodAttributes, CallingConventions, PropertyAttributes, ParameterAttributes
from System.Reflection.Emit import AssemblyBuilderAccess, AssemblyBuilder, ModuleBuilder, TypeBuilder, FieldBuilder, MethodBuilder, PropertyBuilder, ConstructorBuilder, ILGenerator, OpCodes, ParameterBuilder, LocalBuilder


from dsptype import PlanetAlgorithm, PlanetAlgorithm12, PlanetAlgorithm13, EPlanetType, VeinData, PlanetData, PlanetRawData
from dspharmony import harmony, 模块, 类型列表, 类型名称列表
from dspassembly import 程序集类型



def HarmonyPatchDefaultPostfix(dsptype, targetname:str, postfixfunc=None):
    原函数 = AccessTools.Method(dsptype, targetname)
    后置函数 = 新建后置函数默认(dsptype, targetname, postfixfunc)
    修补后置(原函数, 后置函数)

assemblyType = 程序集类型(".\\BepInEx\\core\\0Harmony.dll", "HarmonyLib.Traverse")
classType = None
def 新建后置函数默认(dsptype, targetname:str, postfixfunc=None):
    global classType

    类型名称 = f"{dsptype}"[9:-2]
    类型名称 = f"{类型名称}_{targetname}_Postfix"
    if 类型名称 in 类型名称列表: raise ValueError(f"{类型名称}: 命名冲突，请检查是否和其他mod(Python模块)函数修改冲突")

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)


    装箱方法 = 新建装箱方法(类型)
    转换方法 = 新建转换方法(类型)
    初始星系海洋星删除矿物方法 = 新建初始星系海洋星删除矿物方法(类型)



    字段名称 = f"action{targetname}Postfix"
    后置字段 = 类型.DefineField(字段名称, System.Action[dsptype], FieldAttributes.Public| FieldAttributes.Static) 

    方法 = 类型.DefineMethod("函数", MethodAttributes.Public|MethodAttributes.Static, System.Void, [dsptype]) 
    方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance") # ParameterAttributes.None
    IL = 方法.GetILGenerator()
    planet = IL.DeclareLocal(System.Object) 
    IL.Emit(OpCodes.Ldarg_0)
    # creatMethods = assemblyType.FindMethod("Create"), assemblyType.PrintMethod("Create")
    IL.Emit(OpCodes.Call, AccessTools.Method(Traverse, "Create", [System.Object])) # Traverse.Create(__instance);
    IL.Emit(OpCodes.Ldstr, "planet")
    fieldMethods = assemblyType.FindMethod("Field") #, assemblyType.PrintMethod("Field")
    IL.Emit(OpCodes.Callvirt, fieldMethods[0])
    valueMethods = assemblyType.FindMethod("GetValue") #, assemblyType.PrintMethod("GetValue")
    IL.Emit(OpCodes.Callvirt, valueMethods[0])
    IL.Emit(OpCodes.Stloc_0)  # planet = Traverse.Create(__instance).Field("planet").GetValue()

    IL.Emit(OpCodes.Ldloc_0)   
    IL.Emit(OpCodes.Call, AccessTools.Method(System.Threading.Monitor, "Enter", [System.Object])) # System.Threading.Monitor.Enter(value);
    
    IL.Emit(OpCodes.Ldloc_0)
    IL.Emit(OpCodes.Call, 转换方法)
    IL.Emit(OpCodes.Call, 初始星系海洋星删除矿物方法)

    IL.Emit(OpCodes.Ldsfld, 后置字段)
    IL.Emit(OpCodes.Ldloc_0)
    IL.Emit(OpCodes.Callvirt, AccessTools.Method(System.Action[System.Object], "Invoke")) # actionGenerateVeinsPostfix(value);

    IL.Emit(OpCodes.Ldloc_0)   
    IL.Emit(OpCodes.Call, AccessTools.Method(System.Threading.Monitor, "Exit", [System.Object])) # System.Threading.Monitor.Exit(value);

    IL.Emit(OpCodes.Ret)



    classType = 类型.CreateType()
    Traverse.Create(classType).Field(字段名称).SetValue(System.Action[System.Object](postfixfunc))
    类型列表.append(classType)
    类型名称列表.append(类型名称)
    return AccessTools.Method(classType, "函数")




def 新建装箱方法(类型):
    方法名称 = "ToObject"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, System.Object, [PlanetData]) 
    方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "planet") # ParameterAttributes.None
    IL = 方法.GetILGenerator()
    IL.Emit(OpCodes.Ldarg_0)
    # IL.Emit(OpCodes.Box, !!T) ???
    IL.Emit(OpCodes.Ret)
    return 方法


def 新建转换方法(类型):
    方法名称 = "ToPlanetData"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, PlanetData, [System.Object]) 
    方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "obj") # ParameterAttributes.None
    IL = 方法.GetILGenerator()
    IL.Emit(OpCodes.Ldarg_0)
    IL.Emit(OpCodes.Castclass, 方法.ReturnType) # 直接写 IL.Emit(OpCodes.Castclass, PlanetData) 出错
    IL.Emit(OpCodes.Ret)
    return 方法

dspAssemblyType = 程序集类型(".\\DSPGAME_Data\\Managed\\Assembly-CSharp.dll", "VeinData")
def 新建初始星系海洋星删除矿物方法(类型):
    方法名称 = "海洋星删除矿物"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, System.Void, [PlanetData]) 
    方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "planet") # ParameterAttributes.None
    IL = 方法.GetILGenerator()
    IL.Emit(OpCodes.Ldarg_0)
    IL.Emit(OpCodes.Ldfld, AccessTools.Field(PlanetData, "data"))
    IL.Emit(OpCodes.Ldc_I4, 0x400)
    IL.Emit(OpCodes.Newarr, dspAssemblyType.GetType("VeinData")) #, dspAssemblyType.PrintType("VeinData")
    IL.Emit(OpCodes.Stfld, AccessTools.Field(PlanetRawData, "veinPool")) # planet.data.veinPool = new VeinData[1024]

    IL.Emit(OpCodes.Ldarg_0)
    IL.Emit(OpCodes.Ldfld, AccessTools.Field(PlanetData, "data"))
    IL.Emit(OpCodes.Ldc_I4, 0x1)
    IL.Emit(OpCodes.Stfld, AccessTools.Field(PlanetRawData, "veinCursor")) 

    IL.Emit(OpCodes.Ret)
    return 方法



def ToObject(planet):
    return Traverse.Create(classType).Method("ToObject", [planet]).GetValue()

def ToPlanetData(obj):
    return Traverse.Create(classType).Method("ToPlanetData", [obj]).GetValue()



def 修补后置(原函数, 后置函数):
    patchProcessor = harmony.CreateProcessor(原函数)
    patchProcessor.AddPostfix(HarmonyMethod(后置函数))
    patchProcessor.Patch()



