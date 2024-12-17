
from dsptype import PlanetAlgorithm, PlanetAlgorithm12, EPlanetType, VeinData

from . import 添加矿物


def 函数(planet):
    if not 所在星系是初始星系(planet): return None
    添加矿物.添加石油(planet), print("冻土星添加石油")
    添加矿物.添加煤炭(planet), print("冻土星添加煤炭")


def 所在星系是初始星系(planet):
    result = False
    for i in range(planet.star.planetCount):
        child_planet = planet.star.planets[i]
        if planet.galaxy.birthPlanetId == child_planet.id:
            result = True
            break
    return result


def 所在星系没有荒漠星(planet):
    result = True
    for i in range(planet.star.planetCount):
        child_planet = planet.star.planets[i]
        if child_planet.type == EPlanetType.Desert:  #  橙晶荒漠
            result = False
            break
    return result


