from random import random
from pprint import pprint

class rejectionMethod(object):
    """docstring for alliasMethod."""

    def __init__(self, events):
        super(rejectionMethod, self).__init__()

        self.maxWeight = float(max(events))
        self.events = list(events)

    def addEvent(self, weight):
        self.totalWeight += weight
        self.events.append(weight)

        if weight > self.maxWeight:
            self.maxWeight = float(weight)

    def getEvent(self):
        while True:
            #pick a random index
            index = int(random() * len(self.events))

            #check if we accept the index
            acceptanceRandom = random()
            if acceptanceRandom < self.events[index] / self.maxWeight:
                return index

    def updateEvent(self, eventNr, newWeight):
        #update the weight
        self.events[eventNr] = newWeight

        #check if we need to increase the maximum weight
        if newWeight > self.maxWeight:
            self.maxWeight = newWeight
