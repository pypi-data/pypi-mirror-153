

class Node:

    def __init__(self, _key, _val, _prev=None, _next=None):
        self.key = _key
        self.val = _val
        self.prev = _prev
        self.next = _next

    def __str__(self):
        return f'Node({self.key}, {self.val})'
