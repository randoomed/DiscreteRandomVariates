from linkedList import linkedList
from random import random
from math import log

class tableMethodExt(object):
    I"""Implementation of the extended table method. """


    def __init__(self, base = 10, spaceMultiplier = 2.0):
        super(tableMethodExt, self).__init__()
        # base value used to split the tables (so we get log_base(maxValue) arrays)
        self.__base = base
        #determine the maxmimum number of items per level
        self.__maxItemsPerLevel = base * spaceMultiplier
        # contains the weights of each event in the datastructure.
        self.eventWeights = list()
        # contains the weight of each event on each level
        self.eventLevelItems = list()
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
        add an event to the datastructure.
        :param weight weight of the event.
        """
        self.eventWeights.append(weight)
        #create a list to store a linked list at each depth
        self.eventIndexDepth.append(list())
        #create a list to store the weight at each level
        self.eventLevelItems.append(list())

        #get the index of the event to use as identifier (we know its the last item in the list)
        index = len(self.eventWeights)-1

        remainingWeight = weight

        #catch 0 weight items, as we can't take the log of 0
        if weight != 0:
            #for each level calculate the number of items and add them to the datastructure
            for i in range(0, int(log(weight, self.__base)+1)):
                itemsToAdd = (remainingWeight % self.__base**(i+1))/self.__base**(i)

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
        difference = newWeight - self.eventWeights[eventNr]
        if difference != 0:
            #find the highest depth we have to update
            updateDepth = int(log(abs(difference),self.__base))

            #the difference is positive so we start at the bottom
            if difference > 0:
                for i in range(updateDepth+1):
                    # get the new weight of the event on this depth
                    levelWeight = difference % self.__base**(i+1)

                    #claculate the number of items the event should have at this level
                    levelItems = int(levelWeight / self.__base**i)

                    #update the number of items on this depth
                    self.__addToEvent(i, eventNr, levelItems)

                    difference -= levelItems * self.__base**i

            #the diffence is negative so we start at the top
            else:
                difference = abs(difference)
                for i in range(updateDepth, -1, -1):
                    # get the new weight of the event on this depth
                    levelWeight = difference % self.__base**(i+1)

                    #claculate the number of items the event should have at this level
                    levelItems = int(levelWeight / self.__base**i)

                    #update the number of items on this depth
                    self.__removeFromEvent(i, eventNr, levelItems)

                    difference -= levelItems * self.__base**i

            #update the total weight
            self.totalWeight -= self.eventWeights[eventNr]
            self.totalWeight += newWeight

            #update the weight of the event
            self.eventWeights[eventNr] = newWeight

    def __updateToEvent(self, depth, eventIndex, number):
        """
        increases the number of instances of the event with eventIndex at depth by number.
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
        """ add number items to the datastructure for event with event index at depth depth.
        this function assumes that the total number of instances at depth after
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

        if len(self.eventLevelItems[eventIndex]) <= depth+1:
            #eventLevelItems bestaat nog niet op dit niveau, dus moeten we hem toevoegen
            for i in range(len(self.eventLevelItems[eventIndex]),depth+1):
                self.eventLevelItems[eventIndex].insert(i,0)

        numberToAdd = number

        #print "add %s items to event %s on depth %s, %s on this level"%(number,eventIndex,depth,self.eventLevelItems[eventIndex][depth])
        #check if we overlow the maximum number of items at this level
        if self.eventLevelItems[eventIndex][depth] + number >= self.__maxItemsPerLevel:
            #add one item to one level higher
            self.__addToEvent(depth+1, eventIndex)
            #remove __base items from the number as we just added that much value to the level +1
            numberToAdd -= self.__base

        #if we still have to add items, add them
        if numberToAdd > 0:
            self.eventLevelItems[eventIndex][depth] += numberToAdd

            for j in range(numberToAdd):
                #add the positions of the newly added item to the position list
                self.eventIndexDepth[eventIndex][depth].append(len(self.eventData[depth]))
                #add a tuple of the event item and listItem in the linked item
                self.eventData[depth].append((eventIndex, self.eventIndexDepth[eventIndex][depth].last))

            # update the total weight of the data at this depth
            self.dataWeights[depth] += numberToAdd*self.__base**depth

        #we dont have to do anything
        elif numberToAdd == 0:
            pass

        #the number we need to add is negative so call remove
        else:
            self.__removeFromEvent(depth, eventIndex, abs(numberToAdd))

    def __removeFromEvent(self, depth, eventIndex, number = 1):
        """
        remove number instance(s) of event with eventIndex from the eventData at depth
        """
        #make sure eventLevelItems exists at this level
        if len(self.eventLevelItems[eventIndex]) <= depth+1:
            #eventLevelItems bestaat nog niet op dit niveau, dus moeten we hem toevoegen
            for i in range(len(self.eventLevelItems[eventIndex]),depth+1):
                self.eventLevelItems[eventIndex].insert(i,0)

        #check if the datastructures exist at this level
        if len(self.dataWeights) <= depth+1:
            #eventData bestaat nog niet op dit niveau, dus moeten we dit toevoegen
            for i in range(len(self.dataWeights),depth+1):
                self.dataWeights.append(0)

        ItemsToRemove = number;

        #print "remove %s items from event: %s on depth %s, %s on this level"%(number,eventIndex,depth,self.eventLevelItems[eventIndex][depth])
        #check if we have enough items at this level
        if self.eventLevelItems[eventIndex][depth] < number:
            #if not, check if we have any items above it
            if self.__hasItemsAtLevel(eventIndex, depth+1):
                #get __base items from the level above
                self.__removeFromEvent(depth+1, eventIndex)
                #update the items to be remove
                ItemsToRemove -= self.__base
            #there are no items in the levels above us, so the levels below have more than __base items
            else:
                pushedItems = self.__pushItemsUp(eventIndex, depth-1, ItemsToRemove - self.eventLevelItems[eventIndex][depth])
                ItemsToRemove -= pushedItems

        #if we actually have to remove items
        if ItemsToRemove > 0:

            #if self.eventLevelItems[eventIndex][depth] < ItemsToRemove:
            #    print "aaaah we verwijderen te veel"

            #print "start removing %s items from %s which has %s items" %(ItemsToRemove,eventIndex,self.eventLevelItems[eventIndex][depth])
            #update eventLevelItems
            self.eventLevelItems[eventIndex][depth] -= ItemsToRemove

            #print "eventIndexDepth len: %s"%(len(self.eventIndexDepth[eventIndex][depth]))
            #print "eventIndexDepth[%s][%s]: %s" % (eventIndex,depth,self.eventIndexDepth[eventIndex][depth])
            #actually remove the items from the current level
            for i in range(ItemsToRemove):
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
            self.dataWeights[depth] -= ItemsToRemove*self.__base**depth

        #we dont have to do anything
        elif ItemsToRemove == 0:
            pass
        #items we have to remove is negative so call add
        else:
            self.__addToEvent(depth, eventIndex, abs(ItemsToRemove))

    def __hasItemsAtLevel(self, eventIndex, depth):
        """ returns true if the event with eventIndex has items at or above this level """

        #if we never added the eventLevelItems on this level return false
        if len(self.eventLevelItems[eventIndex]) < depth+1:
            #print "hasItemsAtLevel index: %s, level: %s, items: None"%(eventIndex,depth)
            return False
        #we have items on this level, so return true
        elif self.eventLevelItems[eventIndex][depth] > 0:
            #print "hasItemsAtLevel index: %s, level: %s, items: %s"%(eventIndex,depth,self.eventLevelItems[eventIndex][depth])
            return True
        #we have nothing on this level, so check the one above
        else:
            #print "hasItemsAtLevel index: %s, level: %s, items: %s"%(eventIndex,depth,self.eventLevelItems[eventIndex][depth])
            return self.__hasItemsAtLevel(eventIndex,depth+1)

    def __pushItemsUp(self, eventIndex, depth, number):
        """ Try to push number items up from lower levels """
        #print "push on depth %s for %s items, required: %s, %s items on this depth" %(depth,number,number * self.__base,self.eventLevelItems[eventIndex][depth])
        pushedItems = 0
        #calculate the number of extra items we need to push number items up
        requiredItems = number * self.__base - self.eventLevelItems[eventIndex][depth]
        #check if we need extra from lower levels
        if requiredItems > 0 and depth > 0:
            #if so try to push those items up
            pushedItems = self.__pushItemsUp(eventIndex, depth-1, requiredItems)

        #remove the items we are pushing up
        toBeRemoved = number*self.__base - pushedItems
        pushableItems = number

        #TEMP check if things go right
        if toBeRemoved > self.eventLevelItems[eventIndex][depth]:
            #print "to little items pushed up required %s, pushed %s"%(requiredItems, pushedItems)
            #for i, e in enumerate(self.eventLevelItems[eventIndex]):
            #    print "depth: %s, events: %s"%(i,e)

            pushableItems = int((self.eventLevelItems[eventIndex][depth] + pushedItems)/self.__base)

            toBeRemoved = (pushableItems * self.__base) - pushedItems

        #remove the items we push
        self.__removeFromEvent(depth, eventIndex, toBeRemoved)

        return pushableItems

    def getEvent(self):
        """ gets one of the events from the datastructure, depending on the weights of each event.
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
