import time

from wintersweet.utils.structure import Node


class TimestampNode(Node):

    def __init__(self, *args, **kwargs):
        super(TimestampNode, self).__init__(*args, **kwargs)
        self.timestamp = time.time()


class LRUCache:
    """
    使用频率排列缓存，最近使用过的靠前，满水位时优先剔除过期缓存，再剔除最长时间未使用缓存
    """
    def __init__(self, maximum: int = 100, ttl=3600):

        self._ttl = ttl
        self._maximum = maximum
        self._node_cache = {}
        self._size = 0

        self._head = None
        self._tail = None

    def __delete(self, node):

        self._size -= 1
        if node == self._head:
            temp_node = node.next
            if temp_node:
                temp_node.prev = None
                node.next = None
            self._head = temp_node

        elif node == self._tail:
            temp_node = node.prev
            if temp_node:
                temp_node.next = None
                node.prev = None
            self._tail = temp_node

        else:
            node.prev.next = node.next
            node.next.prev = node.prev

    def __append(self, node):
        self._size += 1
        if self._head is None:
            self._head = self._tail = node
        else:
            node.next = self._head
            self._head.prev = node

            self._head = node

    def __timeout_remove(self):
        temp = self._tail
        while temp and self._size >= self._maximum:
            prev = temp.prev
            if temp.timestamp + self._ttl < time.time():
                self.__delete(temp)
                self._node_cache.pop(temp.key)
            temp = prev

        while self._size >= self._maximum:
            tail_key = self._tail.key
            self.__delete(self._tail)
            self._node_cache.pop(tail_key)

    def get(self, key):

        if key not in self._node_cache:
            return None

        node = self._node_cache[key]
        if node.timestamp + self._ttl < time.time():
            self.__delete(node)
            self._node_cache.pop(key)

            return None

        self.__delete(node)
        self.__append(node)

        return node.val

    def put(self, key, val):

        if key in self._node_cache:
            node = self._node_cache[key]
            node.val = val

            self.__delete(node)
            self.__append(node)
        else:
            self.__timeout_remove()

            node = TimestampNode(key, val)
            self.__append(node)
            self._node_cache[key] = node

    def top(self):
        return self._head.val

    def list(self):

        node_list = []
        if self._head is None:
            return node_list

        temp = self._head
        while temp is not None:
            if temp.timestamp + self._ttl < time.time():
                temp = temp.next
                continue
            node_list.append((temp.key, temp.val))
            temp = temp.next

        return node_list





