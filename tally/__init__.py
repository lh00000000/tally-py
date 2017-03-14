from .data_structures import LinkedList, Node

class Tally:

    def __init__(self):
        self.items = {}
        self.counts = LinkedList()

    @staticmethod
    def _new_count_node(count):
        return Node({
            'count': count,
            'items': LinkedList(),
        })

    @staticmethod
    def _new_item_node(key, count_node):
        return Node({
            'key': key,
            'count_node': count_node
        })

    @staticmethod
    def _transfer(node, new_list):
        node.prev.connect(node.next)
        new_list.append(node)

    def _welcome_key(self, key):
        """welcome our new friend"""
        if self.counts.empty() or self.counts.first().o['count'] != 1:
            self.counts.prepend(Tally._new_count_node(1))

        count_node = self.counts.first()
        self.items[key] = Tally._new_item_node(key, count_node)
        count_node.o['items'].append(self.items[key])

    def _make_next_count_node(self, count_node):
        _new_count_node = Tally._new_count_node(
            count_node.o["count"] + 1)
        _new_count_node.connect(count_node.next)
        count_node.connect(_new_count_node)

    def tally(self, key):
        if key not in self.items:
            self._welcome_key(key)
        else:
            item = self.items[key]
            count_node = item.o['count_node']

            # ensure that the next count node over represents (this item's
            # current count) + 1
            if count_node.next.o == 'TAIL' or count_node.next.o['count'] > count_node.o['count'] + 1:
                self._make_next_count_node(count_node)

            Tally._transfer(item, count_node.next.o['items'])
            item.o['count_node'] = count_node.next

            if count_node.o['items'].empty():
                count_node.prev.connect(count_node.next)

    def remove(self, key):
        item = self.items[key]
        item.prev.connect(item.next)
        if item.o['count_node'].o['items'].empty():
            item.o['count_node'].prev.connect(item.o['count_node'].next)

        del self.items[key]

    def ascending(self):
        for count_node in self.counts:
            count = count_node.o['count']
            for item in count_node.o['items']:
                yield item.o['key'], count

    def descending(self):
        for count_node in self.counts.reversed():
            count = count_node.o['count']
            for item in count_node.o['items'].reversed():
                yield item.o['key'], count
