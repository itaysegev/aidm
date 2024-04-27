import queue
from abc import ABC, abstractmethod


class Container(ABC):

    """Container is an abstract class/interface. There are three types:
        Stack(): A Last In First Out Queue.
        FIFOQueue(): A First In First Out Queue.
        PriorityQueue(order, f): Queue in sorted order (default min-first).
    Each type supports the following methods and functions:
        q.append(item)  -- add an item to the queue
        q.extend(items) -- equivalent to: for item in items: q.append(item)
        q.pop()         -- return the top item from the queue
        len(q)          -- number of items in q (also q.__len())
        item in q       -- does q contain item?
     """
    def __init__(self, container, max_len=None):

        self.container = container
        self.max_len = max_len


    @abstractmethod
    def add(self, item, check_existance=False):
        pass

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __contains__(self, item):
        pass

    @abstractmethod
    def __repr__(self, key):
        pass

    def is_empty(self):
        len = self.__len__()
        if len == 0:
            return True
        else:
            return False


class Queue(Container):

    def __init__(self, queue, max_len=None):
        super().__init__(queue, max_len)

    def add(self, item, check_existance=False):

        if check_existance and self.__contains__(item):
            return

        if not self.max_len or self.__len__() < self.max_len:
            self.container.put(item)
        else:
            raise Exception('FIFOQueue is full')

    def extract(self):
        return self.container.get()

    def __len__(self):
        return self.container.qsize()

    #todo: check if this works
    def __contains__(self, item):
        return item in self.container.queue

    def __repr__(self):
        queue_string = ''
        for item in self.container:
            queue_string+= ' '
            queue_string+= item

        return queue_string


class FIFOQueue(Queue):

    def __init__(self, max_len=None):
        super().__init__(queue.Queue(), max_len)


class LIFOQueue(Queue):

    def __init__(self, max_len=None):
        super().__init__(queue.LifoQueue(), max_len)


class PriorityQueue(Queue):

    """A queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first. If order is min, the item with minimum f(x) is
    returned first; if order is max, then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, eval_func=lambda x: x, max_len=None):
        super().__init__(queue.PriorityQueue(), max_len)
        self.eval_func = eval_func

    def add(self, node):
        eval_value = self.eval_func(node)
        super().add((eval_value, node))

    def extract(self):
        return self.container.get()[1]
