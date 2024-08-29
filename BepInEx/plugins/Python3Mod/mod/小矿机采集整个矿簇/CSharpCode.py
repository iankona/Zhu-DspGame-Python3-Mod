import System
from HarmonyLib import AccessTools, HarmonyMethod, Traverse
from System.Reflection import Assembly, AssemblyName, TypeAttributes, FieldAttributes, MethodAttributes, CallingConventions, PropertyAttributes, ParameterAttributes
from System.Reflection.Emit import AssemblyBuilderAccess, AssemblyBuilder, ModuleBuilder, TypeBuilder, FieldBuilder, MethodBuilder, PropertyBuilder, ConstructorBuilder, ILGenerator, OpCodes, ParameterBuilder, LocalBuilder


from dsptype import PlanetAlgorithm, PlanetAlgorithm12, PlanetAlgorithm13, EPlanetType, VeinData, PlanetData, PlanetRawData
from dspharmony import harmony, 模块, 类型列表, 类型名称列表, 修补前置, Ref类型, Ref_Result_返回值类型读取, Ref_Result_返回值类型赋值
from dspassembly import 程序集类型



def HarmonyPatchDefaultPrefixWithRefParameter(dsptype, targetname:str, returntype=None, funcreturn=None):
    原函数 = AccessTools.Method(dsptype, targetname)
    函数 = 新建前置函数默认WithRefParameter(dsptype, targetname, returntype, funcreturn)
    修补前置(原函数, 函数)


# assemblyType = 程序集类型(".\\BepInEx\\core\\0Harmony.dll", "HarmonyLib.Traverse")
def 新建前置函数默认WithRefParameter(dsptype, targetname:str, returntype=None, funcreturn=None):
    类型名称 = f"{dsptype}"[9:-2]
    类型名称 = f"{类型名称}_{targetname}_Prefix"
    if 类型名称 in 类型名称列表: raise ValueError(f"{类型名称}: 命名冲突，请检查是否和其他mod(Python模块)函数修改冲突")

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)
    
    代理 = System.Func[dsptype, returntype, returntype]
    字段 = 类型.DefineField("funcRef", 代理, FieldAttributes.Public| FieldAttributes.Static) 

    方法 = 类型.DefineMethod("函数", MethodAttributes.Public|MethodAttributes.Static, System.Boolean, [dsptype, Ref类型(returntype)]) 

    方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance") # ParameterAttributes.None
    方法.DefineParameter(2, getattr(ParameterAttributes, "None"), "vcnt") # ParameterAttributes.None

    IL = 方法.GetILGenerator()

    num = IL.DeclareLocal(returntype) 

    IL.Emit(OpCodes.Ldarg_1)
    Ref_Result_返回值类型读取(IL, returntype)
    IL.Emit(OpCodes.Stloc_0)

    IL.Emit(OpCodes.Ldarg_1)
    IL.Emit(OpCodes.Ldsfld, 字段)
    IL.Emit(OpCodes.Ldarg_0)
    IL.Emit(OpCodes.Ldloc_0)
    IL.Emit(OpCodes.Callvirt, AccessTools.Method(代理, "Invoke")) # actionGenerateVeinsPostfix(value);
    Ref_Result_返回值类型赋值(IL, returntype)

    IL.Emit(OpCodes.Ldc_I4_1)
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    Traverse.Create(classType).Field("funcRef").SetValue( 代理(funcreturn) )
    类型列表.append(classType)
    类型名称列表.append(类型名称)
    return AccessTools.Method(classType, "函数")










