from dsptype import GameMain, LDB
from HarmonyLib import Traverse




建筑列表 = [

2001, # 低速传送带
2002, # 高速传送带
2003, # 极速传送带

2205, # 太阳能板

2105, # 轨道采集器

]

def 函数():
    if GameMain.localPlanet == None: return 
    if GameMain.localPlanet.factory == None: return 
    按帧直接建造()


count = 0
def 按帧直接建造(): 
    global count
    prebuildPool = GameMain.localPlanet.factory.prebuildPool
    for i, prebuild in enumerate(prebuildPool):
        if i % 30 != count: continue
        if prebuild.protoId in 建筑列表: Build(prebuild.id)
    count += 1
    if count > 60: count = 0


def 直接建造(): 
    prebuildPool = GameMain.localPlanet.factory.prebuildPool
    for i, prebuild in enumerate(prebuildPool):
        if prebuild.protoId in 建筑列表: Build(prebuild.id)


# def 修改小飞机任务状态():
#     prebuildPool = GameMain.localPlanet.factory.prebuildPool
#     drones = GameMain.localPlanet.factory.constructionSystem.drones
#     for drone in drones.buffer:
#         if drone.targetObjectId < 0:
#             prebuildId = -drone.targetObjectId
#             protoId = prebuildPool[prebuildId].protoId
#             if protoId in 建筑列表: 
#                 drone.stage = 3
#                 Build(prebuildId)
#                 drone.targetObjectId = 0



def Build(prebuildId):
    constructionSystem = GameMain.localPlanet.factory.constructionSystem
    if constructionSystem.factory.planet.factoryLoaded:
      constructionSystem.factory.BuildFinally(constructionSystem.player, prebuildId)
    else:
      constructionSystem.factory.BuildFinally(constructionSystem.player, prebuildId, False, False)





# file = open(r".\BepInEx\plugins\Python3Mod\mod\立即建造\物品属性.txt", mode = "a")
# for item in LDB.items.dataArray: 
#     row = item.name + "，"
#     for name in dir(item):
#         try:
#             char =  f"{name}：{getattr(item, name)}，"
#         except:
#             char =  f"{name}：NoneOrFunc，"
#         row += char
#     row += "\n"
#     file.write(row)
# file.close()


# for item in LDB.items.dataArray: 
#     if item.CanBuild: print(f"# {item.ID}, # {item.name}")


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