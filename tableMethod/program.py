from tableMethod import tableMethod
from tableMethodExt import tableMethodExt
from random import random

numberOfEvents = 100
numberToGenerate = 1000000
numberOfUpdates = 10000
maxRate = 1000
minRate = 1

events = list()

for i in range(numberOfEvents):
    events.append(int((maxRate-minRate) * random())+1)

totalRate = sum(events)

base = 10
datastruct = tableMethodExt(base)


for e in events:
    datastruct.addEvent(e)

result = [0] * numberOfEvents
weightsInDataStructure = [0] * numberOfEvents



for i in range(numberToGenerate):
    result[datastruct.getEvent()] += 1

#for i in range(len(result)):
#    for j in range(len(datastruct.dataWeights)):
#        weightsInDataStructure[i] += len([n for n in datastruct.eventData[j] if n[0] == i]) * (base**j)

#totalWeight = sum(datastruct.eventWeights)
#percentage = [n * 100 / totalWeight for n in datastruct.eventWeights]
#print "%s, %s, %s" %(datastruct.eventWeights, percentage, weightsInDataStructure)
for i in range(len(result)):
    expectedChance = events[i]/float(totalRate)
    actualChance = result[i]/float(numberToGenerate)
    diff = actualChance - expectedChance
    print "%s:\t%s\t%s%%\tresult:%s%%\t%s instances\tdiff: %s\tperc: %s\t%s" %(i, events[i], format(expectedChance*100,'.10f'), format(actualChance*100,'.10f'), result[i], format(diff,'.10f'), format(diff/expectedChance,'.10f'), "\033[91m fail\033[0m" if diff > 0.1 else "\033[92m pass\033[0m")


result = [0] * numberOfEvents
weightsInDataStructure = [0] * numberOfEvents


for i in range(numberOfUpdates):
    updateIndex = int(numberOfEvents*random())
    newWeight = int(maxRate*random())+minRate
    print "update %s: update index: %s, weight: %s, newWeight: %s, diffence: %s" %(i, updateIndex, events[updateIndex], newWeight, newWeight - events[updateIndex])
    datastruct.updateEvent(updateIndex,newWeight)
    events[updateIndex] = newWeight

print "done with updates, starting generation"

for i in range(numberToGenerate):
    result[datastruct.getEvent()] += 1

#for i in range(len(result)):
#    for j in range(len(datastruct.dataWeights)):
#        weightsInDataStructure[i] += len([n for n in datastruct.eventData[j] if n[0] == i]) * (base**j)

totalWeight = sum(datastruct.eventWeights)
percentage = [n * 100 / totalWeight for n in datastruct.eventWeights]
#print "%s, %s, %s" %(datastruct.eventWeights, percentage, weightsInDataStructure)
for i in range(len(result)):
    expectedChance = events[i]/float(totalRate)
    actualChance = result[i]/float(numberToGenerate)
    diff = actualChance - expectedChance
    print "%s:\t%s\t%s%%\tresult:%s%%\t%s instances\tdiff: %s\tperc: %s\t%s" %(i, events[i], format(expectedChance*100,'.10f'), format(actualChance*100,'.10f'), result[i], format(diff,'.10f'), format(diff/expectedChance,'.10f'), "\033[91m fail\033[0m" if diff > 0.1 else "\033[92m pass\033[0m")
