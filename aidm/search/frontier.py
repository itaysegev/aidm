import queue, heapq
from abc import ABC, abstractmethod
from ..core.defs import NEG_INFNTY, INFNTY
import numpy as np

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

    @abstractmethod
    def add(self, item, problem=None, check_existance=False):
        pass

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

    def is_empty(self):
        return True if self.__len__()==0 else False


class Queue(Container):

    def __init__(self, queue, max_len=None):
        self.queue = queue
        self.max_len = max_len

    def add(self, item, problem=None, check_existance=False):
        if check_existance and self.__contains__(item):
            return
        if not self.max_len or self.__len__() < self.max_len:
            self.queue.put(item)
        else:
            raise Exception('FIFOQueue is full')

    def extract(self):
        return self.queue.get()

    def __len__(self):
        return self.queue.qsize()

    def print(self):
        pass


class FIFOQueue(Queue):

    def __init__(self, max_len=None):
        super().__init__(queue.Queue(), max_len)


class LIFOQueue(Queue):

    def __init__(self, max_len=None):
        super().__init__(queue.LifoQueue(), max_len)


class PriorityQueue(Queue):

    def __init__(self, eval_func=lambda x: x, max_len=None, check_before_insert=True):
        super().__init__(queue=[],max_len=max_len)
        self.eval_func = eval_func
        self._index = 0
        self.check_before_insert = check_before_insert

    def add(self, item, problem, check_existance=True):
        priority = self.eval_func(item,problem)
        if self.check_before_insert:
            if priority<=-np.inf or priority>=np.inf or priority is None:
                print('value of nodes exceeds value bounds')
                return
        heapq.heappush(self.queue, (priority, self._index, item))
        self._index += 1

    def extract(self):
        return heapq.heappop(self.queue)[-1]

    def __len__(self):
        return len(self.queue)

    def print(self):
        for element in self.queue:
            print(element)