class linkedList(object):
    """
        custom implementation of a linked list
        We need a custom implementation because in the tableMethod class we need to refere
        to individual items in the linked list to quickly remove and update them.
    """


    first = None
    last = None
    lenght = 0

    def __init__(self):
        super(linkedList, self).__init__()

    #define the __len__ function so we can call len() on the linked list
    def __len__(self):
        return self.lenght

    def __repr__(self):
        li = self.first
        string = "linkedList["
        while li != None:
            string += str(li) + ", "
            li = li.next

        string +="]"

        return string

    #add data at the end of the linked list as last item
    def append(self, data):
        newItem = listItem(data, prev=self.last)

        #if the list is empty, set the new listItem as first
        if self.first is None:
            self.first = newItem
        #if this isnt the first item, set the next of the last item to the new list item
        else:
            self.last.next = newItem

        #update the last item in the linked list to be the new listItem.
        self.last = newItem
        self.lenght += 1

    def removeListItem(self, listItem):
        """
        remove a given listItem from the linkedList
        """

        #if its the first item update the first pointer
        if(listItem.prev is None):
            self.first = listItem.next
        #if its the last item opdate the last pointer
        if(listItem.next is None):
            self.last = listItem.prev

        #update the previous and next items of the listItem
        listItem.remove()
        self.lenght -= 1

class listItem(object):
    """Item in the linkedList"""

    data = None
    next = None
    prev = None

    def __init__(self, data, prev = None, next = None):
        super(listItem, self).__init__()
        self.data = data
        self.prev = prev
        self.next = next

    #prints the listItem in a friendly format
    def __repr__(self):
        return "<listItem data: %s>" % (self.data)

    def remove(self):
        """
        update the previous and next list items so this one can be removed.
        """
        if(not(self.prev is None)):
            self.prev.next = self.next
        if(not(self.next is None)):
            self.next.prev = self.prev
