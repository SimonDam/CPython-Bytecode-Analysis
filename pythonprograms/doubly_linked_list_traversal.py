n = 3670015
min_n = 1
def source_code(n):	
    return f"""# Taken from: https://www.rosettacode.org/wiki/Doubly-linked_list/Traversal#Python

def print(*args, **kwargs):
    pass

class List:
    def __init__(self, data, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev
 
    def append(self, data):
        if self.next == None:
            self.next = List(data, None, self)
            return self.next
        else:
            return self.next.append(data)
 
# Build the list
tail = head = List(10)
n = {n}
for i in range(n):
    tail = tail.append(i)
 
# Traverse forwards
node = head
while node != None:
    print(node.data)
    node = node.next
 
# Traverse Backwards
node = tail
while node != None:
    print(node.data)
    node = node.prev

"""
