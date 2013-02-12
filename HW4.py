## Amy Finnegan
## HW4: Linked List
## I've noted where some of these aren't working
## Hopefully you can help me de-bug them!

class Node:
  def __init__(self, _value=None, _next=None):
    self.value  = _value
    self.next = _next

  def __str__(self):
    return str(self.value)




class LinkedList:
  def __init__(self, value):
      self.head = Node(value)
      self.tail = None
      self.length = 0

     
  def __str__(self):
    return str(self.printNodes())

  def printNodes(self):
    node = self.head
    while node != None:
     print node
     node = node.next
     # O(n) because it has to do something to each element
     
  def length(self):
    return self.length
    
  def addNode(self, new_value):
    new_node = Node(new_value)
    if self.head == None:
      self.head = new_node
      self.tail = new_node
      new_node.next = None
      self.length = self.length + 1
    elif self.tail == None:
      self.head.next = new_node
      self.tail = new_node
      self.tail.next = None
      self.length = self.length + 1
    elif self.tail != None:
      self.tail.next = new_node
      new_node.next = None
      self.tail = new_node
      self.length = self.length + 1
    # O(1) and added time for each if statement
    # nodes are added to the end so it's quick
      
  def addNodeAfter(self, new_value, after_node):
    insert_node = Node(new_value)
    if after_node == self.length - 1:
      addNode(new_value)
    else:
      i = 0
      active_node = self.head
      while i < after_node:
        active_node = active_node.next
        i += 1
      insert_node.prev = active_node
      insert_node.next = active_node.next
      active_node.next.prev = insert_node
      active_node.next = insert_node
      self.length += 1
    # O(1) + search time.  This could probably be sped up
    # since it has to search and do a lot of things
      
  def addNodeBefore(self, new_value, before_node):
    insert_node = Node(new_value)
    if before_node == 1:
      self.head.prev = insert_node.next
      insert_node.next = self.head
      self.head = insert_node
      insert_node.prev = None
      self.length = self.length + 1
    elif before_node > 1:
      active_node = self.head
      i = 1
      while i < before_node:
        active_node = active_node.next
        i += 1
      active_node.prev = insert_node
      insert_node.next = active_node
      active_node.prev.next = insert_node
      #insert_node.prev = active_node.prev.prev
      #insert_node.next = active_node
      self.length = self.length + 1  # not working  
    # NOT WORKING TO INSERT IN MIDDLE
    # O(1) + search time
    
  def removeNode(self, node_to_remove):
     if node_to_remove == 0:
       active_node = self.head
       new_head = active_node.next
       self.head = new_head
       self.length = self.length - 1
     elif node_to_remove != 0:
      active_node = self.head
      i = 1
      while i != node_to_remove:
        active_node = active_node.next
        i += 1
      active_node.next = active_node.next.next
      self.length = self.length - 1
# O(1) + search time     
  
  def findNode(self, value):
    active_node = self.head
    while active_node is not None:
      if active_node.value == value:
        return active_node
      active_node = active_node.next
# O(1) + search time

  def removeNodeByValue(self, value):
    node_to_remove = self.findNode(value)
    left_node = node_to_remove.prev
    left_node.next = left_node.next.next
    self.length = self.length - 1
# can't remove the node if it's the first value because there is no "prev"
# O(1) + search time
  



  def reverse(self):
    last = None
    current = self.head
    
    while current is not None:
      next = current.next
      current.next = last
      last = current
      current = next
      return    
# O(1) + search time

  def reverseNew(self):
    if self.head == None: return
    elif self.head.next == None: return
    else:
      prev = self.head
      current = self.head
      next = self.head.next
      #self.head.next = None
    
      while next != None:
        current = next
        next = current.next
        current.next = prev
        prev = current
        return
      head = current
# O(n) - this is probably the slowest one because
# it has to do something to each node
# NOT WORKING - just returns the first and second node over and over


print 'Check to see that nodes can be added'
L = LinkedList(1)
L.addNode(12)
L.addNode(14)
L.addNode(16)
L.addNode(18)

print L

print '\nAdd odd numbers'
L.addNodeAfter(13, 1)
L.addNodeAfter(15, 3)
#L.addNodeBefore(6, 17)
L.addNodeBefore(0, 1)

L.addNodeBefore(17, 7) # doesn't work

print L

print '\nRemove first, second and 14'
L.removeNode(0) 
L.removeNode(0)
L.removeNodeByValue(14)

print L

#L.reverseNew()


#print L




  


