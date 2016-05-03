"""
Question : 
    Given an input file store the word count and positions in a Hash Table.
Answer:
    H = makeHashForWordsInFile(inputFilename)
    writeOutputToFile(H, outputFilename)

General Hash Table Usage:
Create Hash Table:
    h = HashTable()
Insert Value:
    h.insert(key,value)
Find:
    h.find(key)
"""

# Constant for Hash Table Size 
TABLE_SIZE = 701

class Node:
    def __init__(self,word,count,next=None):
        self.word = word
        self.count = count
        self.next = next
        self.positions = []
    
    def UpdateCount(self, count):
        self.count = count
        
class LinkedList:
    def __init__(self,head=None):
        self.head = head
        
    def Insert(self,node):
        node.next = self.head
        self.head = node
    
    def Search(self,k):
        node = self.head
        while node != None:
            if node.word == k:
                return node
            node = node.next
        return None
        
    def Delete(self, k):
        if self.head is None:
            return "Overflow"
        else:
            found = False
            #Delete from Head
            if self.head.word == k:
                n = self.head
                self.head = n.next
                n.next = None
                found = True
            #Delete from Middle and end    
            else:
                prev = self.head
                curr = self.head.next
                while curr is not None:
                    if curr.word == k:
                        prev.next = curr.next
                        curr.next = None
                        found = True
                    prev = curr
                    curr = curr.next    
            return found
            
    # Helper functions to view output.                
    def PrintList(self):
        h = self.head
        while h != None:
            print h.word + ":" + str(h.count) 
            h = h.next 
    
    def ListAsString(self):
        h = self.head
        l = []
        while h != None:
            l.append(h.word + ":" + str(h.count) +" positions: " + str(h.positions))
            h = h.next
        return l

class HashTable:
    def __init__(self,size=TABLE_SIZE):
        self.table = []
        self.size = size
        i=0 
        while i < size:
            self.table.append(None)
            i = i + 1
    
    def find(self,key):
        index = HashFunction(key)
        if self.table[index] is not None:
            return self.table[index].Search(key)
        else:
            return None
            
    def insert(self,key,value):
        index = HashFunction(key)
        if self.table[index] == None:
            n = Node(key,1)
            self.table[index] = LinkedList(n)
        else:
            node = self.find(key)
            if node is not None:
                node.count = node.count + value
            else:
                node = Node(key,value)
                self.table[index].Insert(node)
        return index
    
    def increase(self, key):
        return self.insert(key,1)
                
    def delete(self,key):
        return self.table[HashFunction(key)].Delete(key)
        
    def listAllKeys(self):
        i=0 
        while i<self.size:
            if self.table[i] != None:
                print "At index ",i
                self.table[i].PrintList()
            i = i + 1
            

# Group in 4 character's convert each group to integer and sum. Then mod this index with Table Size.        
import struct
def HashFunction(k):
    i = 0
    index = 0
    # Making the word length a multiple of 4 by adding trailing 0's
    end = len(k)
    while (end%4 != 0):
        k = k + "0"
        end = end + 1
    while i<len(k):
        str4 = k[i:i+4] 
        index += struct.unpack("=i",str4)[0]    
        i = i + 4
    return index % TABLE_SIZE
    """
    # Secondary Hash Function could be
    # Use sum of ascii value to the power of its significance as index. 
    k = k.lower()
    i=0
    weight = len(k)
    index = 0
    while i<len(k):
        index = index + (ord(k[i]) ** weight)
        weight = weight - 1 
        i = i + 1
    index = index % TABLE_SIZE
    print index
    return index
    """


import re
def makeHashForWordsInFile(filename="alice.txt"):
    f = open(filename,"r")
    h = HashTable(TABLE_SIZE)
    hpos = HashTable(TABLE_SIZE)
    # Read file Line by Line
    wordcount = 0
    for line in f:
        words = line.split(" ")
        # Work on each word in the current line.
        for word in words:
            if len(word) > 0:
                word = word.lower() 
                reg = re.compile("[a-zA-Z0-9]+", re.IGNORECASE)
                m = reg.search(word)
                #Trimming word according to Regular Expression.[a-zA-Z0-9]
                if m is not None:
                    wordcount = wordcount + 1
                    validWord = m.group()
                    i = h.increase(validWord)
                    #Added for listing positions.
                    node = h.find(validWord)
                    node.positions.append(wordcount)
    f.close()
    return h
    
def writeOutputToFile(H, filename="aliceWordCount.txt"):
    f = open(filename,"w")
    i = 0
    while i < TABLE_SIZE:
        if H.table[i] is not None:
            st = H.table[i].ListAsString()
            for word in st:
                f.write(str(i)+ " " + word + "\n")
        i = i + 1
    f.close()
    

"""
H = makeHashForWordsInFile()
writeOutputToFile(H)       
"""