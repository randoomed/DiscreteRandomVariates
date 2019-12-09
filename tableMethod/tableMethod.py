from linkedList import linkedList
from random import random
from math import log

class tableMethod(object):
    """
        Implementation of the table method described in the paper 'Generating
        discrete random variables in a computer' by Marsaglia, G.
        this implementation is extended with an update methode.

        Internal data structure array for data, linked list for finding items of event x
    """


    def __init__(self, base = 10):
        super(tableMethod, self).__init__()
        # base value used to split the tables (so we get log_base(maxValue) arrays)
        self.__base = base
        # contains the weights of each event in the datastructure.
        self.eventWeights = list()
        # contains each the partial arrays, array at position x represents values base^x
        self.eventData = list()
        # contains the totalWeight of level i on index i
        self.dataWeights = list()
        # list containing a linked list of all indices of each event at each level
        self.eventIndexDepth = list()
        # contains the sum of all weights
        self.totalWeight = 0
        self.__base = base

    def addEvent(self, weight):
        """
        Add an event to the datastructure.
        :param weight weight of the event.
        """
        self.eventWeights.append(weight)
        #create a list to store a linked list at each depth
        self.eventIndexDepth.append(list())

        #get the index of the event to use as identifier (we know its the last item in the list)
        index = len(self.eventWeights)-1

        remainingWeight = weight

        #catch 0 weight items, as we can't take the log of 0
        if weight != 0:
            #for each level calculate the number of items and add them to the datastructure
            for i in range(0, int(log(weight, self.__base)+1)):
                itemsToAdd = int((remainingWeight % self.__base**(i+1))/self.__base**(i))

                #add the items to the datastructure
                self.__addToEvent(i,index,itemsToAdd)

                #remove the weight we already added to from the remainingWeight
                remainingWeight = remainingWeight - itemsToAdd

            self.totalWeight += weight

    def updateEvent(self, eventNr, newWeight):
        """  update the event at position eventNr to weight newWeight.
        :param eventNr      index of the event to be updated
        :param newWeight    weight of the event after the update.

        """
        remainingWeight = newWeight

        if newWeight != 0:
            #find the highest depth we have to update
            updateDepth = max(int(log(newWeight,self.__base)+1),
                            int(log(self.eventWeights[eventNr],self.__base)+1))
        else:
            updateDepth = int(log(self.eventWeights[eventNr],self.__base)+1)

        # update weights upto the highest depth
        for i in range(updateDepth):
            # get the new weight of the event on this depth
            levelWeight = remainingWeight % self.__base**(i+1)

            #calculate the number of items the event should have at this level
            levelItems = levelWeight / self.__base**i

            #check if we have data at this level
            if(len(self.eventIndexDepth[eventNr]) <= i):
                #if not, the event has 0 items on this depth
                oldLevelItems = 0
            else:
                # get current number of items for the events on this depth
                oldLevelItems = len(self.eventIndexDepth[eventNr][i])

            #update the number of items on this depth
            self.__updateToEvent(i, eventNr, levelItems - oldLevelItems)

            remainingWeight -= levelWeight

        #update the total weight
        self.totalWeight -= self.eventWeights[eventNr]
        self.totalWeight += newWeight

        #update the weight of the event
        self.eventWeights[eventNr] = newWeight

    def __updateToEvent(self, depth, eventIndex, number):
        """
        Increases the number of instances of the event with eventIndex at depth by number.
        :param depth        depth in the datastructure to update.
        :param eventIndex   index of the event we are updating.
        :param number       the number of instances to add to the datastructure. Can be negative.
        """

        #check if we have to add or remove items
        if number > 0:
            self.__addToEvent(depth, eventIndex, number)
        else:
            self.__removeFromEvent(depth, eventIndex, abs(number))
        pass

    def __addToEvent(self, depth, eventIndex, number = 1):
        """ Add number items to the datastructure for event with event index at depth depth.
        This function assumes that the total number of instances at depth after
        adding number instances < __base
        """

        #check if the datastructures exist at this level
        if len(self.dataWeights) <= depth+1:
            #eventData bestaat nog niet op dit niveau, dus moeten we dit toevoegen
            for i in range(len(self.dataWeights),depth+1):
                self.dataWeights.append(0)

        #check if the datastructures exist at this level
        if len(self.eventData) <= depth+1:
            #eventData bestaat nog niet op dit niveau, dus moeten we dit toevoegen
            for i in range(len(self.eventData),depth+1):
                self.eventData.append(list())

        if len(self.eventIndexDepth[eventIndex]) <= depth+1:
            #eventIndexDepth bestaat nog niet op dit niveau, dus moeten we hem toevoegen
            for i in range(len(self.eventIndexDepth[eventIndex]),depth+1):
                self.eventIndexDepth[eventIndex].insert(i,linkedList())

        for j in range(number):
            #add the positions of the newly added item to the position list
            self.eventIndexDepth[eventIndex][depth].append(len(self.eventData[depth]))
            #add a tuple of the event item and listItem in the linked item
            self.eventData[depth].append((eventIndex, self.eventIndexDepth[eventIndex][depth].last))

        # update the total weight of the data at this depth
        self.dataWeights[depth] += number*self.__base**depth

    def __removeFromEvent(self, depth, eventIndex, number = 1):
        """
        Remove number instance(s) of event with eventIndex from the eventData at depth
        """
        for i in range(number):
            #get the index of an item of event with index index
            index = self.eventIndexDepth[eventIndex][depth].first.data

            #if the item is the last item in the list we can just pop it
            if(len(self.eventData[depth])-1 == index):
                #update the linked list
                self.eventIndexDepth[eventIndex][depth].removeListItem(self.eventData[depth][index][1])
                #remove the event from the linked listItem
                self.eventData[depth].pop()

            else:
                #remove the event from the linked listItem
                self.eventIndexDepth[eventIndex][depth].removeListItem(self.eventData[depth][index][1])
                #overwrite this index with the last item from this depth
                self.eventData[depth][index] = self.eventData[depth].pop()
                #update the location of the item in eventIndexDepth
                self.eventData[depth][index][1].data = index

        #update the weight of the data at depth depth
        self.dataWeights[depth] -= number*self.__base**depth

    def getEvent(self):
        """ Gets one of the events from the datastructure, depending on the weights of each event.
        :param  r   random value between 0 and 1
        :returns the chosen event
        """

        #get a random number between 0 and totalWeight
        randomIndex = int(random() * self.totalWeight)

        #check in which index table we have to look
        for i in reversed(range(0,len(self.eventData))):
            # if we find the range that contains our random number
            if (randomIndex < self.dataWeights[i]):
                #grab the right index and return it
                return self.eventData[i][randomIndex/self.__base**i][0]
            #the random number does not fall within the range of the current depth.
            else:
                #remove the current range from the random variable
                randomIndex -= self.dataWeights[i]
