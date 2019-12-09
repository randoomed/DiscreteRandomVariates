from random import random
from pprint import pprint
from MVNMethod import MVNMethod
from MVNMethodTolerance import MVNMethodTolerance
from MVNMethod import vRange
from MVNMethod import vEvent

numberOfEvents = 2000
numberOfUpdates = 200000
numberOfPulls = 1000000
maxWeight = 99999

events = list()

for i in range(numberOfEvents):
    events.append(vEvent(int(maxWeight*random())+1))

print events

m = MVNMethodTolerance(events,0.4,12)
#m = MVNMethod(events)

print m.totalWeight
m.showForest()

for i in range(numberOfUpdates):

    updateIndex = int(numberOfEvents*random())
    newWeight = int(maxWeight*random())+1
    print "update %s: update index: %s, weight: %s, newWeight: %s" %(i, updateIndex, events[updateIndex].weight, newWeight)

    m.updateEvent(events[updateIndex],newWeight)
    #print "weight after update: %s" % (events[updateIndex].weight)
    #m.showForest()

print m.totalWeight
m.showForest()

eventCounts = dict();
for e in events:
    eventCounts[e.weight] = 0

b = None

for i in range(numberOfPulls):
    eventCounts[m.getEvent().weight] += 1


pprint(eventCounts)

#weight chance occurance totalchance
weights = eventCounts.keys()
weights.sort()
for i in range(len(eventCounts)):
    expectedChance = weights[i]*100/float(m.totalWeight)
    resultChance = eventCounts[weights[i]] * 100 / float(numberOfPulls)
    diff = abs(expectedChance - resultChance)
    print "%s\t%s\t%s\t%s\tdiff: %s\tperc: %s\t%s" % (weights[i], format(expectedChance,'.10f'), eventCounts[weights[i]], format(resultChance,'.10f'), format(diff,'.10f'), format(diff/expectedChance,'.10f'), "\033[91m fail\033[0m" if diff > 0.1 else "\033[92m pass\033[0m")
