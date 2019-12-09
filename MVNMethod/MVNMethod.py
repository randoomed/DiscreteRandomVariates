from math import log
from random import random

class MVNMethod(object):
    """Implementation of the MVN algorithm by Matias et al. in the paper Dynamic generation of discrete
random variates."""


    def __init__(self, events):

        self.totalWeight = 0;
        self.levelTable = list()
        self.rootNodeTable = list()
        self.levelWeights = list()
        #initialize the datastucture and fill it with events
        ranges = events
        level = 1
        #add level 0 items
        self.levelTable.append(dict())
        self.rootNodeTable.append(list())
        self.levelWeights.append(0)
        #initialize the totalWeight
        for r in ranges:
            self.totalWeight += r.weight

        #build the datastructure from the bottom up
        while len(ranges) > 0:
            tmpRanges = dict()
            self.levelTable.append(dict())
            self.rootNodeTable.append(list())
            self.levelWeights.append(0)
            #loop over all ranges and add them to the correct ranges on the next level
            for r in ranges:
                #calculate the range we have to put this range into.
                rangeIndex = int(log(r.weight,2))

                #if the range exists add r to the range
                if rangeIndex in tmpRanges:
                    tmpRanges[rangeIndex].add(r)

                #otherwise make a new range with r as its only member
                else:
                    tmpRanges[rangeIndex] = vRange(rangeIndex,level,r)

                #add the weight of the event to the range
                tmpRanges[rangeIndex].weight += r.weight

                #update the parent of r
                r.parent = tmpRanges[rangeIndex]
            #clear the ranges list so we can fill it with the next levelItems
            ranges = list()
            #go over all new ranges
            for r in tmpRanges.values():
                self.levelTable[level][r.index] = r
                #put next level ranges with 2 or more members in ranges for the next pass
                if len(r) > 1:
                    ranges.append(r)
                #add root ranges to the rootNode table
                else:
                    self.rootNodeTable[level].append(r)
                    self.levelWeights[level] += r.weight

            #increment the level we are currently on
            level += 1

    def addEvent(self, event):
        #determine the index of the range we want to add our event to
        rangeIndex = int(log(event.weight,2))

        self.totalWeight += event.weight

        #check if there exists a level 1 range with index rangeIndex
        if rangeIndex in self.levelTable[1]:
            parentRange = self.levelTable[1][rangeIndex]
            parentRange.add(event)
        #the range does not exist yet, so we create it
        else:
            parentRange = vRange(rangeIndex,1,event)
            self.levelTable[1][rangeIndex] = parentRange

        #update the range
        self.updateEvent(parentRange, parentRange.weight)

    def updateEvent(self, event, newWeight):
        oldWeight = event.weight

        #update the total weight of the datastructure if the event is from level 0
        if(event.level == 0):
            self.totalWeight += newWeight
            self.totalWeight -= oldWeight

        #the event is a root node
        if event.parent == None:
            #if the node is empty
            if len(event) == 0:
                #remove the node from the level List
                del self.levelTable[event.level][event.index]
                #remove the rootNode
                self.rootNodeTable[event.level].remove(event)
                #update the weight of the level
                self.levelWeights[event.level] -= oldWeight

            #if the node was a root node but has more children than a root node should have
            elif len(event) >= 2:
                #remove the weight of the level
                self.levelWeights[event.level] -= oldWeight
                #remove the node from the level List
                self.rootNodeTable[event.level].remove(event)
                #update the weight of the node
                event.weight = newWeight
                #find a parent for the root node
                newEventIndex = int(log(event.weight,2))

                #if the level table does not have a level for our new parent yet add the new level
                if event.level+1 == len(self.levelTable):
                    self.levelTable.append(dict())
                    self.rootNodeTable.append(list())
                    self.levelWeights.append(0)

                #check if the parent exists, if not create it
                if newEventIndex in self.levelTable[event.level+1]:
                    newParent = self.levelTable[event.level+1][newEventIndex]
                    #add the node to its new the parent
                    newParent.add(event)
                    event.parent = newParent
                    #update the new parent
                    self.updateEvent(event.parent, event.parent.weight + newWeight)

                #there does not exist a parent yet
                else:
                    #create a new parent
                    r = vRange(newEventIndex,event.level+1,event)

                    event.parent = r
                    #set the weight of the new ranges
                    r.weight = newWeight
                    #add the new root range to the level table
                    self.levelTable[event.level+1][newEventIndex] = r
                    self.rootNodeTable[event.level+1].append(r)
                    self.levelWeights[event.level+1] += r.weight

            #if the root node remains a root node.
            else:
                #update the weight of the level
                self.levelWeights[event.level] += newWeight
                self.levelWeights[event.level] -= oldWeight
                #update the weight of the event
                event.weight = newWeight

        #if the node is not a root node
        else:
            #this is a range with only one child and not from level 0, it should be changed to root node.
            if len(event) <= 1 and event.level != 0:
                #remove the range from its parent
                event.parent.remove(event)
                #update the parent
                self.updateEvent(event.parent, event.parent.weight - oldWeight)
                #remove the parent
                event.parent = None
                #update the weight of the events
                event.weight = newWeight
                #add the range to the level table
                self.levelTable[event.level][event.index] = event
                #add the node as root node
                self.rootNodeTable[event.level].append(event)
                #update the weight of the level
                self.levelWeights[event.level] += newWeight

            #the node shouldnt be a rootnode and has the correct parent
            elif 2 ** (event.parent.index) <= newWeight and 2 ** (event.parent.index+1) > newWeight:
                #update the weight of the event
                event.weight = newWeight
                #we have the correct parent, so we just have to update that one and its parent
                self.updateEvent(event.parent, event.parent.weight - oldWeight + newWeight )

            #we have the wrong parent, so we have to find the correct one
            else:
                #remove the event from the wrong parrent
                event.parent.remove(event)
                #update the old parent
                self.updateEvent(event.parent, event.parent.weight - oldWeight)
                #update the events weights
                event.weight = newWeight

                #find the correct parrent
                newEventIndex = int(log(event.weight,2))

                #if the level table does not have a level for our new parent yet add the new level
                if event.level+1 == len(self.levelTable):
                    self.levelTable.append(dict())
                    self.rootNodeTable.append(list())
                    self.levelWeights.append(0)

                #check if there exist a range for the weight of event
                if newEventIndex in self.levelTable[event.level+1]:
                    newParent = self.levelTable[event.level+1][newEventIndex]

                    newParent.add(event)
                    event.parent = newParent
                    #update the new parent ranges
                    self.updateEvent(newParent, newParent.weight + newWeight)
                #if there does not exist a parent for the current events weight
                else:
                    #create a new parent
                    r = vRange(newEventIndex,event.level+1,event)

                    event.parent = r
                    #set the weight of the new ranges
                    r.weight = newWeight
                    #add the new root range to the level table
                    self.levelTable[event.level+1][newEventIndex] = r
                    self.rootNodeTable[event.level+1].append(r)
                    self.levelWeights[event.level+1] += r.weight

    def getEvent(self):
        #get our random starting weight
        selectedWeight = random() * self.totalWeight

        #find the level  our starting weight is on
        weightCounter = 0
        for i in range(len(self.rootNodeTable)):
            weightCounter += self.levelWeights[i]
            if weightCounter > selectedWeight:
                break

        selectedWeight = random() * self.levelWeights[i]
        weightCounter = 0;
        #find a root node from this range base on weight
        for j in range(len(self.rootNodeTable[i])):
            weightCounter += self.rootNodeTable[i][j].weight
            if weightCounter > selectedWeight:
                break

        #go down this root node and return the found events
        return self._getChildFromRange(self.rootNodeTable[i][j])


    def _getChildFromRange(self, eventRange):
        #we found an event, so return it and end the recursion
        if(eventRange.level == 0):
            return eventRange

        selectedChild = None
        #use the maximum possible value of an item in this range ax maxWeight for the rejection method
        maxWeight = 2 ** (eventRange.index+1)
        while(True):
            #get random number
            ri = random() * len(eventRange.children)
            #select a variate at random
            selectedChild = eventRange.children[int(ri)]
            #check if we reject the items
            if (ri - int(ri)) < selectedChild.weight/float(maxWeight):
                #if we accept it break out of the loop
                break

        #call this function on the selected child
        return self._getChildFromRange(selectedChild)

    #print the forest formed by the trees of all rootnodes
    def showForest(self):
        levels = range(len(self.rootNodeTable))
        levels.reverse()

        #print all root nodes
        for i in levels:
            print "level: %s" %(i)
            for j in range(len(self.rootNodeTable[i])):
                print self.rootNodeTable[i][j]

        #for each level, show the tree of each rootNode
        for i in levels:
            print "level: %s" %(i)
            for j in range(len(self.rootNodeTable[i])):
                print self.rootNodeTable[i][j]
                self.showTree(self.rootNodeTable[i][j])

    #print the tree of a root node
    def showTree(self,eventRange, indent=1):
        indentStr = "\t" * indent
        if indent == 4:
            return

        for e in eventRange.children:
            print "%s%s" % (indentStr,e)
            if(e.level != 0):
                self.showTree(e,indent+1)


class vRange(object):
    """docstring for vRange."""
    def __init__(self, rangeIndex, level, range):
        self.index = rangeIndex
        self.level = level
        self.children = list()
        self.eventIndex = dict()
        self.weight = 0
        self.lenght = 0
        self.parent = None

        if range is not None:
            self.add(range)

    def add(self, event):
        self.children.append(event)
        self.eventIndex[event] = self.lenght
        self.lenght += 1

    def remove(self, event):
        #get the index of the event we want to remove
        rEventIndex = self.eventIndex[event]

        #if the item we want to remove isnt the last item
        if len(self.children) != rEventIndex - 1:
            #replace the item we want to remove by the last one in the list
            self.children[rEventIndex] = self.children[len(self.children)-1]
            #update the index of the item we want to remove
            self.eventIndex[self.children[rEventIndex]] = rEventIndex

        #remove the last item from children
        self.children.pop()
        #update the lenght of the range
        self.lenght -= 1

    def __len__(self):
        return self.lenght

    def __repr__(self):
        return "<vRange weight: %s, index: %s, level %s, len: %s>" % (self.weight, self.index, self.level, self.lenght)

class vEvent(vRange):
    def __init__(self, weight):
        super(vEvent,self).__init__(0,0,None)
        self.weight = weight

    def __repr__(self):
        return "<vEvent weight: %s>" % (self.weight)
