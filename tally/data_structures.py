

class Node:

    def __init__(self, o={}, _next=None, prev=None, parent=None):
        self.o = o
        self.next = _next
        self.prev = prev

    def __str__(self):
        return str(self.o)

    def connect(self, next_node):
        self.next = next_node
        next_node.prev = self


class LinkedList:

    def __init__(self):
        self.head = Node('HEAD')
        self.tail = Node('TAIL')

        self.head.next = self.tail
        self.tail.prev = self.head

    def prepend(self, node, debug=False):
        node.connect(self.head.next)
        self.head.connect(node)

    def append(self, node, debug=False):
        self.tail.prev.connect(node)
        node.connect(self.tail)

    def empty(self):
        return self.head.next == self.tail and self.tail.prev == self.head

    def first(self):
        return self.head.next

    def last(self):
        return self.tail.prev

    def __iter__(self):
        current = self.first()
        while True:
            if current.o == 'TAIL':
                return
            yield current
            current = current.next

    def reversed(self):
        current = self.last()
        while True:
            if current.o == 'HEAD':
                return
            yield current
            current = current.prev

    def __str__(self):
        return '\n'.join([
            '<ll>',
            'head: \n{}\n'.format(self.head),
            'tail: \n{}\n'.format(self.tail),
            'nodes:',
        ] + list(map(str, enumerate(zip(self, map(str, self))))) + ['</ll>'])

