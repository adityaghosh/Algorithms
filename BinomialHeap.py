class Node:
    def __init__(self, data, leftChild = None, rightSibling = None, parent=None, degree = 0):
        self.data = data
        self.parent = parent
        self.rightSibling = rightSibling
        self.leftChild = leftChild
        self.degree = degree
    
    # Pretty printing Node
    def __str__(self):
        noneStr = "/"
        sparent = ""
        sdata = ""
        sleftChild = ""
        srightSibling = ""
        if self.parent == None:
            sparent = noneStr
        if self.leftChild == None:
            sleftChild = noneStr
        if self.rightSibling == None:
            srightSibling = noneStr
        if self.parent != None:
            sparent = str(self.parent.data)
        if self.leftChild != None:
            sleftChild = str(self.leftChild.data)
        if self.rightSibling != None:
            srightSibling = str(self.rightSibling.data)
        sdata = str(self.data)
        s = "|P: "+sparent+" D: "+sdata+" LC: "+sleftChild+" RS: "+srightSibling+"|"        
        return s
        
        
class BinomialHeap:
    def __init__(self, root = None):
        self.root = root
        self.min = root
        
    def updateMin(self):
        curr = self.root
        if self.min == None and curr != None:
            self.min = curr
        while curr != None:
            if curr.data < self.min.data:
                self.min = curr
            curr = curr.rightSibling
            
def MakeBinomialHeap():
    b = BinomialHeap()
    return b

def BinomialHeapMinimum(h):
    return h.min

def BinomialLink(y, z):
    y.parent = z
    y.rightSibling = z.leftChild
    z.leftChild = y
    z.degree = z.degree + 1

def BinomialHeapMerge(h1, h2):
    heap1root = h1.root
    heap2root = h2.root
    head = None
    if heap1root == None or heap2root == None:
        if heap1root == None and heap2root == None:
            return None
        elif heap1root == None:
            return heap2root
        else:
            return heap1root
    if heap1root.degree < heap2root.degree:
        head = heap1root
    else:
        head = heap2root
        heap2root = heap1root
        heap1root = head
    curr = head
    while heap1root != None and heap2root != None:
        if heap1root.degree > heap2root.degree:
            next = heap2root
            heap2root = heap2root.rightSibling
        else:
            next = heap1root
            heap1root = heap1root.rightSibling
        curr.rightSibling = next
        curr = curr.rightSibling
    while heap1root != None:
        next = heap1root
        heap1root = heap1root.rightSibling
        curr.rightSibling = next
        curr = curr.rightSibling
    while heap2root != None:
        next = heap2root
        heap2root = heap2root.rightSibling
        curr.rightSibling = next
        curr = curr.rightSibling
    return head
    
def BinomialHeapUnion(h1, h2):
    h = MakeBinomialHeap()
    h.root = BinomialHeapMerge(h1, h2)
    if h.root == None:
        return h
    prevx = None
    x = h.root
    nextx = x.rightSibling
    while nextx != None:
        if (x.degree != nextx.degree) or (nextx.rightSibling != None and nextx.rightSibling.degree == x.degree):
            prevx = x
            x = nextx
        else:
            if x.data <= nextx.data:
                x.rightSibling = nextx.rightSibling
                BinomialLink(nextx, x)
            else:
                if prevx == None:
                    h.root = nextx
                else:
                    prevx.rightSibling = nextx
                BinomialLink(x,nextx)
                x = nextx
        nextx = x.rightSibling
    h.updateMin()
    return h

def BinomialHeapInsert(h, x):
    h2 = MakeBinomialHeap()
    h2.root = Node(x)
    h2.min = h2.root
    h = BinomialHeapUnion(h, h2)
    h.updateMin()
    return h
    
def BinomialHeapExtractMin(h):
    x = h.min
    # Update the root list to skip the min link
    prev = None
    curr = h.root
    while curr != x:
        prev = curr
        curr = curr.rightSibling
    # Min is the not first root.
    if prev != None:
        prev.rightSibling = curr.rightSibling
    else:
        h.root = curr.rightSibling
        curr.rightSibling = None
    h2 = MakeBinomialHeap()
    y = x.leftChild
    # Reversing the list(to have list sorted by degree) and making parent of all to None. 
    h2.root = ListReverse(y)
    htemp = BinomialHeapUnion(h, h2)
    htemp.updateMin()
    # Updating the input heap.
    h.root = htemp.root
    h.min = htemp.min
    return x


def BinomialHeapDecreaseKey(b, x, newKey):
    if newKey > x.data:
        return None
    x.data = newKey
    y = x
    z = y.parent
    while z != None and y.data < z.data:
        #ExchangeNodes(y, z)   
        temp = y.data
        y.data = z.data
        z.data = temp
        y = z
        z = y.parent
    return b
            
def BinomialHeapDelete(b, x):
    b = BinomialHeapDecreaseKey(b, x, float("-inf"))
    if b != None:
        b.updateMin()
        inf = BinomialHeapExtractMin(b)
        PrintBinomialHeap(b)
        return b
    else:
        return None


# Utility Functions

# Given a start node to a list returns the start node of the reversed list. 
def ListReverse(y):
    ynext = None
    yprev = None
    while y != None:
        y.parent = None
        ynext = y.rightSibling
        y.rightSibling = yprev
        yprev = y
        y = ynext
    return yprev

# Given two nodes y and z exchanges all information
def ExchangeNodes(y, z):
    # Create a new Temp Node with values of y
    temp = Node(y.data)
    temp.parent = y.parent
    temp.rightSibling = y.rightSibling
    temp.leftChild = y.leftChild
    # swap all values
    y.parent = z.parent
    y.data = z.data
    y.rightSibling = z.rightSibling
    y.leftChild = z.leftChild
    z.parent = temp.parent
    z.data = temp.data
    z.rightSibling = temp.rightSibling
    z.leftChild = temp.leftChild

 
# If a node with the given data exists in the heap return the node otherwise return None.
def FindNode(h, data):
    root = h.root
    while root != None:
        if root.data == data:
            return root
        next = root.leftChild
        while next != None:
            curr = next
            level = curr
            while level != None:
                if level.data == data:
                    return level
                level = level.rightSibling
            next = curr.leftChild 
        root = root.rightSibling
    return None

  

# Pretty prints the binomial Heap.
def PrintBinomialHeap(h):
    root = h.root
    while root != None:
        print ""
        print "Tree with degree",root.degree
        print root
        level = []
        if root.leftChild != None:
            print " / "
            print "\/"
            next = root
            level = level + createLevel(next)
            while len(level) > 0:
                level = printLevel(level)
                print ""
                if len(level) > 0:
                    print " / "
                    print "\/"
        root = root.rightSibling
        print ""

# Given a Node this function creates a list of Nodes which are children of this node
def createLevel(n):
    level = []
    next = n.leftChild
    while next != None:
        level.append(next)
        next = next.rightSibling
    return level
    
# Prints all node in this level and returns a list of nodes in the next level
def printLevel(level):
    nextLevel = []
    for i in range(0,len(level)):
        if level[i].rightSibling != None:
            print level[i],"-->",
        else:
            print level[i],
        nextLevel = nextLevel + createLevel(level[i])
    return nextLevel

def run():
    binomialHeapList = []
    inp = 100
    while inp != 0:
        print "1. Create a New heap(Make-Heap)."
        print "2. Insert a value to Heap."
        print "3. Extract Min from a Heap."
        print "4. Delete value from Heap."
        print "5. Decrease Key."
        print "6. Merge two heaps."
        print "7. Print a binomial Heap"
        print "0. Exit"
        inp = int(raw_input())
        if inp == 0:
            break
        elif inp == 1:
            b = MakeBinomialHeap()
            binomialHeapList.append(b)
            print "Binomial Heap created at index ", len(binomialHeapList) - 1
        elif inp == 2:
            print "Enter an index to select a heap, one of: ", range(0,len(binomialHeapList))
            index = int(raw_input())
            print "Enter Value to insert"
            value = int(raw_input())
            binomialHeapList[index] = BinomialHeapInsert(binomialHeapList[index], value)
            print "Value: ", value," inserted to binomial heap at index", index
        elif inp == 3:
            print "Enter an index to select a heap, one of: ", range(0,len(binomialHeapList))
            index = int(raw_input())
            min = BinomialHeapExtractMin(binomialHeapList[index])
            print "Minimum node in the heap at index: ", index," is ", min
        elif inp == 4:
            print "Enter an index to select a heap, one of: ", range(0,len(binomialHeapList))
            index = int(raw_input())
            print "Enter value to deleted"
            value = int(raw_input())
            node = FindNode(binomialHeapList[index], value)
            if node != None:
                binomialHeapList[index] = BinomialHeapDelete(binomialHeapList[index], node)
            else:
                print "The given value does not exist in the heap."
        elif inp == 5:
            print "Enter an index to select a heap, one of: ", range(0,len(binomialHeapList))
            index = int(raw_input())
            print "Enter value to decrease key of"
            value = int(raw_input())
            node = FindNode(binomialHeapList[index], value)
            if node != None:
                print "Enter the new key for this node"
                newValue = int(raw_input())
                x = BinomialHeapDecreaseKey(binomialHeapList[index], node, newValue)
                if x != None:
                    binomialHeapList[index] = x
                    print "The key has been decreased print the heap at index: ", index," to view its status."
                else:
                    print "The new key is greater than existing value"
            else:
                print "The given value does not exist in the heap."
        elif inp == 6:
            print "Enter an index to select a heap, one of: ", range(0,len(binomialHeapList))
            index1 = int(raw_input())
            print "Enter an index to select another heap"
            index2 = int(raw_input())
            heap1 = binomialHeapList[index1]
            heap2 = binomialHeapList[index2]
            if index1 < index2:
                binomialHeapList.pop(index2)
                binomialHeapList.pop(index1)    
            else:
                binomialHeapList.pop(index1)
                binomialHeapList.pop(index2)
            b = BinomialHeapUnion(heap1, heap2)
            binomialHeapList.append(b)
            print "Merged the heaps at index ", index1, " and index ", index2
            print "To see the merged heap print the heap at index ", len(binomialHeapList) - 1
        elif inp == 7:
            print "Enter an index to select a heap, one of: ", range(0,len(binomialHeapList))
            index = int(raw_input())
            print "Below is the heap at index ", index
            PrintBinomialHeap(binomialHeapList[index])
        else:
            print "Invalid Input. Please try again.\n"
    
run()

# Test input.
"""
b = MakeBinomialHeap()
b = BinomialHeapInsert(b,12)
print "insert 12"
PrintBinomialHeap(b)
b = BinomialHeapInsert(b,7)
print "insert 7"
PrintBinomialHeap(b)
b = BinomialHeapInsert(b,25)
print "insert 25"
PrintBinomialHeap(b)
b = BinomialHeapInsert(b,15)
print "insert 15"
PrintBinomialHeap(b)
b = BinomialHeapInsert(b,28)
print "insert 28"
PrintBinomialHeap(b)
b = BinomialHeapInsert(b,33)
print "insert 33"
PrintBinomialHeap(b)
b = BinomialHeapInsert(b,41)
print "insert 41"
PrintBinomialHeap(b)
#print b.min.data

print "--------------------------------------------------"
print BinomialHeapExtractMin(b).data
print "--------------------------------------------------"
PrintBinomialHeap(b)
"""
