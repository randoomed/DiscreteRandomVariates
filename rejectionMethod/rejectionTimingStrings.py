class rejectionTimingStrings(object):
    """docstring for rejectionTimingStrings."""

    def __init__(self):
        pass

    def rejectionSetup(self, seed = 5, nrEvents = 200, minWeight = 1, maxWeight = 10000):
        return """
import random
from rejectionMethod.rejectionMethod import rejectionMethod

r = random.Random()
r.seed(%s)
events = list()

for i in range(%s):
    events.append(int((%s-%s) * (1-r.random()**2)) + %s)

datastruct = rejectionMethod(events)
        """ % (seed, nrEvents, maxWeight, minWeight, minWeight)

    def rejectionBuildSetup(self, seed = 5, nrEvents = 200, minWeight = 1, maxWeight = 10000):
        return """
import random
from rejectionMethod.rejectionMethod import rejectionMethod

r = random.Random()
r.seed(%s)
events = list()

for i in range(%s):
    events.append(int((%s-%s) * (1-r.random()**2))+%s)
        """ % (seed, nrEvents, maxWeight, minWeight, minWeight)

    def rejectionBuild(self):
        return """
datastruct = rejectionMethod(events)
        """
    def rejectionGenerate(self):
        return """
datastruct.getEvent()
        """

    def rejectionUpdate(self, nrEvents = 200, minWeight = 1, maxWeight = 10000):
        return """
updateIndex = int(%s*r.random())
newWeight = int(%s*(1-r.random()**2))+%s

datastruct.updateEvent(updateIndex,newWeight)
        """ % (nrEvents,maxWeight,minWeight)
