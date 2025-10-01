import System
from HarmonyLib import AccessTools, Traverse
from System.Reflection import TypeAttributes, MethodAttributes, FieldAttributes, ParameterAttributes
from System.Reflection.Emit import  OpCodes


from dspharmony import 类型列表, 查找原函数, 类型名称检查, 模块, 代理参数处理, 委托函数体, OpCodes_Stind, 修补前置


def HarmonyPatch_Prefix_Parameter(dsptype, targetname:str, parastype=[], preparameter=None):
    原函数 = 查找原函数(dsptype, targetname, parastype)
    类型名称 = 类型名称检查(dsptype, targetname, "Prefix")
    参数名称列表, 参数类型列表 = ["__instance"]+[parameter.Name for parameter in 原函数.GetParameters()], [dsptype]+[parameter.ParameterType for parameter in 原函数.GetParameters()]

    index = 2
    parameterType = 参数类型列表[index]
    参数类型列表[index] = parameterType.MakeByRefType()

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)
    方法名称 = "函数"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, System.Boolean, 参数类型列表) 
    for i, paraname in enumerate(参数名称列表): 
        方法.DefineParameter(i+1, getattr(ParameterAttributes, "None"), paraname)
    IL = 方法.GetILGenerator()


    代理定义列表 = 代理参数处理(参数类型列表)
    代理 = System.Func[*代理定义列表, parameterType]
    字段名称 = "funcParameter"
    字段 = 类型.DefineField(字段名称, 代理, FieldAttributes.Public| FieldAttributes.Static) 

    IL.Emit(OpCodes.Ldarg, index)
    委托函数体(IL, 代理, 字段, 参数类型列表)
    IL.Emit(OpCodes_Stind(parameterType))

    # 默认为真，执行原函数
    IL.Emit(OpCodes.Ldc_I4_1)
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    类型列表.append(classType)
    Traverse.Create(classType).Field(字段名称).SetValue( 代理(preparameter) )
    修补前置(原函数, AccessTools.Method(classType, 方法名称))



# 直接修改
# ref float areaRadius
# areaRadius = 18.0f; # 10.0f -> 18.0f;
# IL.Emit(OpCodes.Ldarg_2)
# IL.Emit(OpCodes.Ldc_R4, 18.0) # IL.Emit(OpCodes.Ldc_R4, 18) # 整数会出错 变成 2.5E-44f
# IL.Emit(OpCodes.Stind_R4)


# "".GetType().ToString()           == "System.String"
# "".GetType().GetType().ToString() == "System.RuntimeType"


# a = 参数类型列表[index]
# # print(dir(a))
# print([a.BaseType, a.MemberType, a.Name, a.ReflectedType, a.FullName])
# # [None, <MemberTypes.TypeInfo: 0x00000020>, 'Single&', None, 'System.Single&']

# print([i, f"{paratype}", paratype]) # 直接print与f{}是不一样的
# # [0, "<class '.NearColliderLogic'>", <class '.NearColliderLogic'>]
# # [1, 'UnityEngine.Vector3', <System.RuntimeType object at 0x0000015215D1A000>]
# # [2, 'System.Single&', <System.RuntimeType object at 0x0000015215D19F80>]
# # [3, 'System.Int32[]&', <System.RuntimeType object at 0x0000015215D19FC0>]


