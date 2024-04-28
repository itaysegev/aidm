import time

from aidm.search.node import Node


class ComputationalResources:

    def __init__(self, iteration_bound=None, time_bound=None, depth_bound=None):

        # creating the initial state object
        self.iteration_bound = iteration_bound
        self.iteration_count = 0

        self.time_bound = time_bound
        self.init_time = time.time()
        self.current_time = self.init_time

        self.depth_bound= depth_bound

    def reset(self):

        # creating the initial state object
        if self.iteration_bound:
            self.iteration_count = 0

        if self.time_bound:
            self.init_time = time.time()
            self.current_time = self.init_time

    # return whether there are any remaining resources
    def are_exhausted(self, node=Node):

        if self.iteration_bound:
            if self.iteration_count > self.iteration_bound:
                return True

        if self.time_bound:
            if self.current_time - self.init_time > self.time_bound:
                return True

        if self.depth_bound:
            if len(node.get_transition_path())>self.depth_bound:
                return True

        return False

    def update(self, cur_iteration= None, cur_time = None):

        if cur_iteration:
            self.iteration_count = cur_iteration
        else:
            self.iteration_count += 1

        if cur_time:
            self.current_time= cur_time
        else:
            self.current_time = time.time()

    def __str__(self):

        return 'iteration count:%s elapsed time (sec):%.2f'%(self.iteration_count, self.current_time-self.init_time)