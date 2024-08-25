
from dsptype import DotNet35Random



def 计算出生点(planet):
    dotNet35Random1 = DotNet35Random(planet.seed)
    dotNet35Random1.Next()
    dotNet35Random1.Next()
    dotNet35Random1.Next()
    dotNet35Random1.Next()
    birthSeed = dotNet35Random1.Next()
    if planet.galaxy.birthPlanetId == planet.id: planet.GenBirthPoints(planet.data, birthSeed)

