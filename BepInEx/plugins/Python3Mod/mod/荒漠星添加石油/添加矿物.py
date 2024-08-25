import System

from dsptype import PlanetAlgorithm, PlanetAlgorithm13, EPlanetType, VeinData, DotNet35Random, EVeinType, PlanetModelingManager

from UnityEngine import Vector3



### 矿组.矿脉
def 取原有矿脉位置列表(planet):
    result = []
    if planet.data.veinCursor == 1: return result

    count = planet.data.veinCursor - 2
    for i in range(count):
        vein = planet.data.veinPool[i+1]
        result.append(vein.pos)
    return result




def 布尔都大于间隔(矿脉位置列表, vec1, radius, 弧长):  #  距离
    弧度 = 弧长 / radius
    cos0 = System.Math.Cos(弧度) #  在0~180度之间，角度越大，cos值越小。cos值更大，说明角度更小
    都大于 = True
    for vec2 in 矿脉位置列表:
        cos2 = Vector3.Dot(vec2.normalized, vec1.normalized)
        if cos2 > cos0:
            都大于 = False
            break

    if 都大于:
        return True
    else:
        return False


def 最小值小于间隔(矿脉位置列表, vec1, radius, 弧长):  #  距离
    弧度 = 弧长 / radius
    cos0 = System.Math.Cos(弧度); #  在0~180度之间，角度越大，cos值越小。cos值更大，说明角度更小
    cos1 = -1.0
    for vec2 in 矿脉位置列表:
        cos2 = Vector3.Dot(vec2.normalized, vec1.normalized)
        if cos2 > cos1: cos1 = cos2

    if cos1 > cos0:
        return True
    else:
        return False


def 置矿组随机位置列表(planet, 矿组间隔, num_left, num_right):
    原有矿脉位置列表 = 取原有矿脉位置列表(planet)
    矿组数 = 取随机数(num_left, num_right)
    新增矿组位置列表 = []
    for i in range(矿组数):
        for j in range(10000):
            位置1 = Vector3(取随机浮点数一值(), 取随机浮点数一值(), 取随机浮点数一值()).normalized * planet.radius
            原有都大于 = 布尔都大于间隔(原有矿脉位置列表, 位置1, planet.radius, 矿组间隔)
            新增都大于 = 布尔都大于间隔(新增矿组位置列表, 位置1, planet.radius, 矿组间隔)
            if 原有都大于 and 新增都大于:
                新增矿组位置列表.append(位置1)
                break
    return 新增矿组位置列表



dotNet35Random = DotNet35Random(System.Guid.NewGuid().GetHashCode()) #  dotNet35Random1.NextDouble() 0~1
def 取随机浮点数():
    return dotNet35Random.NextDouble()
def 取随机浮点数一值():
    return dotNet35Random.NextDouble() * 2.0 - 1.0  # [0, 1] -> [-1, +1] 
def 取随机浮点数大值(right):
    return dotNet35Random.NextDouble() * right - right/2 



随机类 = System.Random(System.Guid.NewGuid().GetHashCode())
def 取随机数(num_left, num_right):
    return 随机类.Next(num_left, num_right)
    

def 取随机范围(矿脉数, 矿脉间隔):
    数量 = System.Math.Sqrt(矿脉数) + 1.0
    right = 数量 * 矿脉间隔
    return right



def 规整矿脉位置(矿脉位置列表, vec2, 矿脉间隔):
    长度平方列表 = [Vector3.Magnitude(vec2 - vec0) for vec0 in 矿脉位置列表]
    index = 长度平方列表.index(min(长度平方列表))
    vec1 = 矿脉位置列表[index]
    direct = (vec2 - vec1).normalized * 矿脉间隔
    return vec1 + direct




def 置矿脉随机位置列表(position, planet, 矿脉间隔, num_left, num_right):
    矿脉数 = 取随机数(num_left, num_right)
    新增矿脉位置列表 = []
    新增矿脉位置列表.append(position)
    right = 取随机范围(矿脉数, 矿脉间隔)
    for i in range(矿脉数):
        for j in range(10000):
            位置1 = position + Vector3(取随机浮点数大值(right), 取随机浮点数大值(right), 取随机浮点数大值(right))
            位置1 = 位置1.normalized * planet.radius
            都大于 = 布尔都大于间隔(新增矿脉位置列表, 位置1, planet.radius, 矿脉间隔)
            if 都大于:
                新增矿脉位置列表.append(规整矿脉位置(新增矿脉位置列表, 位置1, 矿脉间隔))
                break
    return 新增矿脉位置列表



def 取矿组当前索引(planet):
    groupindex = 0
    if planet.data.veinCursor == 1:
        groupindex = 1
    else:
        groupindex = planet.data.veinPool[planet.data.veinCursor - 1].groupIndex + 1
    return groupindex


# System.Threading.Monitor.Enter(obj)
# System.Threading.Monitor.Exit(obj)
def __添加石油(planet, groupindex, vein, vec2, vec2_height):
    veintypeindex = (int)(EVeinType.Oil)
    vein.type = EVeinType.Oil
    vein.groupIndex = groupindex
    vein.amount = 随机类.Next(150000, 350000)
    vein.modelIndex = 随机类.Next(PlanetModelingManager.veinModelIndexs[veintypeindex], PlanetModelingManager.veinModelIndexs[veintypeindex] + PlanetModelingManager.veinModelCounts[veintypeindex])
    vein.productId = PlanetModelingManager.veinProducts[veintypeindex]
    vein.minerCount = 0
    vein.pos = vec2.normalized * vec2_height
    planet.data.EraseVegetableAtPoint(vein.pos)  # 清除位置上的树木等
    planet.data.AddVeinData(vein)


def 添加石油(planet):
    矿组随机位置列表 = 置矿组随机位置列表(planet, 40.0, 7, 15) 
    groupindex = 取矿组当前索引(planet) #,     print(矿组随机位置列表)
    vein = VeinData()
    for vec1 in 矿组随机位置列表:
        vec2 = planet.aux.RawSnap(vec1)  #  吸附到网格，单位向量
        vec2_height = planet.data.QueryHeight(vec2) # 海拔高度
        if vec2_height >= planet.radius: 
            __添加石油(planet, groupindex, vein, vec2, vec2_height)
            groupindex += 1        



def __添加基础矿物(planet, veintype, groupindex, vein, vec1, vec1_height):
    veintypeindex = (int)(veintype)
    vein.type = veintype
    vein.groupIndex = groupindex
    vein.amount = 1000000000  #  表示无限储量；
    # vein.amount = 150  #  矿脉高度与容量有关，越多越高
    vein.modelIndex = 随机类.Next(PlanetModelingManager.veinModelIndexs[veintypeindex], PlanetModelingManager.veinModelIndexs[veintypeindex] + PlanetModelingManager.veinModelCounts[veintypeindex])
    vein.productId = PlanetModelingManager.veinProducts[veintypeindex]
    vein.minerCount = 0
    vein.pos = vec1.normalized * vec1_height
    planet.data.EraseVegetableAtPoint(vein.pos) # 清除位置上的树木等
    planet.data.AddVeinData(vein)



def 添加煤炭(planet):
    矿组随机位置列表 = 置矿组随机位置列表(planet, 50.0, 5, 11)
    groupindex = 取矿组当前索引(planet)
    vein = VeinData()
    for position in 矿组随机位置列表:
        矿组有添加 = False
        矿脉随机位置列表 = 置矿脉随机位置列表(position, planet, 1.9, 5, 27)
        for vec1 in 矿脉随机位置列表:
            vec1_height = planet.data.QueryHeight(vec1)
            if vec1_height >= planet.radius:
                __添加基础矿物(planet, EVeinType.Coal, groupindex, vein, vec1, vec1_height)
                矿组有添加 = True
        if 矿组有添加:
            groupindex +=1




def 添加基础矿物(planet, veintype):
    矿组随机位置列表 = 置矿组随机位置列表(planet, 50.0, 5, 11)
    groupindex = 取矿组当前索引(planet)
    vein = VeinData()
    for position in 矿组随机位置列表:
        矿组有添加 = False
        矿脉随机位置列表 = 置矿脉随机位置列表(position, planet, 2.0, 5, 27)
        for vec1 in 矿脉随机位置列表:
            vec1_height = planet.data.QueryHeight(vec1)
            if vec1_height >= planet.radius:
                __添加基础矿物(planet, veintype, groupindex, vein, vec1, vec1_height)
                矿组有添加 = True
        if 矿组有添加:
            groupindex += 1
