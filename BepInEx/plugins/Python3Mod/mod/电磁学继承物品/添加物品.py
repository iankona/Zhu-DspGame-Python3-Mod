from dsptype import GameMain, UIRoot, LDB



# for itemProto in LDB.items.dataArray:
#     print(f"# [{itemProto.ID}, 0], # {itemProto.name}")



物品列表 = [

[1006, 400], # 煤矿

]

def 函数():
    for id, count in 物品列表: GameMain.mainPlayer.TryAddItemToPackage(id, count, 0, False)
