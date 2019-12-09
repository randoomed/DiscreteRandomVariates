from alliasMethod import *
from aliasEnhancement import *
import random
from pprint import pprint

numberOfEvents = 10
numberToGenerate = 1000000
numberOfUpdates = 10000
maxRate = 1000
minRate = 1

r = random.Random()
#r.seed(15)

events = list()

for i in range(numberOfEvents):
    events.append(int((maxRate-minRate) * r.random())+1)

totalRate = sum(events)

datastruct = aliasEnhanced(events)
#datastruct = alliasMethod(events)

result = [0] * numberOfEvents

for i in range(numberToGenerate):
    result[datastruct.getEvent()] += 1
print "done generating \n"

datastruct.printDatastructure()

print "\n\nResult:"
for i in range(len(result)):
    expectedChance = events[i]/float(totalRate)
    actualChance = result[i]/float(numberToGenerate)
    diff = actualChance - expectedChance
    print "%s:\t%s\t%s%%\tresult:%s%%\t%s instances\tdiff: %s\tperc: %s\t%s" %(i, events[i], format(expectedChance*100,'.10f'), format(actualChance*100,'.10f'), result[i], format(diff,'.10f'), format(diff/expectedChance,'.10f'), "\033[91m fail\033[0m" if abs(diff) > 0.0001 else "\033[92m pass\033[0m")


result = [0] * numberOfEvents
weightsInDataStructure = [0] * numberOfEvents

for i in range(numberOfUpdates):
    updateIndex = int(numberOfEvents*r.random())
    newWeight = int(maxRate*r.random())+minRate
    print "update %s: update index: %s, weight: %s, newWeight: %s, diffence: %s" %(i, updateIndex, events[updateIndex], newWeight, newWeight - events[updateIndex])
    datastruct.updateEvent(updateIndex,newWeight)
    events[updateIndex] = newWeight
    #datastruct.printDatastructure()

print "done with updates, starting generation"

for i in range(numberToGenerate):
    result[datastruct.getEvent()] += 1

print "done generating\n"

datastruct.printDatastructure()

totalRate = sum(events)

print "\n\nResult:"
for i in range(len(result)):
    expectedChance = events[i]/float(totalRate)
    actualChance = result[i]/float(numberToGenerate)
    diff = actualChance - expectedChance
    print "%s:\t%s\t%s%%\tresult:%s%%\t%s instances\tdiff: %s\tperc: %s\t%s" %(i, events[i], format(expectedChance*100,'.10f'), format(actualChance*100,'.10f'), result[i], format(diff,'.10f'), format(diff/expectedChance,'.10f'), "\033[91m fail\033[0m" if abs(diff) > 0.0001 else "\033[92m pass\033[0m")
