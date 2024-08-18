from dsptype import GameMain, UIRoot, LDB


# for techProto in LDB.techs.dataArray:
#     print(f"# {techProto.ID}, # {techProto.name}") 用Name字符串前面会多出字母T


科技列表 = [
    
1001, # 电磁学
1002, # 电磁矩阵

1101, # 高效电浆控制
1102, # 等离子萃取精炼
1120, # 流体储存封装
1201, # 基础制造工艺

1401, # 自动化冶金
1402, # 冶炼提纯

1411, # 钢材冶炼
1412, # 火力发电

1601, # 基础物流系统

1801, # 武器系统

2101, # 机甲核心

2201, # 机械骨骼

2301, # 机舱容量

2501, # 能量回路

2701, # 批量建造

2801, # 能量护盾

2901, # 驱动引擎

4101, # 宇宙探索
]

def 函数():
    for id in 科技列表: GameMain.history.UnlockTech(id)
