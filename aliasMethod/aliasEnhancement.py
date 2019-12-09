from random import random

class aliasEnhanced(object):
    """docstring for aliasEnhanced."""

    def __init__(self, events, rebuildFactor = 2):
        super(aliasEnhanced, self).__init__()

        self.eventList = list()
        self.aliasList = list()
        self.probList = list()
        self.aliasProbList = list()
        self.eventPartList = list()

        self.events = list(events)
        self.numberOfEvents = 0

        self.partSize = 0.0
        self.activeParts = 0
        self.partsAfterBuild = 0

        self.updatesAfterBuild = 0

        self.rebuildFactor = rebuildFactor

        self.__buildAliasStructure()


    def addEvent(self, id, weight):
        #add the event to the internal list of events
        self.events.append(weight)
        self.eventPartList.append(list())
        self.updatesAfterBuild += 1

        #check if we need to rebuild the datastructure
        if self.partsAfterBuild * self.rebuildFactor < self.updatesAfterBuild:
            self.__buildAliasStructure()
        else:
            #add the event to a part
            tmpWeight = weight
            #add full parts untill the weight of the new event is smaller than the part size.
            while tmpWeight > self.partSize:
                self.__addPart(id,-1,1.0,0)

            #add the remaining weight as part
            self.__addPart(id,-1,tmpWeight/self.partSize,0)
            #increment the number of events
            self.numberOfEvents += 1

    def getEvent(self):
        #while we havent selected an event try again
        while True:
            #get one of the parts at random
            index = int(random() * self.activeParts)
            acceptanceRandom = random()
            #check if we select the events
            if self.eventList[index] != -1 and  acceptanceRandom < self.probList[index]:
                return self.eventList[index]
            #else check if we select the alias
            if self.aliasList[index] != -1 and acceptanceRandom < self.aliasProbList[index] + self.probList[index]:
                return self.aliasList[index]

    def updateEvent(self, id, weight):

        oldweight = self.events[id]
        self.events[id] = weight
        self.updatesAfterBuild += 1
        #check if we need to rebuild the datastructure
        if self.partsAfterBuild * self.rebuildFactor < self.updatesAfterBuild:
            self.__buildAliasStructure()
        else:
            #check if it is an increase or decreate of max
            #if the weight decreates find parts containing this event and reduce them
            if weight < oldweight:
                #calculate by how much we have to reduce the event
                reduction = (oldweight - weight)/self.partSize
                #while we should reduce the event further
                while reduction > 0.0:
                    #find a part that contains the event with id id.
                    partId = self.eventPartList[id][-1]
                    #checks if its the event or the alias
                    if self.eventList[partId] == id:
                        #if the reduction is larger than the probability
                        if reduction >= self.probList[partId]:
                            #reduce the reduction
                            reduction -= self.probList[partId]
                            #remove the event from the part
                            self.probList[partId] = 0.0
                            self.eventList[partId] = -1
                            self.eventPartList[id].pop()

                        #if the reduction is smaller than the probability in this part
                        else:
                            #empty the reduction
                            self.probList[partId] -= reduction
                            reduction = 0.0
                    #its the alias
                    else:
                        #if the reduction is larger than the probability
                        if reduction >= self.aliasProbList[partId]:
                            #reduce the reduction
                            reduction -= self.aliasProbList[partId]
                            #remove the event from the part
                            self.aliasProbList[partId] = 0
                            self.aliasList[partId] = -1
                            self.eventPartList[id].pop()

                        #if the reduction is smaller than the probability in this part
                        else:
                            #empty the reduction
                            self.aliasProbList[partId] -= reduction
                            reduction = 0

            #if the weight increase add the extra weight as new parts
            elif weight > oldweight:
                #calculate the amount we have to add
                tmpWeight = weight - oldweight
                #add full parts untill the weight of the new event is smaller than the part size.
                while tmpWeight > self.partSize:
                    self.__addPart(id,-1,1.0,0)
                    tmpWeight -= self.partSize

                #add the remaining weight as part
                self.__addPart(id,-1,tmpWeight/self.partSize,0)


    def __buildAliasStructure(self):
        #determine the number of parts as a float for later calculations
        nrParts = float(len(self.events))
        self.partsAfterBuild = nrParts
        self.numberOfEvents = len(self.events)
        self.eventPartList = [list() for i in self.events]
        self.updatesAfterBuild = 0
        self.activeParts = 0
        self.probList = list()
        self.eventList = list()
        self.aliasProbList = list()
        self.aliasList = list()

        #determine the total weight
        totalWeight = sum(a for a in self.events)
        #depermine the part size (total / n-1)
        self.partSize = totalWeight/nrParts

        eventsWorkList = [float(i) for i in self.events]

        smallEventList = list()
        bigEventList = list()

        for i, e in enumerate(eventsWorkList):
            #if the rate of the event is equal to the part size
            if e == self.partSize:
                #add the event as part without alias
                self.__addPart(i,-1,1.0,0.0)

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
                    self.__addPart(tmpBig, -1, 1.0, 0.0)

                    eventsWorkList[tmpBig] -= self.partSize
                else:
                    smallEventList.append(tmpBig)

            else:
                #take a small events
                smallEvent = smallEventList.pop()
                tmpSmallEventNr = smallEvent
                tmpSmallEventSize = eventsWorkList[smallEvent]

                #fill the rest using a big events
                bigEvent = bigEventList.pop()

                #create the part from the small and big event
                self.__addPart(smallEvent, bigEvent, eventsWorkList[smallEvent]/self.partSize, (self.partSize - eventsWorkList[smallEvent])/self.partSize)

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
                    self.__addPart(bigEvent, -1, 1.0, 0.0)
                #if its larger add it back to the big event list
                else:
                    bigEventList.append(bigEvent)

        #at this point the small event list can only contain events with weight equal to the part size.
        #They where put there because of a rounding error so we add them as event with probability 1
        while(smallEventList):
            leftoverEvent = smallEventList.pop()
            #only add the event if its is larger than a floating point error
            if int(eventsWorkList[leftoverEvent]) > 0:
                self.__addPart(leftoverEvent, -1, 1.0, 0.0)

    #adds a part to the current datastructure
    def __addPart(self, event, alias, prob, aliasprob):
        self.eventList.append(event)
        self.aliasList.append(alias)
        self.probList.append(prob)
        self.aliasProbList.append(aliasprob)
        if(event >= 0):
            self.eventPartList[event].append(self.activeParts)
        if(alias >= 0):
            self.eventPartList[alias].append(self.activeParts)
        self.activeParts+=1

    def printDatastructure(self):
        print "partSize: %s"%(self.partSize)
        print "event\talias\tprob\taliasProb\teventSize\taliasSize"
        for i in range(len(self.eventList)):
            print "%s\t%s\t%s\t%s\t%s\t%s"%(self.eventList[i],self.aliasList[i],self.probList[i],self.aliasProbList[i],int(self.probList[i]*self.partSize),int(self.aliasProbList[i] * self.partSize))

        for i, e in enumerate(self.eventPartList):
            print "event %s in parts: %s" % (i,e)
