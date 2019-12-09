from random import random
from pprint import pprint

class alliasMethod(object):
    """docstring for alliasMethod."""

    def __init__(self, events):
        super(alliasMethod, self).__init__()

        self.eventList = list()
        self.aliasList = list()
        self.probList = list()

        self.events = list(events)

        self.partSize = 0.0

        self.__buildAliasStructure()

    def addEvent(self, weight):
        pass


    def getEvent(self):
        #pick an item from the probList at randomIndex
        index = int(random() * len(self.eventList))
        acceptanceRandom = random()
        #if random > prob return the time from the aliasList
        if acceptanceRandom < self.probList[index]:
            return self.eventList[index]
        #otherwise return the item from the eventList
        return self.aliasList[index]

    def __buildAliasStructure(self):
        #determine the number of parts as a float for later calculations
        nrParts = float(len(self.events))
        #determine the total weight
        totalWeight = sum(a for a in self.events)
        #depermine the part size (total / n-1)
        self.partSize = totalWeight/nrParts

        eventsWorkList = [float(i) for i in self.events]

        smallEventList = list()
        bigEventList = list()

        for i, e in enumerate(eventsWorkList):
            if e == self.partSize:
                self.__addPart(i,i,1.0)

            elif e > self.partSize:
                bigEventList.append(i)
            else:
                smallEventList.append(i)

        #while we have big events left in our list:
        while(bigEventList):
            #if there are no small events
            if(not smallEventList):
                tmpBig = bigEventList.pop()

                #while the big event is larger than the part size:
                #add a part of only this event and reduce the size of tmp big in the work list
                while eventsWorkList[tmpBig] >= self.partSize:
                    self.__addPart(tmpBig,tmpBig,1.0)

                    eventsWorkList[tmpBig] -= self.partSize
                else:
                    smallEventList.append(tmpBig)

            else:
                #take a small events
                smallEvent = smallEventList.pop()

                #fill the rest using a big events
                bigEvent = bigEventList.pop()

                #create the part from the small and big event
                self.__addPart(smallEvent,bigEvent,eventsWorkList[smallEvent]/self.partSize)

                #remove the probability use to fill the part form the event
                eventsWorkList[bigEvent] -= self.partSize - eventsWorkList[smallEvent]

                #update the size of the small event
                eventsWorkList[smallEvent] = 0

                #check if the big event becomes a small events
                #if so, add it to the small event list
                if eventsWorkList[bigEvent] < self.partSize:
                    smallEventList.append(bigEvent)
                #if its equal to the part size, add it as part
                elif eventsWorkList[bigEvent] == self.partSize:
                    self.__addPart(bigEvent,bigEvent,1.0)
                #if its larger add it back to the big event list
                else:
                    bigEventList.append(bigEvent)

        #at this point the small event list can only contain events with weight equal to the part size.
        #They where put there because of a rounding error so we add them as event with probability 1
        while(smallEventList):
            leftoverEvent = smallEventList.pop()
            #add the event if its larger than a floating point error
            if int(eventsWorkList[leftoverEvent]) > 0:
                self.__addPart(leftoverEvent,leftoverEvent,1.0)

    #adds a part to the current datastructure
    def __addPart(self, event, allias, prob):
        self.eventList.append(event)
        self.aliasList.append(allias)
        self.probList.append(prob)

    def printDatastructure(self):
        print "partSize: %s"%(self.partSize)
        print "event\talias\tprob\teventSize\taliasSize"
        for i in range(len(self.eventList)):
            print "%s\t%s\t%s\t%s\t%s"%(self.eventList[i],self.aliasList[i],self.probList[i],int(self.probList[i]*self.partSize),int((1-self.probList[i]) * self.partSize))
