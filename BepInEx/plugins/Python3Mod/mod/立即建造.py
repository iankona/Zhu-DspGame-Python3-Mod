import System
from HarmonyLib import AccessTools, Traverse

from dsptype import GameMain, ConstructionSystem, DroneComponent
from dspharmony import HarmonyPatchDefaultPrefix, HarmonyPatchDefaultPrefixAndPostfix



def Start():
    HarmonyPatchDefaultPrefix(ConstructionSystem, "ExecuteBuildTasks", Prefix)

def Update():
    pass

def OnGUI():
    pass



建筑列表 = [

2001, # 低速传送带
2002, # 高速传送带
2003, # 极速传送带

2205, # 太阳能板

2105, # 轨道采集器

]


def Prefix(__instance):
    prebuildPool = __instance.factory.prebuildPool
    for i in range(1,  __instance.drones.cursor):
        drone = __instance.drones.buffer[i] # 没有 ref 关键字 C#底层直接返回副本，在python中，我找不到替代方法。
        if drone.targetObjectId < 0:
            prebuildId = -drone.targetObjectId
            protoId = prebuildPool[prebuildId].protoId
            if protoId in 建筑列表: 
                drone.stage = 3
                __instance.drones.buffer[i] = drone # 搞不定， ref DroneComponent drone = ref __instance.drones.buffer[index1]; 
    return True

# 1131, # 地基
# 2001, # 低速传送带
# 2002, # 高速传送带
# 2003, # 极速传送带
# 2011, # 低速分拣器
# 2012, # 高速分拣器
# 2013, # 极速分拣器
# 2014, # 集装分拣器
# 2020, # 四向分流器
# 2040, # 自动集装机
# 2030, # 流速器
# 2313, # 喷涂机
# 2107, # 物流配送器
# 2101, # 小型储物仓
# 2102, # 大型储物仓
# 2106, # 储液罐
# 2303, # 制造台 Mk.I
# 2304, # 制造台 Mk.II
# 2305, # 制造台 Mk.III
# 2318, # 制造台 Mk.IV
# 2201, # 电力感应塔
# 2202, # 无线输电塔
# 2212, # 卫星配电站
# 2203, # 风力涡轮机
# 2204, # 火力发电厂
# 2211, # 微型聚变发电站
# 2213, # 地热发电站
# 2301, # 采矿机
# 2316, # 大型采矿机
# 2306, # 抽水站
# 2302, # 电弧熔炉
# 2315, # 位面熔炉
# 2319, # 熔炉 Mk.III
# 2307, # 原油萃取站
# 2308, # 原油精炼厂
# 2309, # 化工厂
# 2317, # 化工厂 Mk.II
# 2314, # 分馏塔
# 2205, # 太阳能板
# 2206, # 蓄电器
# 2207, # 蓄电器（满）
# 2311, # 电磁轨道弹射器
# 2208, # 射线接收站
# 2312, # 垂直发射井
# 2209, # 能量枢纽
# 2310, # 微型粒子对撞机
# 2210, # 人造恒星
# 2103, # 物流运输站
# 2104, # 星际物流运输站
# 2105, # 轨道采集器
# 2901, # 矩阵研究站
# 2902, # 矩阵研究站 Mk.II
# 3001, # 高斯机枪塔
# 3002, # 高频激光塔
# 3003, # 聚爆加农炮
# 3004, # 磁化电浆炮
# 3005, # 导弹防御塔
# 3006, # 干扰塔
# 3007, # 信标
# 3008, # 护盾发生器
# 3009, # 战场分析基站
# 3010, # 地面电浆炮