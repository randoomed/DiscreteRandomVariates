class alliasTimingStrings(object):
    """docstring for vitterTimingStrings."""

    def __init__(self):
        pass

    def aliasSetup(self, seed = 5, nrEvents = 200, minWeight = 1, maxWeight = 10000):
        return """
import random
from alliasMethod.alliasMethod import alliasMethod

r = random.Random()
r.seed(%s)
events = list()

for i in range(%s):
    events.append(int((%s-%s) * r.random())+%s)

datastruct = alliasMethod(events)
        """ % (seed, nrEvents, maxWeight, minWeight, minWeight)

    def aliasEnhSetup(self, seed = 5, nrEvents = 200, minWeight = 1, maxWeight = 10000, rebuildFactor = 2):
        return """
import random
from alliasMethod.aliasEnhancement import aliasEnhanced

r = random.Random()
r.seed(%s)
events = list()

for i in range(%s):
    events.append(int((%s-%s) * r.random())+%s)

datastruct = aliasEnhanced(events,%s)
        """ % (seed, nrEvents, maxWeight, minWeight, minWeight, rebuildFactor)

    def aliasEnhDegradeSetup(self, seed = 5, nrEvents = 200, minWeight = 1, maxWeight = 10000, rebuildFactor = 9999999999, updates = 100):
        return """
import random
from alliasMethod.aliasEnhancement import aliasEnhanced

r = random.Random()
r.seed(%s)
events = list()

for i in range(%s):
    events.append(int((%s-%s) * r.random())+%s)

datastruct = aliasEnhanced(events,%s)

for i in range(%s):
    updateIndex = int(%s*r.random())
    newWeight = int(%s*r.random())+%s

    datastruct.updateEvent(updateIndex,newWeight)
        """ % (seed, nrEvents, maxWeight, minWeight, minWeight, rebuildFactor, updates, nrEvents, maxWeight, minWeight)

    def aliasBuildSetup(self, seed = 5, nrEvents = 200, minWeight = 1, maxWeight = 10000):
        return """
import random
from alliasMethod.alliasMethod import alliasMethod

r = random.Random()
r.seed(%s)
events = list()

for i in range(%s):
    events.append(int((%s-%s) * r.random())+%s)
        """ % (seed, nrEvents, maxWeight, minWeight, minWeight)

    def aliasEnhBuildSetup(self, seed = 5, nrEvents = 200, minWeight = 1, maxWeight = 10000):
        return """
import random
from alliasMethod.aliasEnhancement import aliasEnhanced

r = random.Random()
r.seed(%s)
events = list()

for i in range(%s):
    events.append(int((%s-%s) * r.random())+%s)
        """ % (seed, nrEvents, maxWeight, minWeight, minWeight)

    def aliasBuild(self):
        return """
    datastruct = alliasMethod(events)
        """
    def aliasEnhBuild(self, rebuildFactor = 2):
        return """
datastruct = aliasEnhanced(events,%s)
        """ % (rebuildFactor)

    def aliasGenerate(self):
        return """
datastruct.getEvent()
        """
    def aliasEnhUpdate(self, nrEvents = 200, minWeight = 1, maxWeight = 10000):
        return """
updateIndex = int(%s*r.random())
newWeight = int(%s*r.random())+%s

datastruct.updateEvent(updateIndex,newWeight)
        """ % (nrEvents,maxWeight,minWeight)
