class tableMethodTimingStrings(object):
    """docstring for vitterTimingStrings."""

    def __init__(self):
        pass

    def tableSetup(self, seed = 5, nrEvents = 200, minWeight = 1, maxWeight = 10000, base = 10):
        return """
import random
from tableMethod.tableMethod import tableMethod

r = random.Random()
r.seed(%s)

datastruct = tableMethod(%s)

for i in range(%s):
    datastruct.addEvent(int((%s-%s) * (1-r.random()**2))+%s)
""" % (seed, base, nrEvents, maxWeight, minWeight, minWeight)

    def tableExtSetup(self, seed = 5, nrEvents = 200, minWeight = 1, maxWeight = 10000, base = 10, spaceMultiplier = 2):
        return """
import random
from tableMethod.tableMethodExt import tableMethodExt

r = random.Random()
r.seed(%s)

datastruct = tableMethodExt(%s, %s)

for i in range(%s):
    datastruct.addEvent(int((%s-%s) * (1-r.random()**2))+%s)
""" % (seed, base, spaceMultiplier, nrEvents, maxWeight, minWeight, minWeight)

    def tableBuildSetup(self, seed = 5, nrEvents = 200, minWeight = 1, maxWeight = 10000):
        return """
import random
from tableMethod.tableMethod import tableMethod

r = random.Random()
r.seed(%s)

events = list()

for i in range(%s):
    events.append(int((%s-%s) * (1-r.random()**2))+%s)
""" % (seed, nrEvents, maxWeight, minWeight, minWeight)

    def tableExtBuildSetup(self, seed = 5, nrEvents = 200, minWeight = 1, maxWeight = 10000):
        return """
import random
from tableMethod.tableMethodExt import tableMethodExt

r = random.Random()
r.seed(%s)

events = list()

for i in range(%s):
    events.append(int((%s-%s) * (1-r.random()**2))+%s)
""" % (seed, nrEvents, maxWeight, minWeight, minWeight)

    def tableBuild(self, base):
        return """
datastruct = tableMethod(%s)

for e in events:
    datastruct.addEvent(e)
        """ % (base)

    def tableExtBuild(self, base, spaceMultiplier = 2):
        return """
datastruct = tableMethodExt(%s, %s)

for e in events:
    datastruct.addEvent(e)
        """ % (base, spaceMultiplier)

    def tableGenerate(self):
        return """
datastruct.getEvent()
        """

    def tableUpdate(self, nrEvents = 200, minWeight = 1, maxWeight = 10000):
        return """
updateIndex = int(%s*r.random())
newWeight = int(%s*r.random()**2)+%s

datastruct.updateEvent(updateIndex,newWeight)
        """ % (nrEvents,maxWeight,minWeight)
