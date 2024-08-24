from dspharmony import 保存程序集


def Start():
    pass


保存 = True
def Update():
    global 保存
    if 保存: return
    保存程序集()
    保存 = True


def OnGUI():
    pass
